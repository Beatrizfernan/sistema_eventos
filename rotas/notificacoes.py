from flask import  Blueprint, jsonify

from scripts.envio_de_gmail_promocao import enviar_emails_pendentes


notificacao_bp = Blueprint("notificacoes", __name__)

@notificacao_bp.route("/notificacoes/enviar", methods=["GET"])
def enviar_notificacoes():
    try:
        enviar_emails_pendentes()
        return jsonify({"mensagem": "Envio de emails pendentes executado."})
    except Exception as e:
        return jsonify({"erro": f"Erro ao enviar notificações: {str(e)}"}), 500