from flask import Blueprint, request, jsonify
import psycopg2
from database import execute_query

categoria_bp = Blueprint("categoria", __name__)

@categoria_bp.route("/categorias", methods=["POST"])
def criar_categoria():
    dados = request.json
    query = """
        INSERT INTO categoria (nome, descricao)
        VALUES (%s, %s)
    """
    try:
        execute_query(query, (
            dados["nome"],
            dados.get("descricao")  
        ))
        return {"mensagem": "Categoria criada com sucesso!"}, 201
    except Exception as e:
        return {"erro": "Erro ao criar categoria: " + str(e)}, 500


@categoria_bp.route("/categorias/<int:id_categoria>", methods=["GET"])
def obter_categoria(id_categoria):
    query = "SELECT * FROM categoria WHERE id_categoria = %s"
    categoria = execute_query(query, (id_categoria,), fetchone=True)
    if categoria:
        return jsonify(categoria)
    return {"mensagem": "Categoria não encontrada"}, 404


@categoria_bp.route("/categorias", methods=["GET"])
def listar_categorias():
    query = "SELECT * FROM categoria"
    categorias = execute_query(query, fetch=True)
    return jsonify(categorias)


@categoria_bp.route("/categorias/<int:id_categoria>", methods=["PUT"])
def atualizar_categoria(id_categoria):
    dados = request.json
    query = """
        UPDATE categoria
        SET nome = %s, descricao = %s
        WHERE id_categoria = %s
    """
    try:
        execute_query(query, (
            dados["nome"],
            dados.get("descricao"),
            id_categoria
        ))
        return {"mensagem": "Categoria atualizada com sucesso!"}
    except Exception as e:
        return {"erro": "Erro ao atualizar categoria: " + str(e)}, 500


@categoria_bp.route("/categorias/<int:id_categoria>", methods=["DELETE"])
def deletar_categoria(id_categoria):
    try:
        query = "DELETE FROM categoria WHERE id_categoria = %s"
        execute_query(query, (id_categoria,))
        return {"mensagem": "Categoria deletada com sucesso!"}
    except psycopg2.errors.ForeignKeyViolation:
        return {"erro": "Não é possível excluir a categoria pois ela está sendo usada em algum evento."}, 400
    except Exception as e:
        return {"erro": "Erro ao deletar categoria: " + str(e)}, 500
