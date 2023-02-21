import PySimpleGUI as sg
import f_busca
import funções_ as fun

pistas = f_busca.buscar_todas_pistas()

opcoes = []
for pista in pistas:
    opcoes.append(pista[0])


# Criando a janela principal
layout = [[sg.Text('Escolha a Pista:')],
          [sg.Combo(opcoes, default_value=opcoes[0], size=20)],
          [sg.Button('Selecionar Pista')]]

janela_principal = sg.Window('PISTAS', layout, size=(400, 200))

# Criando a segunda janela
layout2 = [[sg.Text('Escolha a Race:')],
           [sg.Combo([], key='-COMBO-', size=20)],
           [sg.Button('Selecionar Race'), sg.Button('Voltar')]]

janela_secundaria = None

layout3 = [[sg.Text('Escolha o primeiro cachorro:')],
           [sg.Combo([], key='-COMBO-', size=20)],
           [sg.Text('Escolha o segundo cachorro:')],
           [sg.Combo([], key='-COMBO2-', size=20)],
           [sg.Button('Comparar'), sg.Button('Voltar')]]

janela_ter = None

# Loop para ler eventos da janela principal
while True:
    evento, valores = janela_principal.read()
    if evento == sg.WINDOW_CLOSED:
        break
    elif evento == 'Selecionar Pista':
        opcao_escolhida = valores[0]
        if janela_secundaria is None:
            janela_secundaria = sg.Window('RACES', layout2, size=(400, 200))
            janela_secundaria.Finalize()
        else:
            janela_secundaria.un_hide()
        janela_principal.hide()  # Escondendo a janela principal enquanto a janela secundária está aberta

        # Preenchendo as opções do campo select com o array passado pela janela principal
        id_pista = f_busca.buscar_pista_id(opcao_escolhida)

        races = f_busca.buscar_races_por_pista(id_pista)

        opcoes = []
        for race in races:
            opcoes.append(race[0])

        janela_secundaria['-COMBO-'].update(values=opcoes)

    # Loop para ler eventos da janela secundária
    while janela_secundaria is not None:
        evento2, valores2 = janela_secundaria.read()
        if evento2 == sg.WINDOW_CLOSED or evento2 == 'Voltar':
            janela_principal.un_hide()  # Mostrando a janela principal novamente
            janela_secundaria.hide()
            break
        elif evento2 == 'Selecionar Race':
            opcao_escolhida = valores2['-COMBO-']
            if janela_ter is None:
                janela_ter = sg.Window('RACES', layout3, size=(400, 200))
                janela_ter.Finalize()
            else:
                janela_ter.un_hide()
            janela_secundaria.hide()

            id_race = f_busca.buscar_race_id(id_pista[0], opcao_escolhida)

            dogs = f_busca.buscar_dogs_por_race(id_race)

            opcoes = []
            for dog in dogs:
                opcoes.append(dog[0])

            janela_ter['-COMBO-'].update(values=opcoes)
            janela_ter['-COMBO2-'].update(values=opcoes)

        while janela_ter is not None:
            evento3, valores3 = janela_ter.read()
            if evento3 == sg.WINDOW_CLOSED or evento3 == 'Voltar':
                janela_secundaria.un_hide()  # Mostrando a janela principal novamente
                janela_ter.hide()
                break
            elif evento3 == 'Comparar':
                dist = f_busca.buscar_race_dist(id_race)
                dog_A = valores3['-COMBO-']
                dog_B = valores3['-COMBO2-']

                fun.compara(dist[0], dog_A, dog_B)


            # opcao_escolhida = valores2['-COMBO-']
            # sg.popup(f'Você escolheu a opção {opcao_escolhida} na segunda janela.')

# Fechando as janelas
janela_principal.close()
if janela_secundaria is not None:
    janela_secundaria.close()


# # Criando a janela principal
# layout = [[sg.Text('Escolha uma opção:')],
#           [sg.Combo(opcoes, default_value=opcoes[0])],
#           [sg.Button('Ok'), sg.Button('Mostrar outra janela')]]

# janela_principal = sg.Window('Janela principal', layout)

# # Criando a segunda janela
# layout = [[sg.Text('Escolha a corrida:')],
#             [sg.Combo(opcoes_r, default_value=opcoes_r[0])],
#             [sg.Button('Ok')]]

# janela_secundaria = None

# # Loop para ler eventos da janela principal
# while True:
#     evento, valores = janela_principal.read()
#     if evento == sg.WINDOW_CLOSED:
#         break
#     elif evento == 'Ok':
#         opcao_escolhida = valores[0]
#         sg.popup(f'Você escolheu a opção {opcao_escolhida}.')
#     elif evento == 'Mostrar outra janela':
#         if janela_secundaria is None:
#             janela_secundaria = sg.Window('Janela secundária', layout)
#         else:
#             janela_secundaria.un_hide()

#     # Loop para ler eventos da janela secundária
#     while janela_secundaria is not None:
#         evento2, valores2 = janela_secundaria.read()
#         if evento2 == sg.WINDOW_CLOSED or evento2 == 'Fechar':
#             janela_secundaria.hide()
#             break

# # Fechando as janelas
# janela_principal.close()
# if janela_secundaria is not None:
#     janela_secundaria.close()
