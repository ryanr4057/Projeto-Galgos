from bs4 import BeautifulSoup
from selenium import webdriver
import funções

driver = webdriver.Chrome()

url ='https://greyhoundbet.racingpost.com/#meeting-list/view=meetings&r_date=2023-02-12'
driver.get(url)

html = driver.page_source

soup = BeautifulSoup(html, 'html.parser')

pistas = soup.find_all('a', {'data-eventid': 'cards_meetings_click'})

links = []
nome_pistas = []

for i in range(1, len(pistas)):
    link = pistas[i]['href']
    links.append(link)

    n_pista = pistas[1].get_text().strip()
    index = n_pista.find(' ')
    nome_pista = n_pista[:index ]
    nome_pistas.append(nome_pista)

print(link[0])

driver.quit()


for i in range(1, len(links)):

    funções.coleta_races(links[i])
