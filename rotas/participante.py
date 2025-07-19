from flask import Blueprint, request, jsonify
import psycopg2
from database import execute_query

participante_bp = Blueprint("participante", __name__)

@participante_bp.route("/participantes", methods=["POST"])
def criar_participante():
    dados = request.json
    query = """
        INSERT INTO participante (nome, email, telefone)
        VALUES (%s, %s, %s)
    """
    try:
        execute_query(query, (
            dados["nome"],
            dados["email"],
            dados.get("telefone")
        ))
        return {"mensagem": "Participante criado com sucesso!"}, 201
    except psycopg2.errors.UniqueViolation:
        return {"erro": "Email já cadastrado."}, 400
    except Exception as e:
        return {"erro": "Erro inesperado: " + str(e)}, 500


@participante_bp.route("/participantes/<int:id_participante>", methods=["GET"])
def obter_participante(id_participante):
    query = "SELECT * FROM participante WHERE id_participante = %s"
    participante = execute_query(query, (id_participante,), fetchone=True)
    if participante:
        return jsonify(participante)
    return {"mensagem": "Participante não encontrado"}, 404


@participante_bp.route("/participantes", methods=["GET"])
def listar_participantes():
    query = "SELECT * FROM participante"
    participantes = execute_query(query, fetch=True)
    return jsonify(participantes)


@participante_bp.route("/participantes/<int:id_participante>", methods=["PUT"])
def atualizar_participante(id_participante):
    dados = request.json
    query = """
        UPDATE participante
        SET nome = %s, email = %s, telefone = %s
        WHERE id_participante = %s
    """
    try:
        execute_query(query, (
            dados["nome"],
            dados["email"],
            dados.get("telefone"),
            id_participante
        ))
        return {"mensagem": "Participante atualizado com sucesso!"}
    except psycopg2.errors.UniqueViolation:
        return {"erro": "Email já cadastrado."}, 400
    except Exception as e:
        return {"erro": "Erro ao atualizar participante: " + str(e)}, 500


@participante_bp.route("/participantes/<int:id_participante>", methods=["DELETE"])
def deletar_participante(id_participante):
    try:
        query = "DELETE FROM participante WHERE id_participante = %s"
        execute_query(query, (id_participante,))
        return {"mensagem": "Participante deletado com sucesso!"}
    except Exception as e:
        return {"erro": "Erro ao deletar participante: " + str(e)}, 500
