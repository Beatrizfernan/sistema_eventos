from flask import Blueprint, request, jsonify
import psycopg2
from database import execute_query

organizador_bp = Blueprint("organizador", __name__)

@organizador_bp.route("/organizadores", methods=["POST"])
def criar_organizador():
    dados = request.json
    query = """
        INSERT INTO organizador (nome, email, cnpj)
        VALUES (%s, %s, %s)
    """
    try:
        execute_query(query, (
            dados["nome"],
            dados["email"],
            dados["cnpj"]
        ))
        return {"mensagem": "Organizador criado com sucesso!"}, 201
    except psycopg2.errors.UniqueViolation as e:
        return {"erro": "Email ou CNPJ já cadastrado."}, 400
    except Exception as e:
        return {"erro": "Erro inesperado: " + str(e)}, 500


@organizador_bp.route("/organizadores/<int:id_organizador>", methods=["GET"])
def obter_organizador(id_organizador):
    query = "SELECT * FROM organizador WHERE id_organizador = %s"
    organizador = execute_query(query, (id_organizador,), fetchone=True)
    if organizador:
        return jsonify(organizador)
    return {"mensagem": "Organizador não encontrado"}, 404


@organizador_bp.route("/organizadores", methods=["GET"])
def listar_organizadores():
    query = "SELECT * FROM organizador"
    organizadores = execute_query(query, fetch=True)
    return jsonify(organizadores)


@organizador_bp.route("/organizadores/<int:id_organizador>", methods=["PUT"])
def atualizar_organizador(id_organizador):
    dados = request.json
    query = """
        UPDATE organizador
        SET nome = %s, email = %s, cnpj = %s
        WHERE id_organizador = %s
    """
    try:
        execute_query(query, (
            dados["nome"],
            dados["email"],
            dados["cnpj"],
            id_organizador
        ))
        return {"mensagem": "Organizador atualizado com sucesso!"}
    except psycopg2.errors.UniqueViolation as e:
        return {"erro": "Email ou CNPJ já cadastrados."}, 400
    except Exception as e:
        return {"erro": "Erro ao atualizar organizador: " + str(e)}, 500


@organizador_bp.route("/organizadores/<int:id_organizador>", methods=["DELETE"])
def deletar_organizador(id_organizador):
    try:
        query = "DELETE FROM organizador WHERE id_organizador = %s"
        execute_query(query, (id_organizador,))
        return {"mensagem": "Organizador deletado com sucesso!"}
    except psycopg2.errors.ForeignKeyViolation:
        return {"erro": "Não é possível excluir o organizador pois ele está vinculado a outros registros."}, 400
    except Exception as e:
        return {"erro": "Erro ao deletar organizador: " + str(e)}, 500
