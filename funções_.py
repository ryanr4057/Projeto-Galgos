from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import sqlite3
from datetime import datetime
import f_bd
import f_busca

#funções de coleta para pistas
def coleta_pistas():
    link_das_pistas = []
    driver = webdriver.Chrome()

    url ='https://greyhoundbet.racingpost.com/#meeting-list/view=meetings&r_date=2023-02-16'
    driver.get(url)
    time.sleep(1.5)

    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    pistas = soup.find_all('a', {'data-eventid': 'cards_meetings_click'})

    if pistas == []:
        driver.quit()
        coleta_pistas()

    link_das_pistas = (coleta_links(pistas))
    coleta_pista_nomes(pistas)

    return(link_das_pistas)

def coleta_pista_nomes(pistas):
    pistas_coletadas = []
    for i in range(0, len(pistas)):
        n_pista = pistas[i].get_text().strip()
        index = n_pista.find(' ')
        nome_pista = n_pista[:index ]
        for j in range(0, len(pistas_coletadas)):
            if nome_pista == pistas_coletadas[j]:
                nome_pista = f"{nome_pista} 2"

        f_bd.inserir_pista(nome_pista)
        pistas_coletadas.append(nome_pista)

#funções de coleta para races

def coleta_races_aux(races):
    race_links = []
    for i in range(0, len(races)):
        race_link = (races[i])['href']
        form_r_link = re.sub('tab=card','tab=form', race_link)
        race_links.append(form_r_link)

    return(race_links)

def coleta_races(pistas_links):
    pistas_races = []
    driver = webdriver.Chrome()

    for i in range(0, len(pistas_links)):

        url =f'https://greyhoundbet.racingpost.com/{pistas_links[i]}'
        driver.get(url)
        driver.refresh
        time.sleep(1.5)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        races = soup.find_all('a', {'data-eventid': 'cards_card'})
        ra = coleta_races_aux(races)
        pistas_races.append(ra)

        if pistas_races == [] :
            driver.quit()
            pistas_races = coleta_races(pistas_links)

    driver.quit()

    return(pistas_races)

def coleta_links(pistas):
    links = []
    for i in range(0, len(pistas)):
        link = pistas[i]['href']
        links.append(link)

    return(links)

#funções de coleta para cachorros

def coleta_dogs_race_aux(pista_races_links, pista_id):
    pista_dogs = []
    driver = webdriver.Chrome()

    for i in range(0, len(pista_races_links)):
        url = f'https://greyhoundbet.racingpost.com/{pista_races_links[i]}'
        driver.get(url)
        driver.refresh()
        time.sleep(0.7)

        html = driver.page_source
        soup = BeautifulSoup(html, 'html.parser')
        time.sleep(0.1)

        top = soup.find('div', {'class': 'racePager'})
        if top is None:
            print("top erro")
            tag = 'div'
            t1 = 'class'
            t2 = 'racePager'
            top = v_campo(soup,driver,tag,t1,t2)

        h = top.find('h3', {'id': 'pagerCardTime'})
        if h is None:
            print("horario erro")
            tag = 'h3'
            t1 = 'id'
            t2 = 'pagerCardTime'
            h = v_campo(top,driver,tag,t1,t2)
        horario = h.get_text().strip()

        p = soup.find('p', {'class': 'p2'})
        reser = 0
        pick = "POST PICK: 0-0-0"

        if p is None:
            res = soup.find_all('b', {'class': 'reserve'})
            if res is not None:
                reser = 1

            else:
                print("pick erro")
                tag = 'p'
                t1 = 'class'
                t2 = 'p2'
                p = v_campo(soup,driver,tag,t1,t2)

        if reser > 1:
            pick = "POST PICK: 0-0-0"
        if reser == 0:
            pick = p.get_text().strip()

        n = soup.find('span', {'class': 'titleColumn1'})
        if n is None:
            print("nome erro")
            tag = 'span'
            t1 = 'class'
            t2 = 'titleColumn1'
            n = v_campo(soup,driver,tag,t1,t2)
        nome = n.get_text().strip()

        t = soup.find('span', {'class': 'titleColumn2'})
        if t is None:
            print("txt erro")
            tag = 'span'
            t1 = 'class'
            t2 = 'titleColumn2'
            t = v_campo(soup,driver,tag,t1,t2)
        txt = t.get_text().strip()

        tab = soup.find('div', {'class': 'formTabContainer'})

        if tab is None:
            print(1)
            tag = 'div'
            t1 = 'class'
            t2 = 'formTabContainer'
            tab = v_campo(soup,driver,tag,t1,t2)

        dogs = tab.find_all('div', {'class': 'runnerBlock'})

        if dogs is None:
            print(2)
            tag = 'div'
            t1 = 'class'
            t2 = 'runnerBlock'
            dogs = v_campo_all(tab,driver,tag,t1,t2)

        pi = pick[10:]
        post_pick = pi[:6].strip()
        categoria = txt[:3].strip()
        dis = txt[5:]
        if len(txt) == 15:
            distancia = int(dis[:4])
        else:
            distancia = int(dis[:3])

        pista_dogs.append(dogs)

        if dogs == [] :
            driver.quit()
            dogs = coleta_dogs_race_aux(pista_races_links)

        f_bd.inserir_race(nome, categoria, distancia, horario, post_pick, pista_id)

    return(pista_dogs)

def coleta_dogs_races(pistas_races):
    pistas_dogs = []

    for i in range(0, len(pistas_races)):
        pista_dogs = coleta_dogs_race_aux(pistas_races[i], (i + 1))
        # print(pistas_races[i])
        pistas_dogs.append(pista_dogs)

    return(pistas_dogs)

#funções de coleta para historico

def coleta_hist_dog_aux(dog, race_id):
    dog_dados = []
    d_nome = dog.find('strong', {}).get_text()
    t = dog.find('i', {})
    tr = (t)['class']
    trap = int((tr[1])[4])
    t_corridas = dog.find('table', {'class': 'formGrid desktop'})
    l_corridas = t_corridas.find_all('tr', {})
    n = len(l_corridas) - 1

    te = dog.find('td', {'class': 'brt'}).get_text().strip()
    tex = te[5:].strip()

    if len(tex) < 5:
        tex = '00.00 A0 (00FFF00)'

    d_brt = tex[9:].strip()
    dat_brt = d_brt.replace("(", "")
    data_brt = dat_brt.replace(")", "")

    tempo_brt = float(tex[:5])

    f_bd.inserir_dog(d_nome, trap, data_brt, tempo_brt, race_id + 1)

    for i in range(1, len(l_corridas)):
        l_corrida = l_corridas[i].find_all('td',{})
        dog_dados.append(dados_corrida_aux(l_corrida, d_nome))

    return(dog_dados)

def dados_corrida_aux(r_dados, d_nome):
    hist_dog = []
    race = []
    split = 0
    vel_media = 0

    t = r_dados[0].find('a', {})
    if t is None:
        data = r_dados[0].get_text().strip()
    else:
        data = t.get_text().strip()

    pista = r_dados[1].get_text().strip()
    distan = r_dados[2].get_text()

    if len(distan) >= 4:
        dist = int(distan[:3])
    elif len(distan) == 3:
         dist = int(distan[:2])
    elif len(distan) == 2:
         dist = int(distan[:1])

    tra = r_dados[3].get_text()
    trap = int(tra[1])

    if (r_dados[4].get_text()) != '':
        split = float(r_dados[4].get_text())

    ben = r_dados[5].get_text().strip()
    bends = ben.replace("-", "")
    peso = float(r_dados[12].get_text())
    cat = r_dados[14].get_text().strip()
    tempo = float(r_dados[15].get_text())
    pos = r_dados[6].get_text().strip()
    remarks = r_dados[9].get_text().strip()
    if tempo > 0:
        vel_media = round((dist/tempo), 2)

    race.append(data)
    race.append(pista)
    race.append(dist)
    race.append(trap)
    race.append(split)
    race.append(bends)
    race.append(peso)
    race.append(cat)
    race.append(tempo)
    race.append(pos)
    race.append(remarks)

    hist_dog = race

    dog_id = f_bd.buscar_id_pelo_nome(d_nome)

    f_bd.inserir_corrida(data, pista, dist, trap, split, bends, peso, cat, tempo, vel_media, pos, remarks, dog_id)

    return(hist_dog)

def coleta_hist_aux1(r_dogs, count2):
    race_dogs = []

    for i in range(0, len(r_dogs)):
        h_dog = coleta_hist_dog_aux(r_dogs[i], count2 )
        race_dogs.append(h_dog)

    return(race_dogs)

def coleta_hist_aux2(races_dogs, count):
    race_dogs = []
    count2 = count

    for i in range(0, len(races_dogs)):
        h_dog = coleta_hist_aux1(races_dogs[i], count2)
        race_dogs.append(h_dog)
        count2 = count2 + 1

    return(race_dogs)

def coleta_hist(dogs):
    race_dogs = []
    count = 0

    for i in range(0, len(dogs)):
        if i != 0:
            count = count + len(dogs[i - 1])
        h_dog = coleta_hist_aux2(dogs[i], count)
        race_dogs.append(h_dog)

    return(race_dogs)

#funções de criação do banco de dados

def cria_bd():
    f_bd.criar_tabela_pistas()
    f_bd.criar_tabela_races()
    f_bd.criar_tabela_dogs()
    f_bd.criar_tabela_corrida()
    d = coleta_hist(coleta_dogs_races(coleta_races(coleta_pistas())))

def v_campo(array, driver, tag, t1, t2):
    driver.refresh()
    time.sleep(0.5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    array = soup.find(tag, {t1: t2})

    if array is None:
        v_campo(array, driver, tag, t1, t2)

    return(array)

def v_campo_all(array, driver, tag, t1, t2):
    driver.refresh()
    time.sleep(0.5)
    html = driver.page_source
    soup = BeautifulSoup(html, 'html.parser')
    array = soup.find_all(tag, {t1: t2})

    if array is None:
        v_campo_all(array, driver, tag, t1, t2)

    return(array)

def dados():
    d = coleta_hist(coleta_dogs_races(coleta_races(coleta_pistas())))

    return(d)

#funções de comparação

def compara(race_dist, dog_A, dog_B):
    d_dog_a = []
    d_dog_b = []

    dog_a = f_busca.buscar_dog_nome(dog_A)
    dog_b = f_busca.buscar_dog_nome(dog_B)

    hist_a = f_busca.buscar_corridas_por_dog_dist(dog_a[0], race_dist)
    hist_b = f_busca.buscar_corridas_por_dog_dist(dog_b[0], race_dist)

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
            po = int(hist_a[i][11][0])
        else:
            po = 0
        pos_a.append(po)
        vel_media_a.append(hist_a[i][10])

        bends = hist_a[i][6]
        rec_c = 0
        bend1 = 0
        split_fin = 0


        if len(bends) > 0:
            bend1 = int(bends[0])
            ultbend = int(bends[len(bends) - 1])
            rec_c = bend1 - ultbend
            split_fin = int(bends[len(bends) - 2]) - int(bends[len(bends) - 1])

        pos_1bend_a.append(bend1)
        rec_cansa_a.append(rec_c)
        splits_fin_a.append(split_fin)

    for i in range(0, len(hist_b)):
        splits_b.append(hist_b[i][5])
        tempos_b.append(hist_b[i][9])
        if len(hist_b[i][11]) > 2:
            po = int(hist_b[i][11][0])
        else:
            po = 0
        pos_b.append(po)
        vel_media_b.append(hist_b[i][10])

        bends = hist_b[i][6]
        rec_c = 0
        bend1 = 0

        if len(bends) > 0:
            bend1 = int(bends[0])
            ultbend = int(bends[len(bends) - 1])
            rec_c = bend1 - ultbend
            split_fin = int(bends[len(bends) - 2]) - int(bends[len(bends) - 1])

        pos_1bend_b.append(bend1)
        rec_cansa_b.append(rec_c)
        splits_fin_b.append(split_fin)

    nome_a = dog_a[1]
    trap_a = dog_a[2]
    peso_a = hist_a[0][7]
    m_split_a = calcula_media(splits_a)
    m_tempos_a = calcula_media(tempos_a)
    var_med_tempo_a = calcula_variacao_media(tempos_a)

    m_pos_a = calcula_media(pos_a)
    m_1bend_a = calcula_media(pos_1bend_a)
    m_vel_med_a = calcula_media(vel_media_a)
    m_rec_cansa_a = calcula_media(rec_cansa_a)
    m_split_fin_a = calcula_media(splits_fin_a)
    dias_sem_correr_a = abs(diferenca_em_dias(hist_a[0][1]))

    d_dog_a.append(trap_a)
    d_dog_a.append(nome_a)
    d_dog_a.append(dias_sem_correr_a)
    d_dog_a.append(peso_a )
    d_dog_a.append(m_split_a)
    d_dog_a.append(m_1bend_a)
    d_dog_a.append(m_pos_a)
    d_dog_a.append(m_tempos_a)
    d_dog_a.append(var_med_tempo_a)
    d_dog_a.append(m_vel_med_a)
    d_dog_a.append(m_rec_cansa_a)
    d_dog_a.append(m_split_fin_a )

    # print(d_dog_a)

    nome_b = dog_b[1]
    trap_b = dog_b[2]
    peso_b = hist_b[0][7]
    m_split_b = calcula_media(splits_b)
    m_tempos_b = calcula_media(tempos_b)
    var_med_tempo_b = calcula_variacao_media(tempos_b)
    m_pos_b = calcula_media(pos_b)
    m_1bend_b = calcula_media(pos_1bend_b)
    m_vel_med_b = calcula_media(vel_media_b)
    m_rec_cansa_b = calcula_media(rec_cansa_b)
    m_split_fin_b = calcula_media(splits_fin_b)
    dias_sem_correr_b = abs(diferenca_em_dias(hist_b[0][1]))

    d_dog_b.append(trap_b)
    d_dog_b.append(nome_b)
    d_dog_b.append(dias_sem_correr_b)
    d_dog_b.append(peso_b )
    d_dog_b.append(m_split_b)
    d_dog_b.append(m_1bend_b)
    d_dog_b.append(m_pos_b)
    d_dog_b.append(m_tempos_b)
    d_dog_b.append(var_med_tempo_b)
    d_dog_b.append(m_vel_med_b)
    d_dog_b.append(m_rec_cansa_b)
    d_dog_b.append(m_split_fin_b )

    # print(d_dog_b)

    venc = compara_dif(d_dog_a, d_dog_b)

    return(d_dog_a, d_dog_b, venc)

def calcula_media(array):
    total = 0
    for i in range(0, len(array)):
        total = total + array[i]
    media = round(total/len(array), 2)
    return(media)

def diferenca_em_dias(data_string):
    data_atual = datetime.now().date()
    data = datetime.strptime(data_string, '%d%b%y').date()
    diferenca = data - data_atual
    return diferenca.days

def calcula_variacao_media(arr):
    soma_variacoes = 0
    for i in range(1, len(arr)):
        variacao = abs(arr[i] - arr[i-1])
        soma_variacoes += variacao

    if (len(arr) - 1) > 0:
        variacao_media = soma_variacoes / (len(arr) - 1)
    else:
        variacao_media = 0

    return round(variacao_media, 2)


def compara_dif(d_dog_a, d_dog_b):
    a = d_dog_a
    b = d_dog_b
    tot_a = 0
    tot_b = 0
    venc = []

    #dias sem correr
    if a[2] > b[2]:
        venc.append(b[0])
        tot_b = tot_b + 1
    elif a[2] < b[2]:
        venc.append(a[0])
        tot_a = tot_a + 1

    else:
        venc.append(0)

    #peso
    if a[3] > b[3]:
        venc.append(a[0])
        tot_a = tot_a + 1

    elif a[3] < b[3]:
        venc.append(b[0])
        tot_b = tot_b + 1

    else:
        venc.append(0)

    #split
    if a[4] > b[4]:
        venc.append(b[0])
        tot_b = tot_b + 1

    elif a[4] < b[4]:
        venc.append(a[0])
        tot_a = tot_a + 1

    else:
        venc.append(0)

    #primeira bend
    if a[5] > b[5]:
        venc.append(b[0])
        tot_b = tot_b + 1

    elif a[5] < b[5]:
        venc.append(a[0])
        tot_a = tot_a + 1

    else:
        venc.append(0)

    #finalização
    if a[6] > b[6]:
        venc.append(b[0])
        tot_b = tot_b + 1

    elif a[6] < b[6]:
        venc.append(a[0])
        tot_a = tot_a + 1

    else:
        venc.append(0)

    #tempo
    if a[7] > b[7]:
        venc.append(b[0])
        tot_b = tot_b + 1

    elif a[7] < b[7]:
        venc.append(a[0])
        tot_a = tot_a + 1

    else:
        venc.append(0)

    #variação media de tempo
    if a[8] > b[8]:
        venc.append(b[0])
        tot_b = tot_b + 1

    elif a[8] < b[8]:
        venc.append(a[0])
        tot_a = tot_a + 1

    else:
        venc.append(0)

     #velocidade media
    if a[9] > b[9]:
        venc.append(a[0])
        tot_a = tot_a + 1

    elif a[9] < b[9]:
        venc.append(b[0])
        tot_b = tot_b + 1

    else:
        venc.append(0)

     #recupera / cansa
    if a[10] > b[10]:
        venc.append(a[0])
        tot_a = tot_a + 1

    elif a[10] < b[10]:
        venc.append(b[0])
        tot_b = tot_b + 1

    else:
        venc.append(0)

       #split final
    if a[11] > b[11]:
        venc.append(a[0])
        tot_a = tot_a + 1
    elif a[11] < b[11]:
        venc.append(b[0])
    else:
        venc.append(0)

    venc.append(tot_a)
    venc.append(tot_b)

    # print(venc)
    return(venc)






