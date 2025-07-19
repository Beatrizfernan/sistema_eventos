import smtplib
from email.message import EmailMessage

GMAIL_USER = " "
GMAIL_PASSWORD = " "

def enviar_email(destinatario, assunto, corpo):
    msg = EmailMessage()
    msg["Subject"] = assunto
    msg["From"] = GMAIL_USER
    msg["To"] = destinatario
    msg.set_content(corpo)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASSWORD)
            smtp.send_message(msg)
        print(f"E-mail enviado para {destinatario}")
    except Exception as e:
        print(f"Erro ao enviar email: {e}")
