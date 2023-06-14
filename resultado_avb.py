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
# import f_busca as f
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

    d_a, d_b, venc, r_dist = compara_av(race_id,a, b, data)

    return d_a, d_b, venc ,r_dist

def cria_base():
    conn = sqlite3.connect('base_avbs_a.sqlite3')
    c = conn.cursor()

    conx = sqlite3.connect('all_avbs_filt.sqlite3')
    cx = conx.cursor()

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

    all_avbs = buscar_avbs(cx)

    for avb in all_avbs:
        d_a, d_b, venc, r_dist = busca(avb[11], avb[3],avb[4])
        c.execute("INSERT INTO dados (dist_race, trap_a, dias_sem_correr_a, peso_a, m_split_a, m_1bend_a, m_pos_a, m_tempos_a, var_med_tempo_a, m_vel_med_a, m_rec_cansa_a, m_split_fin_a , status_cat_a, brt_a, d_brt_a, pontos_a, trap_b, dias_sem_correr_b, peso_b, m_split_b, m_1bend_b, m_pos_b, m_tempos_b, var_med_tempo_b, m_vel_med_b, m_rec_cansa_b, m_split_fin_b , status_cat_b, brt_b, d_brt_b, pontos_b, vencedor) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ? )", (r_dist[0],d_a[0], d_a[2], d_a[3], d_a[4] ,d_a[5], d_a[6], d_a[7], d_a[8], d_a[9], d_a[10], d_a[11], d_a[12], d_a[13], d_a[14], venc[11], d_b[0], d_b[2], d_b[3], d_b[4] ,d_b[5], d_b[6], d_b[7], d_b[8], d_b[9], d_b[10], d_b[11], d_b[12], d_b[13],d_b[14], venc[12], avb[10]))
        conn.commit()

def compara_av(id_race, dog_A, dog_B, data):
    conn = sqlite3.connect(f'banco_de_dados{data}.sqlite3')
    c = conn.cursor()

    c.execute("SELECT distancia FROM races WHERE id = ?", (id_race))
    race_dist = c.fetchone()

    c.execute("SELECT categoria FROM races WHERE id = ?", (id_race))
    race_cat = c.fetchone()

    c.execute("SELECT post_pick FROM races WHERE id = ?", (id_race))
    pick = c.fetchone()

    d_dog_a = []
    d_dog_b = []

    c.execute("SELECT * FROM dogs WHERE nome = ?", (dog_A,))
    dog_a = c.fetchone()

    c.execute("SELECT * FROM dogs WHERE nome = ?", (dog_B,))
    dog_b = c.fetchone()

    brt_a = dog_a[4]
    brt_b = dog_b[4]

    d_brt_a = abs(func.diferenca_em_dias(dog_a[3]))
    d_brt_b = abs(func.diferenca_em_dias(dog_b[3]))

    hist_a = []
    hist_b = []

    c.execute("SELECT * FROM corrida WHERE dog_id = ?  AND distancia = ?", (dog_a[0], race_dist[0]))
    histo_a =  c.fetchall()

    c.execute("SELECT * FROM corrida WHERE dog_id = ?  AND distancia = ?", (dog_b[0], race_dist[0]))
    histo_b =  c.fetchall()

    for i in range(0, len(histo_a)):
        if histo_a[i][9] > 0:
            hist_a.append(histo_a[i])

    for i in range(0, len(histo_b)):
        if histo_b[i][9] > 0:
            hist_b.append(histo_b[i])

    if len(hist_a) > 5:
        hist_a = hist_a[:5]

    if len(hist_b) > 5:
        hist_b = hist_b[:5]


    splits_a = []
    tempos_a = []
    pos_a = []
    pos_1bend_a = []
    vel_media_a = []
    rec_cansa_a = []
    splits_fin_a = []


    splits_b = []
    tempos_b = []
    pos_b = []
    pos_1bend_b = []
    vel_media_b = []
    rec_cansa_b = []
    splits_fin_b = []


    for i in range(0, len(hist_a)):
        splits_a.append(hist_a[i][5])
        tempos_a.append(hist_a[i][9])
        if len(hist_a[i][11]) > 2:
            if hist_a[i][11][0] == '=':
                n_po = (hist_a[i][11]).replace("=", "").strip()
                po = int(n_po[0])
            else:
                po = int(hist_a[i][11][0])
        else:
            po = 6
        pos_a.append(po)
        vel_media_a.append(hist_a[i][10])

        bends = hist_a[i][6]
        rec_c = 0
        bend1 = 6
        split_fin = 0


        if len(bends) > 0:
            bend1 = int(bends[0])
            ultbend = int(bends[len(bends) - 1])
            rec_c = bend1 - po
            split_fin =( int(bends[len(bends) - 2]) - po )

        pos_1bend_a.append(bend1)
        rec_cansa_a.append(rec_c)
        splits_fin_a.append(split_fin)

    ult_tempo_a = ""
    if len(hist_a) >1:
        ult_tempo_a += f"{hist_a[0][9]},"
        ult_tempo_a += f"{hist_a[1][9]},"


    for i in range(0, len(hist_b)):
        splits_b.append(hist_b[i][5])
        if (hist_b[i][9]) != None:
            tempos_b.append(hist_b[i][9])
        if len(hist_b[i][11]) > 2:
            if hist_b[i][11][0] == '=':
                n_po = (hist_a[i][11]).replace("=", "").strip()
                po = int(n_po[0])
            else:
                po = int(hist_b[i][11][0])
        else:
            po = 6
        pos_b.append(po)
        vel_media_b.append(hist_b[i][10])

        bends = hist_b[i][6]
        rec_c = 0
        bend1 = 6

        if len(bends) > 0:
            bend1 = int(bends[0])
            ultbend = int(bends[len(bends) - 1])
            rec_c = bend1 - po
            split_fin = (int(bends[len(bends) - 2]) - po)
        else:
            split_fin = 0

        pos_1bend_b.append(bend1)
        rec_cansa_b.append(rec_c)
        splits_fin_b.append(split_fin)

    ult_tempo_b = ""
    if len(hist_b) >1:
        ult_tempo_b += f"{hist_b[0][9]},"
        ult_tempo_b += f"{hist_b[1][9]},"

    nome_a = dog_a[1]
    trap_a = dog_a[2]
    if len(hist_a) > 0:
        peso_a = hist_a[0][7]
    else:
        peso_a = 0

    if len(splits_a) >= 1:
        m_split_a = func.calcula_media_spl(splits_a)
    else:
        m_split_a = 20

    if len(tempos_a) >= 1:
        m_tempos_a = func.calcula_media(tempos_a)
    else:
        m_tempos_a = 50

    if len(tempos_a) >= 1:
        var_med_tempo_a = func.calcula_variacao_media(tempos_a)
    else:
        var_med_tempo_a = 5

    if len(pos_a) >= 1:
        m_pos_a = func.calcula_media(pos_a)
    else:
        m_pos_a = 6

    if len(pos_1bend_a) >= 1:
        m_1bend_a = func.calcula_media(pos_1bend_a)
    else:
        m_1bend_a = 6

    if len(vel_media_a) >= 1:
        m_vel_med_a = func.calcula_media(vel_media_a)
    else:
        m_vel_med_a = 0

    if len(rec_cansa_a) >= 1:
        m_rec_cansa_a = func.calcula_media(rec_cansa_a)
    else:
        m_rec_cansa_a = 0

    if len(splits_fin_a) >= 1:
        m_split_fin_a = func.calcula_media(splits_fin_a)

    else:
        m_split_fin_a = 0

    if len(hist_a) > 0:
        dias_sem_correr_a = abs(func.diferenca_em_dias(hist_a[0][1]))
    else:
        dias_sem_correr_a = 0

    # if len(hist_a) > 0:
    #     cat_ant_a = hist_a[0][8]
    # else:
    #     cat_ant_a = '0'
    #     status_cat_a = status_cat(cat_ant_a, race_cat)
    # else:
    #     status_cat_a = 3

    cats_a = []
    cat_ant_a = ''
    med_cat_a = 0

    if len(hist_a) > 0:
        for i in range(0, len(hist_a)):
            cats_a.append(hist_a[i][8])
            cat_ant_a = cat_ant_a + f"{hist_a[i][8]},"
        status_cat_a, med_cat_a = func.status_cat_med(cats_a, race_cat)
    else:
        status_cat_a = 3

    d_dog_a.append(trap_a)
    d_dog_a.append(nome_a)
    d_dog_a.append(dias_sem_correr_a)
    d_dog_a.append(peso_a)
    d_dog_a.append(m_split_a)
    d_dog_a.append(m_1bend_a)
    d_dog_a.append(m_pos_a)
    d_dog_a.append(m_tempos_a)
    d_dog_a.append(var_med_tempo_a)
    d_dog_a.append(m_vel_med_a)
    d_dog_a.append(m_rec_cansa_a)
    d_dog_a.append(m_split_fin_a )
    d_dog_a.append(status_cat_a)
    d_dog_a.append(brt_a)
    d_dog_a.append(d_brt_a)
    d_dog_a.append(len(hist_a))
    d_dog_a.append(cat_ant_a)
    d_dog_a.append(med_cat_a)
    d_dog_a.append(ult_tempo_a)
    d_dog_a.append(pick[0])




    # print(d_dog_a)

    nome_b = dog_b[1]
    trap_b = dog_b[2]
    if len(hist_b) > 0:
        peso_b = hist_b[0][7]
    else:
        peso_b = 0

    if len(splits_b) >= 1:
        m_split_b = func.calcula_media_spl(splits_b)
    else:
        m_split_b = 10

    if len(tempos_b) >= 1:
        m_tempos_b = func.calcula_media(tempos_b)
    else:
        m_tempos_b = 50

    if len(tempos_b) >= 1:
        var_med_tempo_b = func.calcula_variacao_media(tempos_b)
    else:
        var_med_tempo_b = 5

    if len(pos_b) >= 1:
        m_pos_b = func.calcula_media(pos_b)
    else:
        m_pos_b = 6

    if len(pos_1bend_b) >= 1:
        m_1bend_b = func.calcula_media(pos_1bend_b)
    else:
        m_1bend_b = 6

    if len(vel_media_b) >= 1:
        m_vel_med_b = func.calcula_media(vel_media_b)
    else:
        m_vel_med_b = 0

    if len(rec_cansa_b) >= 1:
        m_rec_cansa_b = func.calcula_media(rec_cansa_b)
    else:
        m_rec_cansa_b = 0

    if len(splits_fin_b) >= 1:
        m_split_fin_b = func.calcula_media(splits_fin_b)

    else:
        m_split_fin_b = 0

    if len(hist_b) > 0:
        dias_sem_correr_b = abs(func.diferenca_em_dias(hist_b[0][1]))
    else:
        dias_sem_correr_b = 0

    # if len(hist_b) > 0:
    #     cat_ant_b = hist_b[0][8]
    # else:
    #     cat_ant_b = '0'


    #     status_cat_b = status_cat(cat_ant_b, race_cat)
    # else:
    #     status_cat_b = 3
    cats_b = []
    cat_ant_b = ''
    med_cat_b = 0

    if len(hist_b) > 0:
        for i in range(0, len(hist_b)):
            cats_b.append(hist_b[i][8])
            cat_ant_b = cat_ant_b + f"{hist_b[i][8]},"
        status_cat_b, med_cat_b = func.status_cat_med(cats_b, race_cat)
    else:
        status_cat_b = 3

    d_dog_b.append(trap_b)
    d_dog_b.append(nome_b)
    d_dog_b.append(dias_sem_correr_b)
    d_dog_b.append(peso_b)
    d_dog_b.append(m_split_b)
    d_dog_b.append(m_1bend_b)
    d_dog_b.append(m_pos_b)
    d_dog_b.append(m_tempos_b)
    d_dog_b.append(var_med_tempo_b)
    d_dog_b.append(m_vel_med_b)
    d_dog_b.append(m_rec_cansa_b)
    d_dog_b.append(m_split_fin_b )
    d_dog_b.append(status_cat_b )
    d_dog_b.append(brt_b)
    d_dog_b.append(d_brt_b)
    d_dog_b.append(len(hist_b))
    d_dog_b.append(cat_ant_b)
    d_dog_b.append(med_cat_b)
    d_dog_b.append(ult_tempo_b)



    # print(d_dog_b)

    venc = compara_dif_av(d_dog_a, d_dog_b, race_dist[0])

    return(d_dog_a, d_dog_b, venc, race_dist)

def compara_dif_av(d_dog_a, d_dog_b, race_dist):
    a = d_dog_a
    b = d_dog_b
    tot_a = 0
    tot_b = 0
    venc = []
    metodo_a = ''
    metodo_b = ''



    #dias sem correr
    if a[2] > b[2]:
        venc.append(b[0])

    elif a[2] < b[2]:
        venc.append(a[0])
    else:
        venc.append(0)

    if a[2] > 25:
        tot_a = tot_a - 0.5
    if b[2] > 25:
        tot_b = tot_b - 0.5

    #peso
    if a[3] > b[3]:
        venc.append(a[0])
    elif a[3] < b[3]:
        venc.append(b[0])
    else:
        venc.append(0)

    if a[3] > 30:
        tot_a = tot_a + 0.5
    elif a[3] < 26:
        tot_a = tot_a - 0.5


    if b[3] > 30:
        tot_b = tot_b + 0.5
    elif b[3] < 26:
        tot_b = tot_b - 0.5

    #split
    if a[4] > b[4]:
        venc.append(b[0])
        if (a[4] - b[4]) > 0.2 :
            tot_b = tot_b + 0.5
        elif (a[4] - b[4]) > 0.15 :
            tot_b = tot_b + 0.25
        elif (a[4] - b[4]) > 0.1 :
            tot_b = tot_b + 0.1

    elif a[4] < b[4]:
        venc.append(a[0])
        if (b[4] - a[4]) > 0.2 :
            tot_a = tot_a + 0.5
        elif (b[4] - a[4]) > 0.15 :
            tot_a = tot_a + .25
        elif (b[4] - a[4]) > 0.1 :
            tot_a = tot_a + 0.1

    else:
        venc.append(0)

    #primeira bend
    if a[5] > b[5]:
        venc.append(b[0])
        if (a[5] - b[5]) > 1.25 :
            tot_b = tot_b + 0.5
        elif (a[5] - b[5]) > 0.75 :
            tot_b = tot_b + 0.25
        elif (a[5] - b[5]) > 0.5 :
            tot_b = tot_b + 0.1

    elif a[5] < b[5]:
        venc.append(a[0])
        if (b[5] - a[5]) > 1.25 :
            tot_a = tot_a + 0.5
        elif (b[5] - a[5]) > 0.75 :
            tot_a = tot_a + 0.25
        elif (b[5] - a[5]) > 0.5 :
            tot_a = tot_a + 0.1

    else:
        venc.append(0)

    #finalização
    if a[6] > b[6]:
        venc.append(b[0])
        if (a[6] - b[6]) > 1.25 :
            tot_b = tot_b + 1
        elif (a[6] - b[6]) > 0.75 :
            tot_b = tot_b + 0.5
        elif (a[6] - b[6]) > 0.5 :
            tot_b = tot_b + 0.25

    elif a[6] < b[6]:
        venc.append(a[0])
        if (b[6] - a[6]) > 1.25 :
            tot_a = tot_a + 1
        elif (b[6] - a[6]) > 0.75 :
            tot_a = tot_a + 0.5
        elif (b[6] - a[6]) > 0.5 :
            tot_a = tot_a + 0.25

    else:
        venc.append(0)

    #tempo
    if a[7] > b[7]:
        venc.append(b[0])
        # if (a[7] - b[7]) > 0.15 :
        #     tot_b = tot_b + 3
        # elif (a[7] - b[7]) > 0.1 :
        #     tot_b = tot_b + 2
        # elif (a[7] - b[7]) > 0.05 :
        #     tot_b = tot_b + 1

    elif a[7] < b[7]:
        venc.append(a[0])
        # if (b[7] - a[7]) > 0.15 :
        #     tot_a = tot_a + 3
        # elif (b[7] - a[7]) > 0.1 :
        #     tot_a = tot_a + 2
        # elif (b[7] - a[7]) > 0.05 :
        #     tot_a = tot_a + 1

    else:
        venc.append(0)

    #variação media de tempo
    if a[8] > b[8]:
        venc.append(b[0])
    elif a[8] < b[8]:
        venc.append(a[0])
    else:
        venc.append(0)

    if b[8] < 0.1:
        tot_b = tot_b + 0.5
    elif b[8] < 0.3:
        tot_b = tot_b + 0.25
    elif b[8] < 0.5:
        tot_b = tot_b + 0.1

    if a[8] < 0.1:
        tot_a = tot_a + 0.5
    elif a[8] < 0.3:
        tot_a = tot_a + 0.25
    elif a[8] < 0.5:
        tot_a = tot_a + 0.1

     #velocidade media
    if a[9] > b[9]:
        venc.append(a[0])
        # if (a[9] - b[9]) > 0.2 :
        #     tot_a = tot_a + 3
        # elif (a[9] - b[9]) > 0.15 :
        #     tot_a = tot_a + 2
        # elif (a[9] - b[9]) > 0.1 :
        #     tot_a = tot_a + 1

    elif a[9] < b[9]:
        venc.append(b[0])
        # if (b[9] - a[9]) > 0.2 :
        #     tot_b = tot_b + 3
        # elif (b[9] - a[9]) > 0.15 :
        #     tot_b = tot_b + 2
        # elif (b[9] - a[9]) > 0.1 :
        #     tot_b = tot_b + 1

    else:
        venc.append(0)

     #recupera / cansa
    if a[10] > b[10]:
        venc.append(a[0])
        if (a[10] - b[10]) > 1 :
            tot_a = tot_a + 0.5
        elif (a[10] - b[10]) > 0.75 :
            tot_a = tot_a + 0.25
        elif (a[10] - b[10]) > 0.5 :
            tot_a = tot_a + 0.1

    elif a[10] < b[10]:
        venc.append(b[0])
        if (b[10] - a[10]) > 1 :
            tot_b = tot_b + 0.5
        elif (b[10] - a[10]) > 0.75 :
            tot_b = tot_b + 0.25
        elif (b[10] - a[10]) > 0.5 :
            tot_b = tot_b + 0.1

    else:
        venc.append(0)

       #split final
    if a[11] > b[11]:
        venc.append(a[0])
        # if (a[11] - b[11]) > 1 :
        #     tot_a = tot_a + 2
        # elif (a[11] - b[11]) > 0.75 :
        #     tot_a = tot_a + 1
        # elif (a[11] - b[11]) > 0.5 :
        #     tot_a = tot_a + 0.5

    elif a[11] < b[11]:
        venc.append(b[0])
        # if (b[11] - a[11]) > 1 :
        #     tot_b = tot_b + 2
        # elif (b[11] - a[11]) > 0.75 :
        #     tot_b = tot_b + 1
        # elif (b[11] - a[11]) > 0.5 :
        #     tot_b = tot_b + 0.5
    else:
        venc.append(0)

    if a[12] > b[12]:
        venc.append(a[0])
    elif a[12] < b[12]:
        venc.append(b[0])
    else:
        venc.append(0)

    # if a[12] == 2:
    #     tot_a = tot_a + 0.7
    # elif a[12] == 0:
    #     tot_a = tot_a - 1.5


    # if b[12] == 2:
    #     tot_b = tot_b + 0.7
    # elif b[12] == 0:
    #     tot_b = tot_b - 1.5

    if (race_dist >= 350) and (abs(a[7] - b[7]) > 0.1):
        # 1bend + recuperação
        if a[5] < b[5] and a[10] > b[10] and (a[12] >= b[12]) and (a[7] < b[7]):
            if b[5] - a[5] > 0.5 and a[10] - b[10] > 0.5:
                tot_a = tot_a + 6
                metodo_a = metodo_a + "1bend + recuperação + cat // "


        elif b[5] < a[5] and b[10] > a[10] and (b[12] >= a[12]) and (a[7] > b[7]):
            if a[5] - b[5] > 0.5 and b[10] - a[10] > 0.5:
                tot_b = tot_b + 6
                metodo_b = metodo_b + "1bend + recuperação + cat // "

        # recuperador vs cansa + categoria
        if a[10] > b[10] and a[6] < b[6] and (a[12] == 1 or a[12] == 2) and (a[7] < b[7]):
            if a[5] - a[10] < b[5] - b[10]:
                if abs((a[5] - a[10]) - (b[5] - b[10])) > 0.5:
                    tot_a = tot_a + 6
                    metodo_a = metodo_a + "rec cansa + cat. // "

        elif a[10] < b[10] and a[6] > b[6] and (b[12] == 1 or b[12] == 2) and (a[7] > b[7]):
            if a[5] - a[10] < b[5] - b[10]:
                if abs((a[5] - a[10]) - (b[5] - b[10])) > 0.5:
                    tot_b = tot_b + 6
                    metodo_b = metodo_b + "rec cansa + cat. // "

        # media de tempo + quantidade de races + variação media
        if a[7] < b[7] and abs(a[7] - b[7]) > 0.15 and a[15] >= 3 and a[8] < 0.2:
            tot_a = tot_a + 5
            metodo_a = metodo_a + "med. tempo + qtd races + var. media // "

        elif b[7] < a[7] and abs(a[7] - b[7]) > 0.15 and b[15] >= 3 and b[8] < 0.2:
            tot_b = tot_b + 5
            metodo_b = metodo_b + "med. tempo + qtd races + var. media // "

        #media de tempo + categoria
        elif a[7] < b[7] and (a[12] == 1 or a[12] == 2) and b[12] == 0:
            if abs(a[7] - b[7]) > 0.3:
                tot_a = tot_a + 4
                metodo_a = metodo_a + "med. tempo + cat // "

        elif a[7] > b[7] and (b[12] == 1 or b[12] == 2) and a[12] == 0:
            if abs(a[7] - b[7]) > 0.3:
                tot_b = tot_b + 4
                metodo_b = metodo_b + "med. tempo + cat // "

        #media de tempo + variação media
        elif (a[7] + a[8]) < (b[7] - b[8]):
            if(abs((a[7] + a[8]) - (b[7] - b[8])) > 0.1):
                tot_a = tot_a + 3
                metodo_a = metodo_a + "med. tempo + var. media // "

        elif (a[7] - a[8]) > (b[7] + b[8]):
            if(abs((a[7] - a[8]) - (b[7] + b[8])) > 0.1):
                tot_b = tot_b + 3
                metodo_b = metodo_b + "med. tempo + var. media // "

        #split + mantem
        if a[4] < b[4] and abs(a[4] - b[4]) > 0.15 and a[5] < 2.5 and a[10] >=0 and (a[7] < b[7]):
            tot_a = tot_a + 6
            metodo_a = metodo_a + "split + mantem // "

        elif a[4] > b[4] and abs(b[4] - a[4]) > 0.15 and b[5] < 2.5 and b[10] >=0 and (a[7] > b[7]):
            tot_b = tot_b + 6
            metodo_b = metodo_b + "split + mantem // "

        #brt tempo + data
        if (a[13] < b[13]) and abs(a[13] - b[13]) > 0.15 and (a[7] < b[7]):
            if (a[14] < b[14]) and a[14] < 17:
                tot_a = tot_a + 3
                metodo_a = metodo_a + "brt tempo + data // "

        elif (a[13] > b[13]) and abs(a[13] - b[13]) > 0.15 and (a[7] > b[7]):
            if (b[14] < a[14]) and b[14] < 17:
                tot_b = tot_b + 3
                metodo_b = metodo_b + "brt tempo + data // "


    #races curtas
    elif race_dist < 350:
        # 1 bend + media de tempo
        if a[5] < b[5] and abs(a[5] - b[5]) > 1:
            if a[7] < b[7] and abs(a[7] - b[7]) > 0.15:
                tot_a = tot_a + 4
                metodo_a = metodo_a + "1bend + recuperação // "

        elif b[5] < a[5] and abs(a[5] - b[5]) > 1:
            if b[7] < a[7] and abs(a[7] - b[7]) > 0.15:
                tot_b = tot_b + 4
                metodo_b = metodo_b + "1bend + recuperação // "


        #media de tempo + variação media
        if (a[7] + a[8]) < (b[7] - b[8]):
            if(abs((a[7] + a[8]) - (b[7] - b[8])) > 0.1):
                tot_a = tot_a + 4
                metodo_a = metodo_a + "med. tempo + var. media // "

        elif (a[7] + a[8]) > (b[7] - b[8]):
            if(abs((a[7] + a[8]) - (b[7] - b[8])) > 0.1):
                tot_b = tot_b + 4
                metodo_b = metodo_b + "med. tempo + var. media // "



    if a[15] <= 1:
        tot_a = -10
    if b[15] <= 1:
        tot_b = -10

    venc.append( round(tot_a, 2))
    venc.append(round(tot_b, 2))
    venc.append(metodo_a)
    venc.append(metodo_b)


    # print(venc)
    return(venc)


# update()

# purifica()

# a = "Anarchy"
# b = "Fairyhill Run"
# data = "01-04-2023"

# d_a, d_b, venc, r_dist = busca(data,a,b)

# print(r_dist)


cria_base()





