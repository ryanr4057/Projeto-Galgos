import teste2

op = 0

dados = []

while op < 3:

    op = int(input("1- carregar dados 2- imprimir 3- sair"))

    if op == 1:
        teste2.carregar_dados(dados)
    if op == 2:
        print(dados[0][0][0][0][0][0])


