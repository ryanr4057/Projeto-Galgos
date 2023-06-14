import sqlite3
import shutil
import glob
import os
from selenium import webdriver
import time
import re
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
import pyautogui
from datetime import datetime
import pickle
import f_busca as f
import funções_ as func


def gera_bd_all_avbs():
    arquivo_destino = 'all_avbs.sqlite3'

    diretorio_origem = os.path.dirname(os.path.abspath(__file__))


    arquivos_origem = glob.glob(os.path.join(diretorio_origem, 'AvBs_*.sqlite3'))

    # Verificar se o arquivo de destino já existe
    if os.path.exists(arquivo_destino):
        # Remover o arquivo de destino existente
        os.remove(arquivo_destino)

    # Copiar o primeiro arquivo de origem para o arquivo de destino
    shutil.copyfile(arquivos_origem[0], arquivo_destino)

    # Conectar-se ao banco de dados de destino
    conexao_destino = sqlite3.connect(arquivo_destino)
    cursor_destino = conexao_destino.cursor()

    # Obter o nome da tabela do primeiro arquivo de origem
    conexao_origem = sqlite3.connect(arquivos_origem[0])
    cursor_origem = conexao_origem.cursor()
    cursor_origem.execute("SELECT name FROM sqlite_master WHERE type='table';")
    resultado = cursor_origem.fetchone()

    # Verificar se há tabelas no primeiro arquivo de origem
    if resultado is None:
        raise ValueError("O primeiro arquivo de origem não contém tabelas.")

    tabela = resultado[0]

    # Adicionar a coluna "nome_do_arquivo_origem" na tabela do arquivo de destino
    cursor_destino.execute(f"ALTER TABLE {tabela} ADD COLUMN nome_do_arquivo_origem TEXT;")

    # Fechar a conexão com o primeiro arquivo de origem
    conexao_origem.close()

    # Iterar pelos arquivos de origem, extraindo as tabelas e inserindo no arquivo de destino
    for arquivo_origem in arquivos_origem[1:]:
        conexao_origem = sqlite3.connect(arquivo_origem)
        cursor_origem = conexao_origem.cursor()

        # Obter o nome da tabela
        cursor_origem.execute("SELECT name FROM sqlite_master WHERE type='table';")
        resultado = cursor_origem.fetchone()

        # Verificar se há tabelas nos arquivos de origem
        if resultado is None:
            continue

        tabela = resultado[0]

        # Obter os nomes das colunas da tabela
        cursor_origem.execute(f"PRAGMA table_info({tabela});")
        colunas = cursor_origem.fetchall()
        nomes_colunas = [coluna[1] for coluna in colunas]

        # Remover a coluna 'id' dos nomes das colunas
        if 'id' in nomes_colunas:
            nomes_colunas.remove('id')

        # Gerar a string de colunas para a cláusula INSERT
        colunas_insert = ', '.join(nomes_colunas)

        # Obter os dados da tabela de origem, excluindo a coluna 'id'
        cursor_origem.execute(f"SELECT {colunas_insert} FROM {tabela};")
        dados = cursor_origem.fetchall()

        # Obter os últimos 10 dígitos do nome do arquivo de origem
        nome_arquivo_or = os.path.basename(arquivo_origem)[-18:]
        nome_arquivo_origem  = nome_arquivo_or[:10]

        # Inserir os dados no banco de dados de destino, incluindo o nome do arquivo de origem
        placeholders = ', '.join(['?'] * (len(nomes_colunas) + 1))  # +1 para o nome_do_arquivo_origem
        query = f"INSERT INTO {tabela} ({colunas_insert}, nome_do_arquivo_origem) VALUES ({placeholders})"
        for linha in dados:
            valores = list(linha) + [nome_arquivo_origem]
            cursor_destino.execute(query, valores)

        # Salvar as alterações
        conexao_destino.commit()

        # Atualizar registros com nome_do_arquivo_origem como NULL com o valor do primeiro arquivo copiado
        nom = os.path.basename(arquivos_origem[0])[-18:]
        nome = nom[:10]
        cursor_destino.execute(f"UPDATE {tabela} SET nome_do_arquivo_origem = ? WHERE nome_do_arquivo_origem IS NULL", (nome,))

        # Salvar as alterações novamente
        conexao_destino.commit()


        # Fechar a conexão com o arquivo de origem
        conexao_origem.close()

    # Fechar a conexão com o arquivo de destino
    conexao_destino.close()

def atribui_resultado():
    conexao = sqlite3.connect('all_avbs.sqlite3')
    cursor = conexao.cursor()
    all_avbs = buscar_avbs(cursor)

    conn = sqlite3.connect('all_avbs_filt.sqlite3')
    c = conn.cursor()
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
                    resultado INTEGER,
                    nome_do_arquivo_origem
                 )''')
    conn.commit()

    for avb in all_avbs:
        if ((avb[7] >= 7) or (avb[8] >= 7)) and ((avb[7] != -10) and (avb[8] != -10)) :
            c.execute("INSERT INTO avbs (pista, race,  dog_a, dog_b, odd_a, odd_b, pontos_a, pontos_b, vencedor, resultado, nome_do_arquivo_origem) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", (avb[1],avb[2],avb[3],avb[4],avb[5],avb[6],avb[7],avb[8],avb[9],avb[10],avb[11]))
            conn.commit()

def buscar_avbs(c):
    c.execute("SELECT * FROM avbs")
    return c.fetchall()

def converter_formato_data(data_str):
    # Converter a string de data para um objeto datetime
    data = datetime.strptime(data_str, "%d-%m-%Y")

    # Obter o dia, mês e ano da data
    dia = data.day
    mes = data.strftime("%b")  # Obter o mês em formato abreviado
    ano = data.strftime("%y")  # Obter o ano em formato abreviado

    # Gerar a string no formato desejado
    data_convertida = f"{dia}{mes}{ano}"

    if len(data_convertida) < 7:
        data_convertida = f"0{data_convertida}"

    return data_convertida

def update():
    conn = sqlite3.connect('all_avbs_filt.sqlite3')
    c = conn.cursor()
    all_avbs = buscar_avbs(c)

    driver = webdriver.Chrome()
    url ='https://greyhoundbet.racingpost.com/#results-list'
    driver.get(url)
    time.sleep(2)
    pyautogui.click(654,555)
    time.sleep(1)
    pyautogui.click(634,709)
    time.sleep(1)

    erros = pickle.load(open('erros.sav', 'rb'))

    last = pickle.load(open('last.sav', 'rb'))
    last = last - 19
    all_avbs = all_avbs[last:]

    for avb in all_avbs:

        pyautogui.click(732,255)
        time.sleep(0.1)
        pyautogui.typewrite(avb[3])
        pyautogui.press('enter')
        time.sleep(1.5)
        dog = driver.find_elements(By.CLASS_NAME,"details-col1")
        if len(dog) > 0:
            dog[0].click()

        elif len(dog) == 0:
            if len(avb[3]) > 3:
                pyautogui.click(307,195)
                time.sleep(1.5)
                pyautogui.click(732,255)
                time.sleep(0.1)
                pyautogui.typewrite(avb[4])
                pyautogui.press('enter')
                time.sleep(1.5)
                dog = driver.find_elements(By.CLASS_NAME,"details-col1")
                if len(dog) > 0:
                    dog[0].click()
            else:
                pyautogui.click(732,255)
                pyautogui.press('backspace')
                pyautogui.press('backspace')
                pyautogui.press('backspace')
                time.sleep(1.5)
                pyautogui.typewrite(avb[4])
                pyautogui.press('enter')
                time.sleep(1.5)
                dog = driver.find_elements(By.CLASS_NAME,"details-col1")
                if len(dog) > 0:
                    dog[0].click()




        # pyautogui.click(306,374)
        time.sleep(2)

        data = converter_formato_data(avb[11])
        try:
            elementos = driver.find_elements(By.TAG_NAME,"a")

            elementos_filtrados = [elemento for elemento in elementos if data in elemento.text]

            if len(elementos_filtrados) > 0:
                elementos_filtrados[0].click()
                time.sleep(3)
            elif len(elementos_filtrados) == 0:
                pyautogui.click(307,195)
                time.sleep(1.5)
                dog = driver.find_elements(By.CLASS_NAME,"details-col1")
                if len(dog) > 0:
                    dog[1].click()
                time.sleep(2)

                elementos = driver.find_elements(By.TAG_NAME,"a")

                elementos_filtrados = [elemento for elemento in elementos if data in elemento.text]

                if len(elementos_filtrados) > 0:
                    elementos_filtrados[0].click()
                time.sleep(3)

        except Exception:
            pyautogui.click(307,195)
            time.sleep(1.5)
            dog = driver.find_elements(By.CLASS_NAME,"details-col1")
            if len(dog) > 0:
                dog[1].click()
            time.sleep(2)

            elementos = driver.find_elements(By.TAG_NAME,"a")

            elementos_filtrados = [elemento for elemento in elementos if data in elemento.text]

            if len(elementos_filtrados) > 0:
                elementos_filtrados[0].click()
                time.sleep(3)

            elif len(elementos_filtrados) == 0:
                pyautogui.click(307,195)
                time.sleep(1.5)
                pyautogui.click(307,195)
                time.sleep(1.5)
                pyautogui.click(732,255)
                time.sleep(0.1)
                pyautogui.typewrite(avb[4])
                pyautogui.press('enter')
                time.sleep(1.5)
                dog = driver.find_elements(By.CLASS_NAME,"details-col1")
                if len(dog) > 0:
                    dog[0].click()
                time.sleep(2)

                elementos = driver.find_elements(By.TAG_NAME,"a")

                elementos_filtrados = [elemento for elemento in elementos if data in elemento.text]

                if len(elementos_filtrados) > 0:
                    elementos_filtrados[0].click()
                    time.sleep(3)


        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        dogs = soup.find_all('div', {'class': 'name'})
        n_nomes = []
        time.sleep(0.5)


        for i in range(0, len(dogs)):
            n = dogs[i].get_text().strip()
            n = re.sub(r'\(.*?\)', '', n).strip()
            # print(n)
            n_nomes.append(n)

        a = avb[3]
        b = avb[4]

        if (a in n_nomes) and (b in n_nomes):

            pos_a = n_nomes.index(a) + 1
            pos_b = n_nomes.index(b) + 1

            if pos_a < pos_b:
                c.execute("UPDATE avbs SET resultado = ? WHERE id = ?", (0, avb[0]))
                conn.commit()
                print(f"avb de id = {avb[0]} foi verificado")

                pickle.dump(avb[0], open('last.sav', 'wb'))
            elif pos_a > pos_b:
                c.execute("UPDATE avbs SET resultado = ? WHERE id = ?", (1, avb[0]))
                conn.commit()
                print(f"avb de id = {avb[0]} foi verificado")
                pickle.dump(avb[0], open('last.sav', 'wb'))

        else:
            print(f"avb de id = {avb[0]} contem erro")
            erros.append(avb[0])
            pickle.dump(erros, open('erros.sav', 'wb'))
            break

        pyautogui.click(307,195)
        time.sleep(1.5)
        pyautogui.click(307,195)
        time.sleep(1.5)
        pyautogui.click(307,195)
        time.sleep(1.5)

def purifica():
    conexao = sqlite3.connect('all_avbs_filt.sqlite3')
    cursor = conexao.cursor()
    all_avbs = buscar_avbs(cursor)

    conn = sqlite3.connect('all_avbs_100.sqlite3')
    c = conn.cursor()
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
                    resultado INTEGER,
                    nome_do_arquivo_origem
                 )''')
    conn.commit()

    for avb in all_avbs:
        if (avb[9] == "A") and (avb[10] == 0):
            c.execute("INSERT INTO avbs (pista, race,  dog_a, dog_b, odd_a, odd_b, pontos_a, pontos_b, vencedor, resultado, nome_do_arquivo_origem) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", (avb[1],avb[2],avb[3],avb[4],avb[5],avb[6],avb[7],avb[8],avb[9],avb[10],avb[11]))
            conn.commit()
        elif (avb[9] == "B") and (avb[10] == 1):
            c.execute("INSERT INTO avbs (pista, race,  dog_a, dog_b, odd_a, odd_b, pontos_a, pontos_b, vencedor, resultado, nome_do_arquivo_origem) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", (avb[1],avb[2],avb[3],avb[4],avb[5],avb[6],avb[7],avb[8],avb[9],avb[10],avb[11]))
            conn.commit()

def busca(data,a,b):
    conn = sqlite3.connect(f'banco_de_dados{data}.sqlite3')
    c = conn.cursor()

    c.execute("SELECT race_id FROM dogs WHERE nome = ?", (a,))
    race_id = c.fetchone()

    d_a, d_b, venc = func.compara_av(race_id,a, b)

    return d_a, d_b, venc


def cria_base():
    conn = sqlite3.connect('base_avbs.sqlite3')
    c = conn.cursor()

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

    all_avbs = buscar_avbs(c)

    for avb in all_avbs:
        d_a, d_b, venc = busca(avb[11], avb[3],avb[4])


# update()

# purifica()

a = "Anarchy"
b = "Fairyhill Run"
data = "01-04-2023"

d_a, d_b, venc = busca(data,a,b)

print(venc)







