import time
from database import execute_query
from mailer import enviar_email

def enviar_emails_pendentes():
    
    query_notif = """
        SELECT n.id, n.id_participante, n.mensagem
        FROM notificacoes n
        WHERE n.enviado = false
    """
    notificacoes = execute_query(query_notif, fetch=True)

    for notif in notificacoes:
        
        query_email = "SELECT email FROM participante WHERE id_participante = %s"
        participante = execute_query(query_email, (notif['id_participante'],), fetchone=True)
        
        if not participante:
            print(f"Participante {notif['id_participante']} não encontrado.")
            continue

        email = participante['email']
        mensagem = notif['mensagem']
        assunto = "Notificação de Evento"

        try:
            enviar_email(email, assunto, mensagem)
           
            update_query = "UPDATE notificacoes SET enviado = true WHERE id = %s"
            execute_query(update_query, (notif['id'],))
            print(f"E-mail enviado para {email}")
        except Exception as e:
            print(f"Erro ao enviar para {email}: {e}")
