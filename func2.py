from bs4 import BeautifulSoup
from selenium import webdriver
import re
import classes
import time

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

# def coleta_races(pistas_links):
#     pistas_races = []

#     for i in range(0, len(pistas_links)):

#         link = pistas_links[i]

#         url =f'https://greyhoundbet.racingpost.com/{link}'

#         driver = webdriver.Chrome()
#         # print(url)
#         driver.get(url)

#         html = driver.page_source

#         soup = BeautifulSoup(html, 'html.parser')

#         races = soup.find_all('a', {'data-eventid': 'cards_card'})

#         pistas_races.append(coleta_races_aux(races))

#         if len(races) == 0 :
#             driver.quit()
#             pistas_races = coleta_races(pistas_links)

#         driver.quit()

#     return(pistas_races)

def coleta_races(pistas_links): #retorna um array com as races do link do parametro
    pistas_races = []

    driver = webdriver.Chrome()

    for i in range(0, len(pistas_links)):

        url =f'https://greyhoundbet.racingpost.com/{pistas_links[i]}'
        # print(url)

        driver.get(url)

        driver.refresh

        time.sleep(1.5)


        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        races = soup.find_all('a', {'data-eventid': 'cards_card'})

        ra = coleta_races_aux(races)

        print(ra)

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

def executa_coleta_races(pistas_links):
    pistas_races = []
    for i in range(0, 2):
        pistas_r = coleta_races(pistas_links[i])
        pistas_races.append(pistas_r)
    return(pistas_races)

def coleta_links(pistas):
    links = []
    for i in range(0, len(pistas)):
        link = pistas[i]['href']
        links.append(link)

    return(links)

def coleta_pista_nomes(pistas):
    nome_pistas = []

    for i in range(0, len(pistas)):
        n_pista = pistas[1].get_text().strip()
        index = n_pista.find(' ')
        nome_pista = n_pista[:index ]
        nome_pistas.append(nome_pista)
    return(nome_pistas)

def coleta_dogs_race_aux(pista_races_links): #recebe um array com os links das races de uma pista
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

        dogs = soup.find_all('div', {'class': 'runnerBlock'})

        pista_dogs.append(dogs)

        if dogs == [] :
            driver.quit()
            dogs = coleta_dogs_race_aux1(pista_races_links)

    # def timer(seconds):
    #     time.sleep(seconds)
    #     driver.quit()

    # timer(5)

    return(pista_dogs)

def coleta_dogs_race_aux2(pista_races):
    race_dogs = []

    for i in range(0, len(pista_races)):
        r_dogs = coleta_dogs_race_aux1(pista_races[i])
        # print(pista_races[i])
        race_dogs.append(r_dogs)
    return(race_dogs)

def coleta_dogs_races(pistas_races): #recebe um array de arrays contendo os links das races das pistas
    pistas_dogs = []

    for i in range(0, 1):
        pista_dogs = coleta_dogs_race_aux(pistas_races[i])
        # print(pistas_races[i])
        pistas_dogs.append(pista_dogs)

    return(pistas_dogs)

def coleta_hist_dog_aux(dog):
    dog_dados = []
    t_corridas = dog.find('table', {'class': 'formGrid desktop'})
    # print(t_corridas)
    l_corridas = t_corridas.find_all('tr', {})
    # print(len(l_corridas))
    n = len(l_corridas) - 1

    for i in range(1, len(l_corridas)):
        l_corrida = l_corridas[i].find_all('td',{})
        dog_dados.append(dados_corrida_aux(l_corrida))

    return(dog_dados)

def dados_corrida_aux(r_dados):
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
    if len(pos) > 0:
        po = int(pos[0])
        if (po == 1) or (po == 2) or (po == 3) or (po == 4) or (po == 5) or (po == 6):
            pos = po

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

def coleta_hist_aux1(r_dogs):
    race_dogs = []
    for i in range(0, len(r_dogs)):
        # print(r_dogs[i])
        h_dog = coleta_hist_dog_aux(r_dogs[i])
        race_dogs.append(h_dog)
    return(race_dogs)

def coleta_hist_aux2(races_dogs):
    race_dogs = []
    for i in range(0, len(races_dogs)):
        h_dog = coleta_hist_aux1(races_dogs[i])
        race_dogs.append(h_dog)
    return(race_dogs)

def coleta_hist_aux3(races_dogs):
    race_dogs = []
    for i in range(0, len(races_dogs)):
        h_dog = coleta_hist_aux2(races_dogs[i])
        race_dogs.append(h_dog)
    return(race_dogs)

def coleta_hist(p_races_dogs):
    race_dogs = []
    for i in range(0, len(p_races_dogs)):
        h_dog = coleta_hist_aux3(p_races_dogs[i])
        race_dogs.append(h_dog)
    return(race_dogs)

# def coleta_hist(pistas_dogs):
#     todos_dogs = []
#     for i in range(0, len(pistas_dogs)):
#         for j in range(0, len(pistas_dogs[i])):
#             for k in range(0, len(pistas_dogs[i][j])):
#                 for l in range(0, len(pistas_dogs[i][j][k])):
#                     dog = coleta_hist_dog_aux(pistas_dogs[i][j][k][l])
#                     todos_dogs[i][j][k][l].append(dog)

# def coleta_hist(pistas_dogs):
#     todos_dogs = []
#     for l in range(0, 1):
#         dog = coleta_hist_dog_aux(pistas_dogs[0][0][0][l])
#         todos_dogs[0][0][0].append(dog)


