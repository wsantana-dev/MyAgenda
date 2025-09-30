from flask import Flask, render_template, request, redirect, url_for
import psycopg2
import psycopg2.extras
import os

app = Flask(__name__)

# Configuração do PostgreSQL via variáveis de ambiente (Render)
DB_HOST = os.environ.get('DB_HOST')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
DB_PORT = os.environ.get('DB_PORT', 5432)

# Função para conectar ao banco
def get_db_connection():
    conn = psycopg2.connect(
        host=DB_HOST,
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        port=DB_PORT,
        cursor_factory=psycopg2.extras.DictCursor
    )
    return conn

# Página inicial - listar contatos
@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM contatos")
    contatos = cur.fetchall()
    cur.close()
    conn.close()
    return render_template('index.html', contatos=contatos)

# Rota para adicionar contato
@app.route('/add', methods=['GET', 'POST'])
def add_contato():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "INSERT INTO contatos (nome, email, telefone) VALUES (%s, %s, %s)",
            (nome, email, telefone)
        )
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add.html')

# Rota para excluir contato
@app.route('/delete/<int:id>')
def delete_contato(id):
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("DELETE FROM contatos WHERE id = %s", (id,))
    conn.commit()
    cur.close()
    conn.close()
    return redirect(url_for('index'))

# Rota para editar contato
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contato(id):
    conn = get_db_connection()
    cur = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        cur.execute("""
            UPDATE contatos
            SET nome = %s, email = %s, telefone = %s
            WHERE id = %s
        """, (nome, email, telefone, id))
        conn.commit()
        cur.close()
        conn.close()
        return redirect(url_for('index'))

    cur.execute("SELECT * FROM contatos WHERE id = %s", (id,))
    contato = cur.fetchone()
    cur.close()
    conn.close()
    return render_template('edit.html', contato=contato)

# Execução local (desabilitado no Render)
if __name__ == '__main__':
    app.run(debug=True)
