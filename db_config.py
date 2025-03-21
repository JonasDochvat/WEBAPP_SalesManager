from flask import Flask, render_template, jsonify
import psycopg2
from dotenv import load_dotenv
import os
app = Flask(__name__)


# Carregar as variáveis do arquivo .env
load_dotenv()

# Conexão com o banco de dados usando variáveis de ambiente
def conectar():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        host=os.getenv("DB_HOST"),  
        user=os.getenv("DB_USER"), 
        password=os.getenv("DB_PASSWORD"),
        port="5432"  # Porta padrão do PostgreSQL
    )