from bs4 import BeautifulSoup
from selenium import webdriver
import re
import classes

def coleta_pistas():
    driver = webdriver.Chrome()

    url ='https://greyhoundbet.racingpost.com/#meeting-list/view=meetings&r_date=2023-02-13'
    driver.get(url)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    pistas = soup.find_all('a', {'data-eventid': 'cards_meetings_click'})

    if len(pistas) == 0 :
        driver.quit()
        coleta_pistas()

    return(pistas)

# def coleta_races(link):
#     driver = webdriver.Chrome()

#     url =f'https://greyhoundbet.racingpost.com/{link}'
#     driver.get(url)

#     print(url)

#     html = driver.page_source

#     soup = BeautifulSoup(html, 'html.parser')

#     races = soup.find_all('a', {'data-eventid': 'cards_card'})

#     race_links = []

#     for i in range(1, len(races)):
#         race_link = races[i]['href']
#         race_links.append(race_link)

#     driver.quit()

#     return(race_links)


def coleta_races(pistas_links):
    pistas_races = []

    driver = webdriver.Chrome()

    for i in range(0, len(pistas_links)):

        link = pistas_links[i]

        url =f'https://greyhoundbet.racingpost.com/{link}'
        driver.get(url)

        html = driver.page_source

        soup = BeautifulSoup(html, 'html.parser')

        races = soup.find_all('a', {'data-eventid': 'cards_card'})

        race_links = []

        for j in range(0, len(races)):
            race_link = races[j]['href']
            form_r_link = re.sub('tab=card','tab=form', race_link)
            race_links.append(form_r_link)

        pistas_races.append(race_links)

        if len(pistas_races) == 0 :
            driver.quit()
            coleta_races()

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

def coleta_dogs_race(link):
    driver = webdriver.Chrome()

    url =f'https://greyhoundbet.racingpost.com/{link}'
    driver.get(url)

    html = driver.page_source

    soup = BeautifulSoup(html, 'html.parser')

    dogs = soup.find_all('div', {'class': 'runnerBlock'})

    if len(dogs) == 0 :
        driver.quit()
        coleta_dogs_race()

    return(dogs)

def coleta_hist_dog(dog):
    l_corridas = dog.find_all('tr', {})

    return(l_corridas)

def coleta_dados_corr(l_corrida):
    r_dados = l_corrida.find_all('td',{})


    return(r_dados)

def dados_corrida(r_dados):

    data = 1
    pista = r_dados[1].get_text().strip()
    dist = r_dados[2].get_text()
    distan = int(dist[:3])
    tra = r_dados[3].get_text()
    trap = int(tra[1])
    if (r_dados[4].get_text()) != '':
        split = float(r_dados[4].get_text())
    bends = r_dados[5].get_text().strip()
    peso = float(r_dados[12].get_text())
    cat = r_dados[14].get_text().strip()
    tempo = float(r_dados[15].get_text())
    po = r_dados[5].get_text()
    pos = int(po[0])

    print(pista)
    print(distan)
    print(trap)
    print(split)
    print(bends)
    print(peso)
    print(cat)
    print(tempo)
    print(pos)


