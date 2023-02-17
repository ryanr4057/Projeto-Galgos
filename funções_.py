from bs4 import BeautifulSoup
from selenium import webdriver
import re
import time
import sqlite3
from datetime import datetime
import f_bd

def coleta_pistas(): #retorna um array contendo os objetos pistas
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

    # def timer(seconds):
    #     time.sleep(seconds)
    #     driver.quit()

    link_das_pistas = (coleta_links(pistas))

    coleta_pista_nomes(pistas)

    return(link_das_pistas)

def coleta_races_aux(races):
    race_links = []
    # print(races[2])
    for i in range(0, len(races)):
        race_link = (races[i])['href']
        # print(race_link)
        form_r_link = re.sub('tab=card','tab=form', race_link)

        # print(form_r_link)
        race_links.append(form_r_link)

    return(race_links)

def coleta_races(pistas_links): #retorna um array com as races do link do parametro
    pistas_races = []

    driver = webdriver.Chrome()

    for i in range(0, 1):

        url =f'https://greyhoundbet.racingpost.com/{pistas_links[i]}'
        # print(url)

        driver.get(url)

        driver.refresh

        time.sleep(1.5)


        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        races = soup.find_all('a', {'data-eventid': 'cards_card'})

        ra = coleta_races_aux(races)

        # print(ra)

        pistas_races.append(ra)

        if pistas_races == [] :
            driver.quit()
            pistas_races = coleta_races(pistas_links)

        # def timer(seconds):
        #     time.sleep(seconds)
        #     driver.quit()

        # timer(0.7)


    driver.quit()

    return(pistas_races)

def coleta_links(pistas):
    links = []
    for i in range(0, len(pistas)):
        link = pistas[i]['href']
        links.append(link)

    return(links)

def coleta_pista_nomes(pistas):
    for i in range(0, len(pistas)):
        n_pista = pistas[i].get_text().strip()
        index = n_pista.find(' ')
        nome_pista = n_pista[:index ]
        f_bd.inserir_pista(nome_pista)


def coleta_dogs_race_aux(pista_races_links, pista_id): #recebe um array com os links das races de uma pista
    pista_dogs = []

    driver = webdriver.Chrome()

    for i in range(0, len(pista_races_links)):


        url = f'https://greyhoundbet.racingpost.com/{pista_races_links[i]}'
        # print(url)
        driver.get(url)

        driver.refresh()

        time.sleep(0.7)

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        time.sleep(0.1)

        tab = soup.find('div', {'id': 'sortContainer'})

        time.sleep(0.1)

        dogs = tab.find_all('div', {'class': 'runnerBlock'})

        nome = soup.find('span', {'class': 'titleColumn1'}).get_text().strip()
        txt = soup.find('span', {'class': 'titleColumn2'}).get_text().strip()
        horario = soup.find('h3', {'id': 'pagerCardTime'}).get_text().strip()
        categoria = txt[:3].strip()
        dis = txt[4:]
        distancia = int(dis[:4])



        pista_dogs.append(dogs)

        if dogs == [] :
            driver.quit()
            dogs = coleta_dogs_race_aux(pista_races_links)

        f_bd.inserir_race(nome, categoria, distancia, horario, pista_id)

    # def timer(seconds):
    #     time.sleep(seconds)
    #     driver.quit()

    # timer(5)


    return(pista_dogs)

def coleta_dogs_races(pistas_races): #recebe um array de arrays contendo os links das races das pistas
    pistas_dogs = []

    for i in range(0, len(pistas_races)):
        pista_dogs = coleta_dogs_race_aux(pistas_races[i], (i + 1))
        # print(pistas_races[i])
        pistas_dogs.append(pista_dogs)

    return(pistas_dogs)

def coleta_hist_dog_aux(dog, race_id):
    dog_dados = []
    d_nome = dog.find('strong', {}).get_text()
    t = dog.find('i', {})
    tr = (t)['class']
    trap = int((tr[1])[4])
    # print(trap)
    # print(d_nome)
    # print(race_id)
    t_corridas = dog.find('table', {'class': 'formGrid desktop'})
    # print(t_corridas)
    l_corridas = t_corridas.find_all('tr', {})
    # print(len(l_corridas))
    n = len(l_corridas) - 1

    f_bd.inserir_dog(d_nome, trap, race_id)

    for i in range(1, len(l_corridas)):
        l_corrida = l_corridas[i].find_all('td',{})
        dog_dados.append(dados_corrida_aux(l_corrida, d_nome))


    return(dog_dados)

def dados_corrida_aux(r_dados, d_nome):
    hist_dog = []
    race = []

    data = 1
    pista = r_dados[1].get_text().strip()
    distan = r_dados[2].get_text()
    dist = int(distan[:3])
    tra = r_dados[3].get_text()
    trap = int(tra[1])
    split = 0
    if (r_dados[4].get_text()) != '':
        split = float(r_dados[4].get_text())
    bends = r_dados[5].get_text().strip()
    peso = float(r_dados[12].get_text())
    cat = r_dados[14].get_text().strip()
    tempo = float(r_dados[15].get_text())
    pos = r_dados[6].get_text().strip()
    # if len(pos) > 0:
    #     po = int(pos[0])
    #     if (po == 1) or (po == 2) or (po == 3) or (po == 4) or (po == 5) or (po == 6):
    #         pos = po

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

    hist_dog = race

    dog_id = f_bd.buscar_id_pelo_nome(d_nome)

    f_bd.inserir_corrida(data, pista, dist, trap, split, bends, peso, cat, tempo, pos, dog_id)

    return(hist_dog)


    # print(pista)
    # print(distan)
    # print(trap)
    # print(split)
    # print(bends)
    # print(peso)
    # print(cat)
    # print(tempo)
    # print(pos)

def coleta_hist_aux1(r_dogs,race_id):
    race_dogs = []
    for i in range(0, len(r_dogs)):
        h_dog = coleta_hist_dog_aux(r_dogs[i], race_id)
        race_dogs.append(h_dog)
    return(race_dogs)

def coleta_hist_aux2(races_dogs):
    race_dogs = []
    for i in range(0, len(races_dogs)):
        h_dog = coleta_hist_aux1(races_dogs[i], (i+1))
        race_dogs.append(h_dog)
    return(race_dogs)

def coleta_hist(dogs):
    race_dogs = []

    for i in range(0, len(dogs)):
        h_dog = coleta_hist_aux2(dogs[i])
        race_dogs.append(h_dog)
    return(race_dogs)

def cria_bd():
    f_bd.criar_tabela_pistas()
    f_bd.criar_tabela_races()
    f_bd.criar_tabela_dogs()
    f_bd.criar_tabela_corrida()

