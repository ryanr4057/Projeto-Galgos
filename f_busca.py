import sqlite3
from datetime import datetime

data_atual = datetime.now().strftime('%d-%m-%Y')


conn = sqlite3.connect(f'banco_de_dados{ data_atual}.sqlite3')
conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

# Busca de elementos na tabela pistas
def buscar_pista(id):
    c.execute("SELECT * FROM pistas WHERE id = ?", (id,))
    return c.fetchone()

def buscar_pista_id(nome):
    c.execute("SELECT id FROM pistas WHERE nome = ?", (nome,))
    return c.fetchone()

def buscar_todas_pistas():
    c.execute("SELECT nome FROM pistas")
    return c.fetchall()


# Busca de elementos na tabela races
def buscar_race(id):
    c.execute("SELECT * FROM races WHERE id = ?", (id,))
    return c.fetchone()

def buscar_race_id(pista_id,nome):
    c.execute("SELECT id FROM races WHERE pista_id = ? AND nome = ?", (pista_id, nome))
    return c.fetchone()

def buscar_todas_races():
    c.execute("SELECT * FROM races")
    return c.fetchall()

def buscar_races_por_pista(pista_id):
    c.execute("SELECT nome FROM races WHERE pista_id = ?", (pista_id))
    return c.fetchall()


# Busca de elementos na tabela dogs
def buscar_dog(id):
    c.execute("SELECT * FROM dogs WHERE id = ?", (id,))
    return c.fetchone()

def buscar_todos_dogs():
    c.execute("SELECT * FROM dogs")
    return c.fetchall()

def buscar_dogs_por_race(race_id):
    c.execute("SELECT nome FROM dogs WHERE race_id = ?", (race_id))
    return c.fetchall()


# Busca de elementos na tabela histórico
def buscar_historico(id):
    c.execute("SELECT * FROM historico WHERE id = ?", (id,))
    return c.fetchone()


# Busca de elementos na tabela corrida
def buscar_corrida(id):
    c.execute("SELECT * FROM corrida WHERE id = ?", (id,))
    return c.fetchone()

def buscar_corridas_por_historico(historico_id):
    c.execute("SELECT * FROM corrida WHERE historico_id = ?", (historico_id,))
    return c.fetchall()



def buscar_id_pelo_nome(nome):
    conn = sqlite3.connect('nome_do_banco.db')
    c = conn.cursor()
    c.execute("SELECT id FROM dogs WHERE nome = ?", (nome,))
    resultado = c.fetchone()
    conn.close()
    if resultado is not None:
        return resultado[0]
    else:
        return None
