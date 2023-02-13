from bs4 import BeautifulSoup
from selenium import webdriver
import funções

pistas = funções.coleta_pistas()

# print(len(pistas))

pistas_links = funções.coleta_links(pistas)

# print(len(pistas_links))

nomes_p = funções.coleta_pista_nomes(pistas)

# print(len(nomes_p))

pistas_races = funções.coleta_races(pistas_links)

# print(pistas_races[0][0])

dogs = funções.coleta_dogs_race(pistas_races[0][1])

print(len(dogs))

# print(dogs[0])

corridas = funções.coleta_hist_dog(dogs[0])

# print(len(corridas))

# print(corridas[0])

l_corrida = funções.coleta_dados_corr(corridas[3])

print(len(l_corrida))

funções.dados_corrida(l_corrida)
