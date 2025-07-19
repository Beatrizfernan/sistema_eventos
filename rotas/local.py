from flask import Blueprint, request, jsonify
import psycopg2
from database import execute_query

local_bp = Blueprint("local", __name__)

@local_bp.route("/locais", methods=["POST"])
def criar_local():
    dados = request.json
    query = """
        INSERT INTO local (nome, endereco, capacidade)
        VALUES (%s, %s, %s)
    """
    try:
        execute_query(query, (
            dados["nome"],
            dados["endereco"],
            dados.get("capacidade") 
        ))
        return {"mensagem": "Local criado com sucesso!"}, 201

    except Exception as e:
        return {"erro": "Erro inesperado: " + str(e)}, 500


@local_bp.route("/locais/<int:id_local>", methods=["GET"])
def obter_local(id_local):
    query = "SELECT * FROM local WHERE id_local = %s"
    local = execute_query(query, (id_local,), fetchone=True)
    if local:
        return jsonify(local)
    return {"mensagem": "Local não encontrado"}, 404


@local_bp.route("/locais", methods=["GET"])
def listar_locais():
    query = "SELECT * FROM local"
    locais = execute_query(query, fetch=True)
    return jsonify(locais)


@local_bp.route("/locais/<int:id_local>", methods=["PUT"])
def atualizar_local(id_local):
    dados = request.json
    query = """
        UPDATE local
        SET nome = %s, endereco = %s, capacidade = %s
        WHERE id_local = %s
    """
    try:
        execute_query(query, (
            dados["nome"],
            dados["endereco"],
            dados.get("capacidade"),
            id_local
        ))
        return {"mensagem": "Local atualizado com sucesso!"}
    except Exception as e:
        return {"erro": "Erro ao atualizar local: " + str(e)}, 500


@local_bp.route("/locais/<int:id_local>", methods=["DELETE"])
def deletar_local(id_local):
    try:
        query = "DELETE FROM local WHERE id_local = %s"
        execute_query(query, (id_local,))
        return {"mensagem": "Local deletado com sucesso!"}
    except psycopg2.errors.ForeignKeyViolation:
        return {"erro": "Não é possível excluir o local pois ele está sendo usado em algum evento."}, 400
    except Exception as e:
        return {"erro": "Erro ao deletar local: " + str(e)}, 500
