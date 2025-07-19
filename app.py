
import datetime
from decimal import Decimal
from flask import Flask
from database import execute_query
from rotas.evento import evento_bp
from rotas.local import local_bp
from rotas.categoria import categoria_bp
from rotas.organizador import organizador_bp
from rotas.participante import participante_bp
from rotas.ingresso import ingresso_bp
from rotas.notificacoes import notificacao_bp

def test_connection():
    try:
        result = execute_query("SELECT 1;", fetchone=True)
        print("Conexão bem-sucedida! Resultado:", result)
    except Exception as e:
        print("Erro ao conectar ao banco:", e)

test_connection()

app = Flask(__name__)

app.register_blueprint(evento_bp)
app.register_blueprint(local_bp)
app.register_blueprint(categoria_bp)
app.register_blueprint(organizador_bp)
app.register_blueprint(participante_bp)
app.register_blueprint(ingresso_bp)
app.register_blueprint(notificacao_bp)

def convert_types_to_serializable(data):
    for k, v in data.items():
        if isinstance(v, datetime.datetime):
            data[k] = v.isoformat()
        elif isinstance(v, Decimal):
            data[k] = float(v)  
    return data

if __name__ == "__main__":
    app.run(debug=True)