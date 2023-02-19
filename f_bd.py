import sqlite3
from datetime import datetime

data_atual = datetime.now().strftime('%d-%m-%Y')

conn = sqlite3.connect(f'banco_de_dados{ data_atual}.sqlite3')
conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

# Criação da tabela pistas
def criar_tabela_pistas():
    c.execute('''CREATE TABLE pistas (
                    id INTEGER PRIMARY KEY,
                    nome TEXT
                 )''')
    conn.commit()

# Inserção de dados na tabela pistas
def inserir_pista(nome):
    c.execute("INSERT INTO pistas (nome) VALUES (?)", (nome,))
    conn.commit()

# Edição de dados na tabela pistas
def editar_pista(id, novo_nome):
    c.execute("UPDATE pistas SET nome = ? WHERE id = ?", (novo_nome, id))
    conn.commit()

# Apagar dados na tabela pistas
def apagar_pista(id):
    c.execute("DELETE FROM pistas WHERE id = ?", (id,))
    conn.commit()


# Criação da tabela races
def criar_tabela_races():
    c.execute('''CREATE TABLE races (
                    id INTEGER PRIMARY KEY,
                    nome TEXT,
                    categoria TEXT,
                    distancia INTEGER,
                    horario TEXT,
                    post_pick TEXT,
                    pista_id INTEGER,
                    FOREIGN KEY (pista_id) REFERENCES pistas(id)
                 )''')
    conn.commit()

# Inserção de dados na tabela races
def inserir_race(nome, categoria, distancia, horario, post_pick, pista_id):
    c.execute("INSERT INTO races (nome, categoria, distancia, horario, post_pick, pista_id) VALUES (?, ?, ?, ?, ?, ?)", (nome, categoria, distancia, horario, post_pick, pista_id))
    conn.commit()

# Edição de dados na tabela races
def editar_race(id, novo_nome, nova_pista_id):
    c.execute("UPDATE races SET nome = ?, pista_id = ? WHERE id = ?", (novo_nome, nova_pista_id, id))
    conn.commit()

# Apagar dados na tabela races
def apagar_race(id):
    c.execute("DELETE FROM races WHERE id = ?", (id,))
    conn.commit()


# Criação da tabela dogs
def criar_tabela_dogs():
    c.execute('''CREATE TABLE dogs (
                    id INTEGER PRIMARY KEY,
                    nome TEXT,
                    trap INTEGER,
                    race_id INTEGER,
                    FOREIGN KEY (race_id) REFERENCES races(id)
                 )''')
    conn.commit()

# Inserção de dados na tabela dogs
def inserir_dog(nome, trap, race_id):
    c.execute("INSERT INTO dogs (nome, trap, race_id) VALUES (?, ?, ?)", (nome, trap, race_id))
    conn.commit()

# Edição de dados na tabela dogs
def editar_dog(id, novo_nome, nova_race_id):
    c.execute("UPDATE dogs SET nome = ?, race_id = ? WHERE id = ?", (novo_nome, nova_race_id, id))
    conn.commit()

# Apagar dados na tabela dogs
def apagar_dog(id):
    c.execute("DELETE FROM dogs WHERE id = ?", (id,))
    conn.commit()

    c.execute("DELETE FROM historico WHERE id = ?", (id,))
    conn.commit()

# Criação da tabela corrida
def criar_tabela_corrida():
    c.execute('''CREATE TABLE corrida (
                    id INTEGER PRIMARY KEY,
                    data TEXT,
                    pista TEXT,
                    distancia INTEGER,
                    trap INTEGER,
                    split REAL,
                    bends TEXT,
                    peso REAL,
                    categoria TEXT,
                    tempo REAL,
                    posicao TEXT,
                    remarks TEXT,
                    dog_id INTEGER,
                    FOREIGN KEY (dog_id) REFERENCES dogs(id)
                 )''')
    conn.commit()

# Inserção de dados na tabela corrida
def inserir_corrida(data, pista, distancia, trap, split, bends, peso, categoria, tempo, posicao, remarks, dog_id):
    c.execute("INSERT INTO corrida (data, pista, distancia, trap, split, bends, peso, categoria, tempo, posicao, remarks, dog_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (data, pista, distancia, trap, split, bends, peso, categoria, tempo, posicao,remarks, dog_id))
    conn.commit()

# Edição de dados na tabela corrida
def editar_corrida(id, nova_data, novo_tempo, novo_historico_id):
    c.execute("UPDATE corrida SET data = ?, tempo = ?, historico_id = ? WHERE id = ?", (nova_data, novo_tempo, novo_historico_id, id))
    conn.commit()

# Apagar dados na tabela corrida
def apagar_corrida(id):
    c.execute("DELETE FROM corrida WHERE id = ?", (id,))
    conn.commit()

def buscar_id_pelo_nome(nome):
    c.execute("SELECT id FROM dogs WHERE nome = ?", (nome,))
    resultado = c.fetchone()
    if resultado is not None:
        return resultado[0]
    else:
        return None

# # Exemplo de uso das funções
# criar_tabela_pistas()
# criar_tabela_races()
# criar_tabela_dogs()
# criar_tabela_historico()
# criar_tabela_corrida()

# inserir_pista("monmore")
# # inserir_pista("Pista 2")

# inserir_race("Corrida 1","10:23", 1)
# # inserir_race("Corrida 2", 2)

# inserir_dog("Cachorro 1", 1)
# # inserir_dog("Cachorro 2", 1)

# inserir_historico(1)

# inserir_corrida("2023-02-16", "momn", 400, 1, 4.25, "1111", 30.21, "a1", 29.32, "1st", 1)

