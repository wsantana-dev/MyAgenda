from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__)

# Configuração do MySQL (XAMPP)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # no XAMPP normalmente é vazio
app.config['MYSQL_DB'] = 'myagenda'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'

mysql = MySQL(app)

# Página inicial - listar contatos
@app.route('/')
def index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM contatos")
    contatos = cur.fetchall()
    cur.close()
    return render_template('index.html', contatos=contatos)

# Rota para adicionar contato
@app.route('/add', methods=['GET', 'POST'])
def add_contato():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']

        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO contatos (nome, email, telefone) VALUES (%s, %s, %s)", (nome, email, telefone))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    return render_template('add.html')




# Rota para excluir contato
@app.route('/delete/<int:id>')
def delete_contato(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM contatos WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    return redirect(url_for('index'))

# Rota para editar contato
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_contato(id):
    cur = mysql.connection.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        cur.execute("""
            UPDATE contatos
            SET nome = %s, email = %s, telefone = %s
            WHERE id = %s
        """, (nome, email, telefone, id))
        mysql.connection.commit()
        cur.close()
        return redirect(url_for('index'))

    # Se for GET → carrega os dados do contato
    cur.execute("SELECT * FROM contatos WHERE id = %s", (id,))
    contato = cur.fetchone()
    cur.close()
    return render_template('edit.html', contato=contato)


    # Se for GET → carrega os dados do contato
    cur.execute("SELECT * FROM contatos WHERE id = %s", (id,))
    contato = cur.fetchone()
    cur.close()
    return render_template('edit.html', contato=contato)

if __name__ == '__main__':
    app.run(debug=True)