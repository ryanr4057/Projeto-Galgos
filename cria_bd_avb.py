import sqlite3
from datetime import datetime

data_atual = datetime.now().strftime('%d-%m-%Y')

conn = sqlite3.connect(f'IA_bd.sqlite3')
conn.execute("PRAGMA foreign_keys = ON")
c = conn.cursor()

# Criação da tabela dados
def criar_tabela_AvBs():
    c.execute('''CREATE TABLE dados (
                    id INTEGER PRIMARY KEY,
                    dist_race INTEGER,
                    trap_a INTEGER,
                    dias_sem_correr_a INTEGER,
                    peso_a REAL,
                    m_split_a REAL,
                    m_1bend_a REAL,
                    m_pos_a REAL,
                    m_tempos_a REAL,
                    var_med_tempo_a REAL,
                    m_vel_med_a REAL,
                    m_rec_cansa_a REAL,
                    m_split_fin_a REAL,
                    status_cat_a INTEGER,
                    brt_a REAL,
                    d_brt_a INTEGER,
                    pontos_a REAL,
                    trap_b INTEGER,
                    dias_sem_correr_b INTEGER,
                    peso_b REAL,
                    m_split_b REAL,
                    m_1bend_b REAL,
                    m_pos_b REAL,
                    m_tempos_b REAL,
                    var_med_tempo_b REAL,
                    m_vel_med_b REAL,
                    m_rec_cansa_b REAL,
                    m_split_fin_b REAL,
                    status_cat_b INTEGER,
                    brt_b REAL,
                    d_brt_b INTEGER,
                    pontos_b REAL,
                    vencedor INTEGER
                 )''')
    conn.commit()

# Inserção de dados na tabela dados
def inserir_Avb(dist_race, trap_a, dias_sem_correr_a, peso_a, m_split_a, m_1bend_a, m_pos_a, m_tempos_a, var_med_tempo_a, m_vel_med_a, m_rec_cansa_a, m_split_fin_a , status_cat_a, brt_a, d_brt_a, pontos_a, trap_b, dias_sem_correr_b, peso_b, m_split_b, m_1bend_b, m_pos_b, m_tempos_b, var_med_tempo_b, m_vel_med_b, m_rec_cansa_b, m_split_fin_b , status_cat_b, brt_b, d_brt_b, pontos_b, vencedor):
    c.execute("INSERT INTO dados (dist_race, trap_a, dias_sem_correr_a, peso_a, m_split_a, m_1bend_a, m_pos_a, m_tempos_a, var_med_tempo_a, m_vel_med_a, m_rec_cansa_a, m_split_fin_a , status_cat_a, brt_a, d_brt_a, pontos_a, trap_b, dias_sem_correr_b, peso_b, m_split_b, m_1bend_b, m_pos_b, m_tempos_b, var_med_tempo_b, m_vel_med_b, m_rec_cansa_b, m_split_fin_b , status_cat_b, brt_b, d_brt_b, pontos_b, vencedor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", (dist_race, trap_a, dias_sem_correr_a, peso_a, m_split_a, m_1bend_a, m_pos_a, m_tempos_a, var_med_tempo_a, m_vel_med_a, m_rec_cansa_a, m_split_fin_a , status_cat_a, brt_a, d_brt_a, pontos_a, trap_b, dias_sem_correr_b, peso_b, m_split_b, m_1bend_b, m_pos_b, m_tempos_b, var_med_tempo_b, m_vel_med_b, m_rec_cansa_b, m_split_fin_b , status_cat_b, brt_b, d_brt_b, pontos_b, vencedor))
    conn.commit()

def buscar_todos_avb():
    c.execute("SELECT * FROM dados")
    return c.fetchall()

