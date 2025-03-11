from flask import Flask, jsonify, request
import sqlite3

app = Flask(__name__)

# Função para conectar ao banco de dados
def conectar_bd():
    conexao = sqlite3.connect('alunos.db')
    conexao.row_factory = sqlite3.Row
    return conexao

# Configurar a base de dados (criação da tabela e inserção de dados de exemplo)
def configurar_bd():
    with conectar_bd() as conexao:
        conexao.execute('''
            CREATE TABLE IF NOT EXISTS alunos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                idade INTEGER NOT NULL,
                curso TEXT NOT NULL
            )
        ''')
        # Inserir alguns dados iniciais
        conexao.execute('''
            INSERT INTO alunos (nome, idade, curso)
            VALUES
                ('Ana Silva', 22, 'Engenharia'),
                ('Carlos Souza', 25, 'Medicina'),
                ('Joana Pereira', 20, 'Administração')
        ''')
        conexao.commit()

# Configurando a base de dados antes de iniciar o servidor
configurar_bd()

# Rota para listar todos os alunos
@app.route('/alunos', methods=['GET'])
def listar_alunos():
    with conectar_bd() as conexao:
        cursor = conexao.execute('SELECT * FROM alunos')
        alunos = [dict(row) for row in cursor.fetchall()]
    return jsonify(alunos)

# Rota para consultar um aluno específico pelo ID
@app.route('/alunos/<int:aluno_id>', methods=['GET'])
def consultar_aluno(aluno_id):
    with conectar_bd() as conexao:
        cursor = conexao.execute('SELECT * FROM alunos WHERE id = ?', (aluno_id,))
        aluno = cursor.fetchone()
    if aluno:
        return jsonify(dict(aluno))
    return jsonify({'erro': 'Aluno não encontrado'}), 404

# Rota para adicionar um novo aluno
@app.route('/alunos', methods=['POST'])
def adicionar_aluno():
    novo_aluno = request.get_json()
    with conectar_bd() as conexao:
        cursor = conexao.execute('''
            INSERT INTO alunos (nome, idade, curso) VALUES (?, ?, ?)
        ''', (novo_aluno['nome'], novo_aluno['idade'], novo_aluno['curso']))
        conexao.commit()
        novo_aluno['id'] = cursor.lastrowid
    return jsonify(novo_aluno), 201

if __name__ == '__main__':
    app.run(debug=True)
