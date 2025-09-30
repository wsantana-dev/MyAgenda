import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# Pega as variáveis do ambiente
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT', 5432)  # porta padrão 5432

def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        cursor_factory=psycopg2.extras.DictCursor
    )
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM contatos;')
    contatos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', contatos=contatos)

@app.route('/add', methods=('GET', 'POST'))
def add():
    if request.method == 'POST':
        try:
            nome = request.form['nome']
            email = request.form['email']
            telefone = request.form['telefone']

            conn = get_db_connection()
            cur = conn.cursor()
            cur.execute('INSERT INTO contatos (nome, email, telefone) VALUES (%s, %s, %s)',
                        (nome, email, telefone))
            conn.commit()
            cur.close()
            conn.close()
            return redirect(url_for('index'))
        except Exception as e:
            print("Erro ao inserir no banco:", e)  # erro no console/terminal
            return "Erro interno no servidor", 500  # mensagem simples para o usuário

    return render_template('add.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
