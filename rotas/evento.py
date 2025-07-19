from flask import Blueprint, request, jsonify
import psycopg2
from database import execute_query
import json

evento_bp = Blueprint("evento", __name__)

@evento_bp.route("/eventos", methods=["POST"])
def criar_evento():
    dados = request.json
    query = """
        INSERT INTO evento (nome, descricao, data_inicio, data_fim, id_local, id_categoria, id_organizador, preco)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    try:
        execute_query(query, (
            dados["nome"],
            dados["descricao"],
            dados["data_inicio"],
            dados["data_fim"],
            dados["id_local"],
            dados["id_categoria"],
            dados["id_organizador"],
            dados.get("preco")  
        ))
        return {"mensagem": "Evento criado com sucesso!"}, 201

    except psycopg2.errors.ForeignKeyViolation as e:
        error_message = str(e)
        if "fk_local" in error_message:
            return {"erro": "O local informado não existe."}, 400
        elif "fk_categoria" in error_message:
            return {"erro": "A categoria informada não existe."}, 400
        elif "fk_organizador" in error_message:
            return {"erro": "O organizador informado não existe."}, 400
        else:
            return {"erro": "Erro de integridade referencial: " + error_message}, 400

    except Exception as e:
        return {"erro": "Erro inesperado: " + str(e)}, 500

@evento_bp.route("/eventos/<int:id_evento>", methods=["GET"])
def obter_evento(id_evento):
    query = "SELECT * FROM evento WHERE id_evento = %s"
    evento = execute_query(query, (id_evento,), fetchone=True)
    if evento:
        return jsonify(evento)
    return {"mensagem": "Evento não encontrado"}, 404

@evento_bp.route("/eventos", methods=["GET"])
def listar_eventos():
    query = "SELECT * FROM evento"
    eventos = execute_query(query, fetch=True)
    return jsonify(eventos)

@evento_bp.route("/eventos/<int:id_evento>", methods=["PUT"])
def atualizar_evento(id_evento):
    dados = request.json
    query = """
        UPDATE evento
        SET nome = %s, descricao = %s, data_inicio = %s, data_fim = %s, id_local = %s, id_categoria = %s, id_organizador = %s, preco = %s
        WHERE id_evento = %s
    """
    execute_query(query, (
        dados["nome"],
        dados["descricao"],
        dados["data_inicio"],
        dados["data_fim"],
        dados["id_local"],
        dados["id_categoria"],
        dados["id_organizador"],
        dados.get("preco"), 
        id_evento
    ))
    return {"mensagem": "Evento atualizado com sucesso"}

@evento_bp.route("/eventos/<int:evento_id>", methods=["DELETE"])
def deletar_evento(evento_id):
    usuario = request.headers.get("X-Usuario") or "desconhecido"

    evento = execute_query("SELECT * FROM evento WHERE id_evento = %s", (evento_id,), fetchone=True)

    if not evento:
        return jsonify({"erro": "Evento não encontrado"}), 404

    query_log = """
        INSERT INTO log_geral (tabela, acao, registro_id, dados_anteriores, usuario)
        VALUES (%s, %s, %s, %s, %s)
    """
    execute_query(
        query_log,
        (
            "evento",
            "DELETE",
            evento_id,
            json.dumps(evento, default=str),
            usuario,
        ),
    )

    execute_query("DELETE FROM evento WHERE id_evento = %s", (evento_id,))
    return jsonify({"mensagem": "Evento deletado com sucesso"})
