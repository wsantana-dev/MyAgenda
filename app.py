import os
from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras

app = Flask(__name__)

# Variáveis de ambiente (Render usa isso)
DB_HOST = os.getenv('DB_HOST')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASS = os.getenv('DB_PASS')
DB_PORT = os.getenv('DB_PORT', 5432)

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS,
        port=DB_PORT,
        cursor_factory=psycopg2.extras.DictCursor
    )

# Página inicial - lista contatos
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM contatos;')
    contatos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', contatos=contatos)

# Adicionar contato
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
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

    return render_template('add.html')

# Editar contato
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        cur.execute('UPDATE contatos SET nome=%s, email=%s, telefone=%s WHERE id=%s',
                    (nome, email, telefone, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    # GET - buscar dados do contato para preencher o formulário
    cur.execute('SELECT * FROM contatos WHERE id = %s', (id,))
    contato = cur.fetchone()
    cur.close()
    conn.close()

    return render_template('edit.html', contato=contato)

# Deletar contato
@app.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('DELETE FROM contatos WHERE id = %s', (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

# Rodar localmente (ignorado no Render)
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
