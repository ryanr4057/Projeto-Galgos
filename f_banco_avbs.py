import sqlite3
from datetime import datetime

data_atual = datetime.now().strftime('%d-%m-%Y')

conn = sqlite3.connect(f'AvBs_{data_atual}.sqlite3')
# conn = sqlite3.connect('AvBs_24-03-2023.sqlite3')
conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

def criar_tabela_avbs():
    c.execute('''CREATE TABLE avbs (
                    id INTEGER PRIMARY KEY,
                    pista TEXT,
                    race TEXT,
                    dog_a TEXT,
                    dog_b TEXT,
                    odd_a REAL,
                    odd_b REAL,
                    pontos_a REAL,
                    pontos_b REAL,
                    vencedor TEXT,
                    resultado INTEGER
                 )''')
    conn.commit()

def inserir_avb(pista, race,  dog_a, dog_b, odd_a, odd_b, pontos_a, pontos_b, vencedor, resultado):
    c.execute("INSERT INTO avbs (pista, race,  dog_a, dog_b, odd_a, odd_b, pontos_a, pontos_b, vencedor, resultado) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", (pista, race,  dog_a, dog_b, odd_a, odd_b, pontos_a, pontos_b, vencedor, resultado))
    conn.commit()

def atribuir_result(id, resultado):
    c.execute("UPDATE avbs SET resultado = ? WHERE id = ?", (resultado, id))
    conn.commit()

def buscar_avbs_a(max, min, resultado):
    c.execute("SELECT * FROM avbs WHERE pontos_a >= ? AND pontos_b <= ? AND  resultado = ?", (max, min, resultado))
    return c.fetchall()

def buscar_avbs_b(max, min, resultado):
    c.execute("SELECT * FROM avbs WHERE pontos_b >= ? AND pontos_a <= ? AND  resultado = ?", (max, min, resultado))
    return c.fetchall()

def buscar_avbs_lim_b(max, min):
    c.execute("SELECT * FROM avbs WHERE pontos_b >= ? AND pontos_a <= ?", (max, min))
    return c.fetchall()

def buscar_avbs_lim_a(max, min):
    c.execute("SELECT * FROM avbs WHERE pontos_a >= ? AND pontos_b <= ?", (max, min))
    return c.fetchall()

def buscar_todos_avb():
    c.execute("SELECT * FROM avbs")
    return c.fetchall()

def buscar_id_avb(nome):
    c.execute("SELECT id FROM avbs WHERE dog_a == ?", (nome,))
    return c.fetchone()

def busca_nomes(id):
    c.execute("SELECT * FROM avbs WHERE id == ?", (id,))
    return c.fetchone()
