import funções_
import sqlite3
import datetime
import f_busca



# funções_.cria_bd()

# funções_.ordena_races()

# dados = funções_.dados()
nome = "Tuftys Goofy"
race_id = f_busca.buscar_dog_rid(nome)
dog = f_busca.buscar_dog_nome(nome)
print(race_id)
print(dog)
