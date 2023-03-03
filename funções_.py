from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import sqlite3
import datetime
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

        # n = soup.find('span', {'class': 'titleColumn1'})
        # if n is None:
        #     print("nome erro")
        #     tag = 'span'
        #     t1 = 'class'
        #     t2 = 'titleColumn1'
        #     n = v_campo(soup,driver,tag,t1,t2)
        # nome = n.get_text().strip()

        nome = f"Race {i + 1}"

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
    d_nome = dog.find('strong', {}).get_text().strip()
    d_nome = re.sub(r'\(.*?\)', '', d_nome)
    d_nome = d_nome.strip()

    t = dog.find('i', {})
    tr = (t)['class']
    trap = int((tr[1])[4])
    t_corridas = dog.find('table', {'class': 'formGrid desktop'})
    l_corridas = t_corridas.find_all('tr', {})
    n = len(l_corridas) - 1

    te = dog.find('td', {'class': 'brt'}).get_text().strip()
    tex = te[5:].strip()

    if len(tex) < 5:
        tex = '00.00 A12 (01jan20)'

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

def compara(id_race, dog_A, dog_B):
    race_dist = f_busca.buscar_race_dist(id_race)
    race_cat = f_busca.buscar_race_cat(id_race)
    d_dog_a = []
    d_dog_b = []

    dog_a = f_busca.buscar_dog_nome(dog_A)
    dog_b = f_busca.buscar_dog_nome(dog_B)

    hist_a = f_busca.buscar_corridas_por_dog_dist(dog_a[0], race_dist[0])
    hist_b = f_busca.buscar_corridas_por_dog_dist(dog_b[0], race_dist[0])

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

        pos_1bend_b.append(bend1)
        rec_cansa_b.append(rec_c)
        splits_fin_b.append(split_fin)

    nome_a = dog_a[1]
    trap_a = dog_a[2]
    if len(hist_a) > 0:
        peso_a = hist_a[0][7]
    else:
        peso_a = 0

    if len(splits_a) >= 1:
        m_split_a = calcula_media(splits_a)
    else:
        m_split_a = 20

    if len(tempos_a) >= 1:
        m_tempos_a = calcula_media(tempos_a)
    else:
        m_tempos_a = 50

    if len(tempos_a) >= 1:
        var_med_tempo_a = calcula_variacao_media(tempos_a)
    else:
        var_med_tempo_a = 5

    if len(pos_a) >= 1:
        m_pos_a = calcula_media(pos_a)
    else:
        m_pos_a = 6

    if len(pos_1bend_a) >= 1:
        m_1bend_a = calcula_media(pos_1bend_a)
    else:
        m_1bend_a = 6

    if len(vel_media_a) >= 1:
        m_vel_med_a = calcula_media(vel_media_a)
    else:
        m_vel_med_a = 0

    if len(rec_cansa_a) >= 1:
        m_rec_cansa_a = calcula_media(rec_cansa_a)
    else:
        m_rec_cansa_a = 0

    if len(splits_fin_a) >= 1:
        m_split_fin_a = calcula_media(splits_fin_a)

    else:
        m_split_fin_a = 0

    if len(hist_a) > 0:
        dias_sem_correr_a = abs(diferenca_em_dias(hist_a[0][1]))
    else:
        dias_sem_correr_a = 0

    if len(hist_a) > 0:
        cat_ant_a = hist_a[0][8]
        status_cat_a = status_cat(cat_ant_a, race_cat)
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

    # print(d_dog_a)

    nome_b = dog_b[1]
    trap_b = dog_b[2]
    if len(hist_b) > 0:
        peso_b = hist_b[0][7]
    else:
        peso_b = 0

    if len(splits_b) >= 1:
        m_split_b = calcula_media(splits_b)
    else:
        m_split_b = 10

    if len(tempos_b) >= 1:
        m_tempos_b = calcula_media(tempos_b)
    else:
        m_tempos_b = 50

    if len(tempos_b) >= 1:
        var_med_tempo_b = calcula_variacao_media(tempos_b)
    else:
        var_med_tempo_b = 5

    if len(pos_b) >= 1:
        m_pos_b = calcula_media(pos_b)
    else:
        m_pos_b = 6

    if len(pos_1bend_b) >= 1:
        m_1bend_b = calcula_media(pos_1bend_b)
    else:
        m_1bend_b = 6

    if len(vel_media_b) >= 1:
        m_vel_med_b = calcula_media(vel_media_b)
    else:
        m_vel_med_b = 0

    if len(rec_cansa_b) >= 1:
        m_rec_cansa_b = calcula_media(rec_cansa_b)
    else:
        m_rec_cansa_b = 0

    if len(splits_fin_b) >= 1:
        m_split_fin_b = calcula_media(splits_fin_b)

    else:
        m_split_fin_b = 0

    if len(hist_b) > 0:
        dias_sem_correr_b = abs(diferenca_em_dias(hist_b[0][1]))
    else:
        dias_sem_correr_b = 0

    if len(hist_b) > 0:
        cat_ant_b = hist_b[0][8]
        status_cat_b = status_cat(cat_ant_b, race_cat)
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

    # print(d_dog_b)

    venc = compara_dif_pond(d_dog_a, d_dog_b)

    return(d_dog_a, d_dog_b, venc)

def calcula_media(array):
    total = 0
    for i in range(0, len(array)):
        total = total + array[i]
    media = round(total/len(array), 2)
    return(media)

def diferenca_em_dias(data_string):
    data_atual = datetime.datetime.now().date()
    data = datetime.datetime.strptime(data_string, '%d%b%y').date()
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

def compara_dif_pond(d_dog_a, d_dog_b):
    a = d_dog_a
    b = d_dog_b
    tot_a = 0
    tot_b = 0
    venc = []

    #dias sem correr
    if a[2] > b[2]:
        venc.append(b[0])

    elif a[2] < b[2]:
        venc.append(a[0])
    else:
        venc.append(0)

    if a[2] < 5:
        tot_a = tot_a + 0.5
    elif a[2] < 10:
        tot_a = tot_a + 0.2
    elif a[2] < 15:
        tot_a = tot_a + 0.1

    if b[2] < 5:
        tot_b = tot_b + 0.5
    elif b[2] < 10:
        tot_b = tot_b + 0.2
    elif b[2] < 15:
        tot_b = tot_b + 0.1

    #peso
    if a[3] > b[3]:
        venc.append(a[0])
    elif a[3] < b[3]:
        venc.append(b[0])
    else:
        venc.append(0)

    if a[3] > 30:
        tot_a = tot_a + 1
    elif a[3] > 27.5:
        tot_a = tot_a + 0.75
    elif a[3] > 26:
        tot_a = tot_a + 0.25

    if b[3] > 30:
        tot_b = tot_b + 1
    elif b[3] > 27.5:
        tot_b = tot_b + 0.75
    elif b[3] > 26:
        tot_b = tot_b + 0.25

    #split
    if a[4] > b[4]:
        venc.append(b[0])
        if (a[4] - b[4]) > 0.2 :
            tot_b = tot_b + 3
        elif (a[4] - b[4]) > 0.15 :
            tot_b = tot_b + 2
        elif (a[4] - b[4]) > 0.1 :
            tot_b = tot_b + 1

    elif a[4] < b[4]:
        venc.append(a[0])
        if (b[4] - a[4]) > 0.2 :
            tot_a = tot_a + 3
        elif (b[4] - a[4]) > 0.15 :
            tot_a = tot_a + 2
        elif (b[4] - a[4]) > 0.01 :
            tot_a = tot_a + 1

    else:
        venc.append(0)

    #primeira bend
    if a[5] > b[5]:
        venc.append(b[0])
        if (a[5] - b[5]) > 1.25 :
            tot_b = tot_b + 2
        elif (a[5] - b[5]) > 0.75 :
            tot_b = tot_b + 1
        elif (a[5] - b[5]) > 0.5 :
            tot_b = tot_b + 0.5

    elif a[5] < b[5]:
        venc.append(a[0])
        if (b[5] - a[5]) > 1.25 :
            tot_a = tot_a + 2
        elif (b[5] - a[5]) > 0.75 :
            tot_a = tot_a + 1
        elif (b[5] - a[5]) > 0.5 :
            tot_a = tot_a + 0.5

    else:
        venc.append(0)

    #finalização
    if a[6] > b[6]:
        venc.append(b[0])
        if (a[6] - b[6]) > 1.25 :
            tot_b = tot_b + 2
        elif (a[6] - b[6]) > 0.75 :
            tot_b = tot_b + 1
        elif (a[6] - b[6]) > 0.5 :
            tot_b = tot_b + 0.5

    elif a[6] < b[6]:
        venc.append(a[0])
        if (b[6] - a[6]) > 1.25 :
            tot_a = tot_a + 2
        elif (b[6] - a[6]) > 0.75 :
            tot_a = tot_a + 1
        elif (b[6] - a[6]) > 0.5 :
            tot_a = tot_a + 0.5

    else:
        venc.append(0)

    #tempo
    if a[7] > b[7]:
        venc.append(b[0])
        if (a[7] - b[7]) > 0.15 :
            tot_b = tot_b + 3
        elif (a[7] - b[7]) > 0.1 :
            tot_b = tot_b + 2
        elif (a[7] - b[7]) > 0.05 :
            tot_b = tot_b + 1

    elif a[7] < b[7]:
        venc.append(a[0])
        if (b[7] - a[7]) > 0.15 :
            tot_a = tot_a + 3
        elif (b[7] - a[7]) > 0.1 :
            tot_a = tot_a + 2
        elif (b[7] - a[7]) > 0.05 :
            tot_a = tot_a + 1

    else:
        venc.append(0)

    #variação media de tempo
    if a[8] > b[8]:
        venc.append(b[0])
        if b[8] < 0.1:
            tot_b = tot_b + 2
        elif b[8] < 0.3:
            tot_b = tot_b + 1
        elif b[8] < 0.5:
            tot_b = tot_b + 0.5

    elif a[8] < b[8]:
        venc.append(a[0])
        if a[8] < 0.1:
            tot_a = tot_a + 2
        elif a[8] < 0.3:
            tot_a = tot_a + 1
        elif a[8] < 0.5:
            tot_a = tot_a + 0.5

    else:
        venc.append(0)

     #velocidade media
    if a[9] > b[9]:
        venc.append(a[0])
        if (a[9] - b[9]) > 0.2 :
            tot_a = tot_a + 3
        elif (a[9] - b[9]) > 0.15 :
            tot_a = tot_a + 2
        elif (a[9] - b[9]) > 0.1 :
            tot_a = tot_a + 1


    elif a[9] < b[9]:
        venc.append(b[0])
        if (b[9] - a[9]) > 0.2 :
            tot_b = tot_b + 3
        elif (b[9] - a[9]) > 0.15 :
            tot_b = tot_b + 2
        elif (b[9] - a[9]) > 0.1 :
            tot_b = tot_b + 1

    else:
        venc.append(0)

     #recupera / cansa
    if a[10] > b[10]:
        venc.append(a[0])
        if (a[10] - b[10]) > 1 :
            tot_a = tot_a + 3
        elif (a[10] - b[10]) > 0.75 :
            tot_a = tot_a + 2
        elif (a[10] - b[10]) > 0.5 :
            tot_a = tot_a + 1

    elif a[10] < b[10]:
        venc.append(b[0])
        if (b[10] - a[10]) > 1 :
            tot_b = tot_b + 3
        elif (b[10] - a[10]) > 0.75 :
            tot_b = tot_b + 2
        elif (b[10] - a[10]) > 0.5 :
            tot_b = tot_b + 1

    else:
        venc.append(0)

       #split final
    if a[11] > b[11]:
        venc.append(a[0])
        if (a[11] - b[11]) > 1 :
            tot_a = tot_a + 2
        elif (a[11] - b[11]) > 0.75 :
            tot_a = tot_a + 1
        elif (a[11] - b[11]) > 0.5 :
            tot_a = tot_a + 0.5

    elif a[11] < b[11]:
        venc.append(b[0])
        if (b[11] - a[11]) > 1 :
            tot_b = tot_b + 2
        elif (b[11] - a[11]) > 0.75 :
            tot_b = tot_b + 1
        elif (b[11] - a[11]) > 0.5 :
            tot_b = tot_b + 0.5
    else:
        venc.append(0)

    if a[12] > b[12]:
        venc.append(a[0])
    elif a[12] < b[12]:
        venc.append(b[0])
    else:
        venc.append(0)

    if a[12] == 2:
        tot_a = tot_a + 0.7
    elif a[12] == 0:
        tot_a = tot_a - 0.7


    if b[12] == 2:
        tot_b = tot_b + 0.7
    elif b[12] == 0:
        tot_b = tot_b - 0.7



    venc.append( round(tot_a, 2))
    venc.append(round(tot_b, 2))

    # print(venc)
    return(venc)

def ordena_races():
    horas=[]
    hs = f_busca.buscar_race_hor()
    for i in range(0, len(hs)):
        horas.append(hs[i][0])

    orded_races = sorted(horas, key=lambda hora: datetime.datetime.strptime(hora, "%H:%M").time())

    return(orded_races)

def proxima_hora( horas):

    hora_atual_3 = hora_fuso()

    horas_datetime = [datetime.datetime.combine(datetime.datetime.today().date(), datetime.datetime.strptime(h, '%H:%M').time()) for h in horas]

    horas_futuras = [h for h in horas_datetime if h > hora_atual_3]

    if len(horas_futuras) == 0:
        return None

    proxima_hora = min(horas_futuras)

    return proxima_hora.strftime('%H:%M')

def hora_fuso():
    hora_atual = datetime.datetime.now().time() # Obtém a hora atual do sistema
    hora_atual_datetime = datetime.datetime.combine(datetime.datetime.today(), hora_atual) # Converte a hora atual em um objeto datetime
    hora_atual_datetime += datetime.timedelta(hours=3) # Adiciona 3 horas ao horário atual
    hora_atual_3 = datetime.datetime.combine(datetime.datetime.today().date(), hora_atual_datetime.time())
    hora_12 = datetime.time(13, 0)
    d_hora_12 = datetime.datetime.combine(datetime.datetime.today().date(), hora_12)

    if hora_atual_3 < d_hora_12:
        data_hora = datetime.datetime.combine(datetime.datetime.today(), hora_12) # Usa a data atual com a hora 12:00
    else:
        data_hora = datetime.datetime.combine(datetime.datetime.today().date(), hora_12)

    if hora_atual_3 > data_hora:
        hora_atual_3 = hora_atual_3 - datetime.timedelta(hours=12)
    return hora_atual_3

def atribui_dados(id_race, d_a, d_b, valores, janela_comp ):
    dist = f_busca.buscar_race_dist(id_race)
    cat = f_busca.buscar_race_cat(id_race)
    pick = f_busca.buscar_race_pick(id_race)


    dog_A = d_a[4:]
    dog_B = d_b[4:]
    d_dogs_a, d_dogs_b, venc = compara(id_race, dog_A, dog_B)

    a = d_dogs_a
    b = d_dogs_b


    #dias sem correr
    if a[2] > b[2]:
        dsc_a_cor = '#FF0800'
        dsc_b_cor = '#00FF00'
    elif a[2] < b[2]:
        dsc_a_cor = '#00FF00'
        dsc_b_cor = '#FF0800'
    else:
        dsc_a_cor = 'white'
        dsc_b_cor = 'white'

    #peso
    if a[3] > b[3]:
        p_a_cor = '#00FF00'
        p_b_cor = '#FF0800'
    elif a[3] < b[3]:
        p_a_cor = '#FF0800'
        p_b_cor = '#00FF00'
    else:
        p_a_cor = 'white'
        p_b_cor = 'white'

    #split
    if a[4] > b[4]:
        spl_a_cor = '#FF0800'
        spl_b_cor = '#00FF00'
    elif a[4] < b[4]:
        spl_a_cor = '#00FF00'
        spl_b_cor = '#FF0800'
    else:
        spl_a_cor = 'white'
        spl_b_cor = 'white'

    #primeira bend
    if a[5] > b[5]:
        bnd1_a_cor = '#FF0800'
        bnd1_b_cor = '#00FF00'
    elif a[5] < b[5]:
        bnd1_a_cor = '#00FF00'
        bnd1_b_cor = '#FF0800'
    else:
        bnd1_a_cor = 'white'
        bnd1_b_cor = 'white'

    #finalização
    if a[6] > b[6]:
        pos_a_cor = '#FF0800'
        pos_b_cor = '#00FF00'
    elif a[6] < b[6]:
        pos_a_cor = '#00FF00'
        pos_b_cor = '#FF0800'
    else:
        pos_a_cor = 'white'
        pos_b_cor = 'white'

    #tempo
    if a[7] > b[7]:
        t_a_cor = '#FF0800'
        t_b_cor = '#00FF00'
    elif a[7] < b[7]:
        t_a_cor = '#00FF00'
        t_b_cor = '#FF0800'
    else:
        t_a_cor = 'white'
        t_b_cor = 'white'

    #variação media de tempo
    if a[8] > b[8]:
        vmt_a_cor = '#FF0800'
        vmt_b_cor = '#00FF00'
    elif a[8] < b[8]:
        vmt_a_cor = '#00FF00'
        vmt_b_cor = '#FF0800'
    else:
        vmt_a_cor = 'white'
        vmt_b_cor = 'white'

    #velocidade media
    if a[9] > b[9]:
        vm_a_cor = '#00FF00'
        vm_b_cor = '#FF0800'
    elif a[9] < b[9]:
        vm_a_cor = '#FF0800'
        vm_b_cor = '#00FF00'
    else:
        vm_a_cor = 'white'
        vm_b_cor = 'white'

    #recupera / cansa
    if a[10] > b[10]:
        rec_a_cor = '#00FF00'
        rec_b_cor = '#FF0800'
    elif a[10] < b[10]:
        rec_a_cor = '#FF0800'
        rec_b_cor = '#00FF00'
    else:
        rec_a_cor = 'white'
        rec_b_cor = 'white'

    #split final
    if a[11] > b[11]:
        spf_a_cor = '#00FF00'
        spf_b_cor = '#FF0800'
    elif a[11] < b[11]:
        spf_a_cor = '#FF0800'
        spf_b_cor = '#00FF00'
    else:
        spf_a_cor = 'white'
        spf_b_cor = 'white'

    #split final
    if a[12] > b[12]:
        stcat_a_cor = '#00FF00'
        stcat_b_cor = '#FF0800'
    elif a[12] < b[12]:
        stcat_a_cor = '#FF0800'
        stcat_b_cor = '#00FF00'
    else:
        stcat_a_cor = 'white'
        stcat_b_cor = 'white'

    janela_comp['nome_pista'].update(value=valores[0])
    janela_comp['dist_pista'].update(value=dist[0] )
    janela_comp['cat_pista'].update(value=cat[0] )
    janela_comp['post_pick'].update(value=pick[0] )

    cor_a = define_cor_trap_t(d_dogs_a)

    if d_dogs_a[12] == 2:
        stcat_a = 'DESCENDO'
    elif d_dogs_a[12] == 1:
        stcat_a = 'MANTENDO'
    elif d_dogs_a[12] == 0:
        stcat_a = 'SUBINDO'
    elif d_dogs_a[12] == 3:
        stcat_a = '---'

    if d_dogs_b[12] == 2:
        stcat_b = 'DESCENDO'
    elif d_dogs_b[12] == 1:
        stcat_b = 'MANTENDO'
    elif d_dogs_b[12] == 0:
        stcat_b = 'SUBINDO'
    elif d_dogs_b[12] == 3:
        stcat_b = '---'


    janela_comp['trap_a'].update(value=d_dogs_a[0], background_color= cor_a[0] )
    janela_comp['nome_a'].update(value=d_dogs_a[1])
    janela_comp['dscorrer_a'].update(value=d_dogs_a[2], text_color = dsc_a_cor)
    janela_comp['peso_a'].update(value=d_dogs_a[3], text_color = p_a_cor)
    janela_comp['split_a'].update(value=d_dogs_a[4], text_color =spl_a_cor)
    janela_comp['bend1_a'].update(value=d_dogs_a[5], text_color =bnd1_a_cor)
    janela_comp['pos_a'].update(value=d_dogs_a[6], text_color =pos_a_cor)
    janela_comp['tempo_a'].update(value=d_dogs_a[7], text_color =t_a_cor )
    janela_comp['vtemp_a'].update(value=d_dogs_a[8], text_color =vmt_a_cor)
    janela_comp['vmed_a'].update(value=d_dogs_a[9], text_color =vm_a_cor)
    janela_comp['rec_a'].update(value=d_dogs_a[10], text_color =rec_a_cor)
    janela_comp['spfin_a'].update(value=d_dogs_a[11], text_color =spf_a_cor)
    janela_comp['stcat_a'].update(value=stcat_a, text_color =stcat_a_cor)


    cor_b = define_cor_trap_t(d_dogs_b)

    janela_comp['trap_b'].update(value=d_dogs_b[0], background_color= cor_b[0])
    janela_comp['nome_b'].update(value=d_dogs_b[1])
    janela_comp['dscorrer_b'].update(value=d_dogs_b[2], text_color =dsc_b_cor)
    janela_comp['peso_b'].update(value=d_dogs_b[3], text_color = p_b_cor)
    janela_comp['split_b'].update(value=d_dogs_b[4], text_color =spl_b_cor)
    janela_comp['bend1_b'].update(value=d_dogs_b[5], text_color =bnd1_b_cor)
    janela_comp['pos_b'].update(value=d_dogs_b[6], text_color =pos_b_cor)
    janela_comp['tempo_b'].update(value=d_dogs_b[7], text_color =t_b_cor)
    janela_comp['vtemp_b'].update(value=d_dogs_b[8], text_color =vmt_b_cor)
    janela_comp['vmed_b'].update(value=d_dogs_b[9], text_color =vmt_b_cor)
    janela_comp['rec_b'].update(value=d_dogs_b[10], text_color =rec_b_cor)
    janela_comp['spfin_b'].update(value=d_dogs_b[11], text_color =spf_b_cor)
    janela_comp['stcat_b'].update(value=stcat_b, text_color =stcat_b_cor)


    janela_comp['dscorrer_d'].update(value= abs(d_dogs_a[2] - d_dogs_b[2] ))
    janela_comp['peso_d'].update(value= abs(round(d_dogs_a[3] - d_dogs_b[3], 2)))
    janela_comp['split_d'].update(value= abs(round(d_dogs_a[4] - d_dogs_b[4], 2)))
    janela_comp['bend1_d'].update(value= abs(round(d_dogs_a[5] - d_dogs_b[5], 2)))
    janela_comp['pos_d'].update(value= abs(round(d_dogs_a[6] - d_dogs_b[6], 2)))
    janela_comp['tempo_d'].update(value= abs(round(d_dogs_a[7] - d_dogs_b[7], 2)))
    janela_comp['vtemp_d'].update(value= abs(round(d_dogs_a[8] - d_dogs_b[8], 2)))
    janela_comp['vmed_d'].update(value= abs(round(d_dogs_a[9] - d_dogs_b[9], 2)))
    janela_comp['rec_d'].update(value= abs(round(d_dogs_a[10] - d_dogs_b[10], 2)))
    janela_comp['spfin_d'].update(value= abs(round(d_dogs_a[11] - d_dogs_b[11], 2)))

    cores = define_cor_trap(venc)

    janela_comp['dscorrer_v'].update(value=venc[0], background_color= cores[0])
    janela_comp['peso_v'].update(value=venc[1], background_color= cores[1])
    janela_comp['split_v'].update(value=venc[2], background_color= cores[2])
    janela_comp['bend1_v'].update(value=venc[3], background_color= cores[3])
    janela_comp['pos_v'].update(value=venc[4], background_color= cores[4])
    janela_comp['tempo_v'].update(value=venc[5], background_color= cores[5])
    janela_comp['vtemp_v'].update(value=venc[6], background_color= cores[6])
    janela_comp['vmed_v'].update(value=venc[7], background_color= cores[7])
    janela_comp['rec_v'].update(value=venc[8], background_color= cores[8])
    janela_comp['spfin_v'].update(value=venc[9], background_color= cores[9])
    janela_comp['tot_a'].update(value=venc[11], background_color= cor_a[0])
    janela_comp['tot_b'].update(value=venc[12], background_color= cor_b[0])

    if venc[11] > venc[12]:
        janela_comp['vencedor'].update(value=d_dogs_a[0], background_color= cor_a[0])
    elif venc[11] < venc[12]:
        janela_comp['vencedor'].update(value=d_dogs_b[0], background_color= cor_b[0])
    else:
        janela_comp['vencedor'].update(value='empate')


    a = f_busca.buscar_dog_id(dog_A)
    hist_a = f_busca.buscar_corridas_por_dog(a[0])
    for i in range(0, len(hist_a)):
        hist_a[i] = hist_a[i][1:]

    b = f_busca.buscar_dog_id(dog_B)
    hist_b = f_busca.buscar_corridas_por_dog(b[0])
    for i in range(0, len(hist_b)):
        hist_b[i] = hist_b[i][1:]
    # t_races_a = len(hist_a)
    # t_races_b = len(hist_b)

    janela_comp['hist_a'].update(values=hist_a)
    janela_comp['hist_b'].update(values=hist_b)

def define_cor_trap(venc):
    cores = []
    for i in range(0, len(venc)):
        if venc[i] == 1:
            cores.append('red')
        elif venc[i] == 2:
            cores.append('blue')
        elif venc[i] == 3:
            cores.append('#D3D3D3')
        elif venc[i] == 4:
            cores.append('#484D50')
        elif venc[i] == 5:
            cores.append('orange')
        elif venc[i] == 6:
            cores.append('gray')
        else:
            cores.append('black')
    return (cores)

def define_cor_trap_t(venc):
    cores = []

    if venc[0] == 1:
        cores.append('red')
    elif venc[0] == 2:
        cores.append('blue')
    elif venc[0] == 3:
        cores.append('#D3D3D3')
    elif venc[0] == 4:
        cores.append('#484D50')
    elif venc[0] == 5:
        cores.append('orange')
    elif venc[0] == 6:
        cores.append('gray')
    else:
        cores.append('black')
    return (cores)

def status_cat(cat_atual, cat_race):
    status = 3

    if cat_race[0][0] == "A" == cat_atual[0] :
        if int(cat_atual[1:]) < int(cat_race[0][1:]):
            status = 2
        elif int(cat_atual[1:]) == int(cat_race[0][1:]):
            status = 1
        elif int(cat_atual[1:]) > int(cat_race[0][1:]):
            status = 0

    elif cat_race[0][0] == "D" == cat_atual[0] :
        if int(cat_atual[1:]) < int(cat_race[0][1:]):
            status = 2
        elif int(cat_atual[1:]) == int(cat_race[0][1:]):
            status = 1
        elif int(cat_atual[1:]) > int(cat_race[0][1:]):
            status = 0

    elif cat_race[0][0] == "S" == cat_atual[0] :
        if int(cat_atual[1:]) < int(cat_race[0][1:]):
            status = 2
        elif int(cat_atual[1:]) == int(cat_race[0][1:]):
            status = 1
        elif int(cat_atual[1:]) > int(cat_race[0][1:]):
            status = 0

    elif cat_race[0][0] == "B" == cat_atual[0] :
        if int(cat_atual[1:]) < int(cat_race[0][1:]):
            status = 2
        elif int(cat_atual[1:]) == int(cat_race[0][1:]):
            status = 1
        elif int(cat_atual[1:]) > int(cat_race[0][1:]):
            status = 0


    elif cat_race[0][0] == "A" and cat_atual[0] == "O" :
        status = 2

    elif cat_race[0][0] == "O" and cat_atual[0] != "O" :
        status = 0

    elif cat_race[0][0] == "O" and cat_atual[0] == "O" :
        status = 1

    elif cat_atual[0][0] == "T":
        status = 0

    elif cat_atual[0][0] == "I":
        status = 0

    else:
        print(f'nao entrou na cat {cat_atual}')

    return(status)

def index_prox_race(id_pista):
    i_races = f_busca.buscar_races_por_pista_i(id_pista)
    races_h = f_busca.buscar_races_h_por_pista(id_pista)

    races_h_str = []
    for i in range(0, len(races_h)):
        races_h_str.append(races_h[i][0])

    p_race = proxima_hora(races_h_str)

    if(p_race) is None:
        p_race = races_h[0][0]

    if p_race[0] == '0':
        p_race = p_race[1:]

    id_p_race = f_busca.buscar_race_id_h(id_pista[0], p_race)

    for i in range(0, len(i_races)):
        if id_p_race == i_races[i]:
            index = i

    return index

# def comp_avançada(race_id, nome_a, nome_b):
#     race_dist = f_busca.buscar_race_dist(race_id)
#     race_cat = f_busca.buscar_race_cat(race_id)

#     dog_a = f_busca.buscar_dog_nome(nome_a)
#     dog_b = f_busca.buscar_dog_nome(nome_b)

#     hist_a = f_busca.buscar_corridas_por_dog_dist(dog_a[0], race_dist[0])
#     hist_b = f_busca.buscar_corridas_por_dog_dist(dog_b[0], race_dist[0])

# def point(hist):
#     corrid_points = 0
#     medias = []

#     data = []
#     pista = []
#     distancia = []
#     trap = []
#     split = []
#     bends = []
#     bends1 = []
#     peso = []
#     categoria = []
#     tempo = []
#     vel_media = []
#     posicao = []
#     remarks = []
#     rec_cansa = []
#     split_fin = []

#     for i in range(0, len(hist)):
#         data.append(hist[i][1])
#         pista.append(hist[i][2])
#         distancia.append(hist[i][3])
#         trap.append(hist[i][4])
#         split.append(hist[i][5])
#         bends.append(hist[i][6])
#         bends1.append(int(hist[i][6][0]))
#         peso.append(hist[i][7])
#         categoria.append(hist[i][8])
#         tempo.append(hist[i][9])
#         vel_media.append(hist[i][10])

#         pos = hist[i][11]
#         posicao.append(hist[i][11])
#         remarks.append(hist[i][12])

#         rec_cansa.append( int(hist[i][6][len(hist[i][6]) - 1])  )

#     m_split = calcula_media(split)
#     m_1bend = calcula_media(bends1)
#     m_tempo = calcula_media(tempo)
#     m_vel_media = calcula_media(vel_media)
#     var_media = calcula_variacao_media(tempo)

def compara_av(id_race, dog_A, dog_B):
    race_dist = f_busca.buscar_race_dist(id_race)
    race_cat = f_busca.buscar_race_cat(id_race)
    d_dog_a = []
    d_dog_b = []

    dog_a = f_busca.buscar_dog_nome(dog_A)
    dog_b = f_busca.buscar_dog_nome(dog_B)

    brt_a = dog_a[4]
    brt_b = dog_b[4]

    d_brt_a = abs(diferenca_em_dias(dog_a[3]))
    d_brt_b = abs(diferenca_em_dias(dog_b[3]))

    hist_a = f_busca.buscar_corridas_por_dog_dist(dog_a[0], race_dist[0])
    hist_b = f_busca.buscar_corridas_por_dog_dist(dog_b[0], race_dist[0])

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

    nome_a = dog_a[1]
    trap_a = dog_a[2]
    if len(hist_a) > 0:
        peso_a = hist_a[0][7]
    else:
        peso_a = 0

    if len(splits_a) >= 1:
        m_split_a = calcula_media(splits_a)
    else:
        m_split_a = 20

    if len(tempos_a) >= 1:
        m_tempos_a = calcula_media(tempos_a)
    else:
        m_tempos_a = 50

    if len(tempos_a) >= 1:
        var_med_tempo_a = calcula_variacao_media(tempos_a)
    else:
        var_med_tempo_a = 5

    if len(pos_a) >= 1:
        m_pos_a = calcula_media(pos_a)
    else:
        m_pos_a = 6

    if len(pos_1bend_a) >= 1:
        m_1bend_a = calcula_media(pos_1bend_a)
    else:
        m_1bend_a = 6

    if len(vel_media_a) >= 1:
        m_vel_med_a = calcula_media(vel_media_a)
    else:
        m_vel_med_a = 0

    if len(rec_cansa_a) >= 1:
        m_rec_cansa_a = calcula_media(rec_cansa_a)
    else:
        m_rec_cansa_a = 0

    if len(splits_fin_a) >= 1:
        m_split_fin_a = calcula_media(splits_fin_a)

    else:
        m_split_fin_a = 0

    if len(hist_a) > 0:
        dias_sem_correr_a = abs(diferenca_em_dias(hist_a[0][1]))
    else:
        dias_sem_correr_a = 0

    if len(hist_a) > 0:
        cat_ant_a = hist_a[0][8]
        status_cat_a = status_cat(cat_ant_a, race_cat)
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


    # print(d_dog_a)

    nome_b = dog_b[1]
    trap_b = dog_b[2]
    if len(hist_b) > 0:
        peso_b = hist_b[0][7]
    else:
        peso_b = 0

    if len(splits_b) >= 1:
        m_split_b = calcula_media(splits_b)
    else:
        m_split_b = 10

    if len(tempos_b) >= 1:
        m_tempos_b = calcula_media(tempos_b)
    else:
        m_tempos_b = 50

    if len(tempos_b) >= 1:
        var_med_tempo_b = calcula_variacao_media(tempos_b)
    else:
        var_med_tempo_b = 5

    if len(pos_b) >= 1:
        m_pos_b = calcula_media(pos_b)
    else:
        m_pos_b = 6

    if len(pos_1bend_b) >= 1:
        m_1bend_b = calcula_media(pos_1bend_b)
    else:
        m_1bend_b = 6

    if len(vel_media_b) >= 1:
        m_vel_med_b = calcula_media(vel_media_b)
    else:
        m_vel_med_b = 0

    if len(rec_cansa_b) >= 1:
        m_rec_cansa_b = calcula_media(rec_cansa_b)
    else:
        m_rec_cansa_b = 0

    if len(splits_fin_b) >= 1:
        m_split_fin_b = calcula_media(splits_fin_b)

    else:
        m_split_fin_b = 0

    if len(hist_b) > 0:
        dias_sem_correr_b = abs(diferenca_em_dias(hist_b[0][1]))
    else:
        dias_sem_correr_b = 0

    if len(hist_b) > 0:
        cat_ant_b = hist_b[0][8]
        status_cat_b = status_cat(cat_ant_b, race_cat)
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

    # print(d_dog_b)

    venc = compara_dif_av(d_dog_a, d_dog_b)

    return(d_dog_a, d_dog_b, venc)

def compara_dif_av(d_dog_a, d_dog_b):
    a = d_dog_a
    b = d_dog_b
    tot_a = 0
    tot_b = 0
    venc = []

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

    if a[12] == 2:
        tot_a = tot_a + 0.7
    elif a[12] == 0:
        tot_a = tot_a - 1.5


    if b[12] == 2:
        tot_b = tot_b + 0.7
    elif b[12] == 0:
        tot_b = tot_b - 1.5

    # 1bend + recuperação
    if a[5] > b[5] and a[10] > b[10]:
        if a[5] - b[5] > 0.5 and a[10] - b[10] > 0.5:
            tot_a = tot_a + 3

    elif b[5] > a[5] and b[10] > a[10]:
        if b[5] - a[5] > 0.5 and b[10] - a[10] > 0.5:
            tot_b = tot_b + 3


    # media de tempo + quantidade de races + variação media
    if a[7] > b[7] and a[15] >= 3 and a[8] < 0.2:
        tot_a = tot_a + 4

    elif b[7] > a[7] and b[15] >= 3 and b[8] < 0.2:
        tot_b = tot_b + 4

    # recuperador vs cansa + categoria
    if a[10] > b[10] and a[6] < b[6] and (a[12] == 1 or a[12] == 2):
        if a[5] + a[10] > b[5] + b[10]:
            if abs((a[5] + a[10]) - (b[5] + b[10])) > 0.5:
                tot_a = tot_a + 4

    elif a[10] < b[10] and a[6] > b[6] and (b[12] == 1 or b[12] == 2):
        if a[5] + a[10] < b[5] + b[10]:
            if abs((a[5] + a[10]) - (b[5] + b[10])) > 0.5:
                tot_b = tot_b + 4

    #media de tempo + categoria
    if a[7] > b[7] and (a[12] == 1 or a[12] == 2) and b[12] == 0:
        if abs(a[7] - b[7]) > 0.3:
            tot_a = tot_a + 3
    elif a[7] < b[7] and (b[12] == 1 or b[12] == 2) and a[12] == 0:
        if abs(a[7] - b[7]) > 0.3:
            tot_b = tot_b + 3

    if a[15] == 0:
        tot_a = 0
    if b[15] == 0:
        tot_b = 0

    venc.append( round(tot_a, 2))
    venc.append(round(tot_b, 2))

    # print(venc)
    return(venc)










