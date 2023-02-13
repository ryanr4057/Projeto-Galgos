from bs4 import BeautifulSoup
from selenium import webdriver
import funções

pistas = funções.coleta_pistas()

print(len(pistas))

links = []
nome_pistas = []

todas_races = []


for i in range(1, len(pistas)):
    link = pistas[i]['href']
    links.append(link)

    n_pista = pistas[1].get_text().strip()
    index = n_pista.find(' ')
    nome_pista = n_pista[:index ]
    nome_pistas.append(nome_pista)

print(links[0])


for i in range(1, len(links)):
    corr = funções.coleta_races(links[i])
    todas_races.append(corr)

