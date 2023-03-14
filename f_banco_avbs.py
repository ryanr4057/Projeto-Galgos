import sqlite3
from datetime import datetime

data_atual = datetime.now().strftime('%d-%m-%Y')

conn = sqlite3.connect(f'AvBs_{ data_atual}.sqlite3')
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

def buscar_avbs_por_result(resultado):
    c.execute("SELECT * FROM avbs WHERE resultado = ?", (resultado,))
    return c.fetchall()
