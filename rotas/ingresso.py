import datetime
import json
from flask import Blueprint, request, jsonify
import psycopg2

from database import execute_query

ingresso_bp = Blueprint("ingresso", __name__)

@ingresso_bp.route("/ingressos", methods=["POST"])
def criar_ingresso():
    dados = request.json
    query = """
        INSERT INTO ingresso (id_evento, id_participante)
        VALUES (%s, %s)
    """
    try:
        execute_query(query, (
            dados["id_evento"],
            dados["id_participante"]
        ))
        return {"mensagem": "Ingresso criado com sucesso!"}, 201
    except psycopg2.errors.ForeignKeyViolation as e:
        error_message = str(e)
        if "fk_evento" in error_message:
            return {"erro": "Evento informado não existe."}, 400
        elif "fk_participante" in error_message:
            return {"erro": "Participante informado não existe."}, 400
        else:
            return {"erro": "Violação de chave estrangeira: " + error_message}, 400
    except Exception as e:
        return {"erro": "Erro inesperado: " + str(e)}, 500


@ingresso_bp.route("/ingressos/<int:id_ingresso>", methods=["GET"])
def obter_ingresso(id_ingresso):
    query = "SELECT * FROM ingresso WHERE id_ingresso = %s"
    ingresso = execute_query(query, (id_ingresso,), fetchone=True)
    if ingresso:
        return jsonify(ingresso)
    return {"mensagem": "Ingresso não encontrado"}, 404


@ingresso_bp.route("/ingressos", methods=["GET"])
def listar_ingressos():
    query = "SELECT * FROM ingresso"
    ingressos = execute_query(query, fetch=True)
    return jsonify(ingressos)


@ingresso_bp.route("/ingressos/<int:id_ingresso>", methods=["PUT"])
def atualizar_ingresso(id_ingresso):
    dados = request.json
    query = """
        UPDATE ingresso
        SET id_evento = %s, id_participante = %s
        WHERE id_ingresso = %s
    """
    try:
        execute_query(query, (
            dados["id_evento"],
            dados["id_participante"],
            id_ingresso
        ))
        return {"mensagem": "Ingresso atualizado com sucesso!"}
    except psycopg2.errors.ForeignKeyViolation as e:
        error_message = str(e)
        if "fk_evento" in error_message:
            return {"erro": "Evento informado não existe."}, 400
        elif "fk_participante" in error_message:
            return {"erro": "Participante informado não existe."}, 400
        else:
            return {"erro": "Violação de chave estrangeira: " + error_message}, 400
    except Exception as e:
        return {"erro": "Erro ao atualizar ingresso: " + str(e)}, 500


@ingresso_bp.route("/ingressos/<int:id_ingresso>", methods=["DELETE"])
def deletar_ingresso(id_ingresso):
    from app import convert_types_to_serializable
    try:
        usuario = request.headers.get("Usuario", "desconhecido")

        
        select_query = "SELECT * FROM ingresso WHERE id_ingresso = %s"
        resultado = execute_query(select_query, (id_ingresso,),fetchone=True)

        if not resultado:
            return {"erro": "Ingresso não encontrado."}, 404

       
        delete_query = "DELETE FROM ingresso WHERE id_ingresso = %s"
        execute_query(delete_query, (id_ingresso,))

        
        log_query = """
            INSERT INTO log_geral (tabela, acao, registro_id, dados_anteriores, usuario, data_acao)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        dados_anteriores = dict(resultado)
        dados_anteriores = convert_types_to_serializable(dados_anteriores)

        execute_query(
            log_query,
            (
                "ingresso",
                "DELETE",
                id_ingresso,
                json.dumps(dados_anteriores),
                usuario,
                datetime.datetime.now(),
            ),
        )

        return {"mensagem": "Ingresso deletado com sucesso!"}

    except Exception as e:
        return {"erro": "Erro ao deletar ingresso: " + str(e)}, 500
