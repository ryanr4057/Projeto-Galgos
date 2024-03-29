import sqlite3
from datetime import datetime

data_atual = datetime.now().strftime('%d-%m-%Y')

conn = sqlite3.connect(f'banco_de_dados{ data_atual}.sqlite3')
# conn = sqlite3.connect('banco_de_dados17-04-2023.sqlite3')

conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

# Busca de elementos na tabela pistas
def buscar_pista(id):
    c.execute("SELECT * FROM pistas WHERE id = ?", (id,))
    return c.fetchone()
def buscar_pista_id_r(r_id):
    c.execute("SELECT pista_id FROM races WHERE id = ?", (r_id,))
    return c.fetchone()

def buscar_pista_nome(id):
    c.execute("SELECT nome FROM pistas WHERE id = ?", (id,))
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

def buscar_race_pis(id):
    c.execute("SELECT pista_id FROM races WHERE id = ?", (id,))
    return c.fetchone()

def buscar_race_dist(id):
    c.execute("SELECT distancia FROM races WHERE id = ?", (id))
    return c.fetchone()

def buscar_race_pick(id):
    c.execute("SELECT post_pick FROM races WHERE id = ?", (id))
    return c.fetchone()

def buscar_race_cat(id):
    c.execute("SELECT categoria FROM races WHERE id = ?", (id))
    return c.fetchone()

def buscar_race_pick(id):
    c.execute("SELECT post_pick FROM races WHERE id = ?", (id))
    return c.fetchone()


def buscar_race_id(pista_id,nome):
    c.execute("SELECT id FROM races WHERE pista_id = ? AND nome = ?", (pista_id, nome))
    return c.fetchone()

def buscar_race_id_h(pista_id, horario):
    c.execute("SELECT id FROM races WHERE pista_id = ? AND horario = ?", (pista_id, horario))
    return c.fetchone()

def buscar_race_h(race_id):
    c.execute("SELECT horario FROM races WHERE id = ?", (race_id,))
    return c.fetchone()

def buscar_race_nome(race_id):
    c.execute("SELECT nome FROM races WHERE id = ?", (race_id,))
    return c.fetchone()

def buscar_race_hor():
    c.execute("SELECT horario FROM races")
    return c.fetchall()

def buscar_todas_races():
    c.execute("SELECT * FROM races")
    return c.fetchall()

def buscar_todas_races_id():
    c.execute("SELECT id FROM races")
    return c.fetchall()

def buscar_races_por_pista(pista_id):
    c.execute("SELECT nome FROM races WHERE pista_id = ?", (pista_id))
    return c.fetchall()

def buscar_races_por_pista_i(pista_id):
    c.execute("SELECT id FROM races WHERE pista_id = ?", (pista_id))
    return c.fetchall()

def buscar_races_h_por_pista(pista_id):
    c.execute("SELECT horario FROM races WHERE pista_id = ?", (pista_id))
    return c.fetchall()


# Busca de elementos na tabela dogs
def buscar_dog(id):
    c.execute("SELECT * FROM dogs WHERE id = ?", (id,))
    return c.fetchone()

def buscar_dog_rid(nome):
    c.execute("SELECT race_id FROM dogs WHERE nome = ?", (nome,))
    return c.fetchone()

def buscar_dog_tempo_brt(id):
    c.execute("SELECT tempo_brt FROM dogs WHERE id = ?", (id,))
    return c.fetchone()

def buscar_dog_data_brt(id):
    c.execute("SELECT data_brt FROM dogs WHERE id = ?", (id,))
    return c.fetchone()

def buscar_dog_nome(nome):
    c.execute("SELECT * FROM dogs WHERE nome = ?", (nome,))
    return c.fetchone()

def buscar_dog_trap(nome):
    c.execute("SELECT trap FROM dogs WHERE nome = ?", (nome,))
    return c.fetchone()

def buscar_dog_id(nome):
    c.execute("SELECT id FROM dogs WHERE nome = ?", (nome,))
    return c.fetchone()

def buscar_todos_dogs():
    c.execute("SELECT * FROM dogs")
    return c.fetchall()

def buscar_dogs_por_race(race_id):
    c.execute("SELECT nome FROM dogs WHERE race_id = ?", (race_id))
    return c.fetchall()

def buscar_dogs_por_race_trap(race_id):
    c.execute("SELECT trap FROM dogs WHERE race_id = ?", (race_id))
    return c.fetchall()


# Busca de elementos na tabela histórico
def buscar_historico(id):
    c.execute("SELECT * FROM historico WHERE id = ?", (id,))
    return c.fetchone()


# Busca de elementos na tabela corrida
def buscar_corrida(id):
    c.execute("SELECT * FROM corrida WHERE id = ?", (id,))
    return c.fetchone()

def buscar_corridas_por_dog_dist(dog_id, dist):
    c.execute("SELECT * FROM corrida WHERE dog_id = ?  AND distancia = ?", (dog_id, dist))
    return c.fetchall()

def buscar_corridas_por_dog(dog_id):
    c.execute("SELECT * FROM corrida WHERE dog_id = ?", (dog_id,))
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
