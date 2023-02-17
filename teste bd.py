import funções_
import sqlite3
from datetime import datetime



funções_.cria_bd()

pistas_links = funções_.coleta_pistas()

# print(len(pistas_links))
# print("   ")
pistas_races = funções_.coleta_races(pistas_links)
# print(len(pistas_races))
# print("   ")

# for i in range(0, len(pistas_races)):
#     print(len(pistas_races[i]))

# print("   ")


dogs = funções_.coleta_dogs_races(pistas_races)

# for i in range(0, len(dogs)):
#     print("   ")
#     for j in range(0, len(dogs[i])):
#         print(len(dogs[i][j]))
#         print("   ")

# # print(len(dogs))


dog_dados = funções_.coleta_hist(dogs)

# # print(len(dog_dados))

# print(dog_dados)

# # print(dog_dados[0][1][1])
