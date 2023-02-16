from bs4 import BeautifulSoup
from selenium import webdriver
import funções

dados = []

pistas = funções.coleta_pistas()

print(len(pistas))
print(pistas)


# nomes_p = funções.coleta_pista_nomes(pistas)

# # print(len(nomes_p))

# pistas_races = funções.executa_coleta_races(pistas_links)

pistas_races = funções.coleta_races(pistas[0])

print(pistas_races)

# # print(pistas_races)


# # print(pistas_races[0][0])

dogs = funções.coleta_dogs_race_aux1(pistas_races[0])

print(dogs)

#     # print(dogs[0][0][0][0])

#     # print(len(dogs))
#     # corridas = funções.coleta_hist_dog(dogs[0])
#     # print(len(corridas))
#     # print(corridas[0])
#     # l_corrida = funções.coleta_dados_corr(corridas[3])
#     # print(len(l_corrida))
#     # funções.dados_corrida(l_corrida)

# todos_dogs = funções.coleta_hist(dogs)

#     # print (len(todos_dogs[0][0][0][0][0][0]))
#     # print (len(todos_dogs[0][0][0][0][0]))
#     # print (len(todos_dogs[0][0][0][0]))
#     # print (len(todos_dogs[0][0][0]))
#     # print (len(todos_dogs[0][0]))
#     # print (len(todos_dogs[0]))

#     # print(todos_dogs[0][0][0][0][0][0])

# dados = todos_dogs
