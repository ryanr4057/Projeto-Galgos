import PySimpleGUI as sg
import f_busca
import funções_ as fun
import datetime
import bot

pistas = f_busca.buscar_todas_pistas()


opcoes = []
for pista in pistas:
    opcoes.append(pista[0])


# Criando a janela principal
layout = [[sg.Text('Escolha a Pista:', background_color='black')],
          [sg.Combo(opcoes, default_value=opcoes[0], size=20)],
          [sg.Text('      ', background_color='black')],
          [sg.Text('      ', background_color='black')],
          [sg.Text('      ', background_color='black')],
          [sg.Text('      ', background_color='black')],
          [sg.Button('Selecionar Pista')]]

janela_principal = sg.Window('PISTAS', layout, size=(400, 200), background_color='black')

# Criando a segunda janela
layout2 = [[sg.Text('Escolha a Race:', background_color='black')],
           [sg.Combo([], key='-COMBO-', size=20)],
           [sg.Text('      ', background_color='black')],
           [sg.Text('      ', background_color='black')],
           [sg.Text('      ', background_color='black')],
           [sg.Text('      ', background_color='black')],
           [sg.Button('Voltar'), sg.Button('Selecionar Race') ]]

janela_secundaria = None

layout3 = [[sg.Text('Escolha o primeiro cachorro:', background_color='black')],
           [sg.Combo([], key='-COMBO-', size=20)],
           [sg.Text('Escolha o segundo cachorro:', background_color='black')],
           [sg.Combo([], key='-COMBO2-', size=20)],
           [sg.Text('      ', background_color='black')],
           [sg.Text('      ', background_color='black')],
           [sg.Button('Voltar'), sg.Button('Comparar')]]

janela_ter = None

layout4 = [[sg.Text(key='nome_pista', size= 11, background_color= 'black', justification= 'center'),sg.Text(key='dist_pista', size= 11, background_color= 'black', justification= 'center'),sg.Text(key='cat_pista', size= 11, background_color= 'black', justification= 'center'), sg.Text(key='post_pick', size= 11, background_color= 'black', justification= 'center')],
           [sg.Text('TRAP', size= 11,background_color= 'black', justification= 'center' ), sg.Text('NOME',background_color= 'black', size= 11, justification= 'center'), sg.Text('DIAS S/ CORRER',background_color= 'black', size= 11, justification= 'center'), sg.Text('PESO', background_color= 'black',size= 11, justification= 'center'), sg.Text('MED SPLIT',background_color= 'black', size= 11, justification= 'center'), sg.Text('MED 1 BEND', background_color= 'black', size= 11, justification= 'center'), sg.Text('MED POSIÇÃO', background_color= 'black', size= 11, justification= 'center'), sg.Text('MED TEMPOS', background_color= 'black', size= 11, justification= 'center'), sg.Text('V MED TEMPO', background_color= 'black', size= 11, justification= 'center'), sg.Text('VEL MEDIA', background_color= 'black', size= 11, justification= 'center'), sg.Text('REC/CANSA', background_color= 'black', size= 11, justification= 'center'), sg.Text('SPLIT FIN', background_color= 'black', size= 11, justification= 'center'), sg.Text('STATUS_CAT', background_color= 'black', size= 11, justification= 'center')  ],
           [sg.Text(key='trap_a', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='nome_a', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='dscorrer_a', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='peso_a', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='split_a', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='bend1_a', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='pos_a', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='tempo_a', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='vtemp_a', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='vmed_a', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='rec_a', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='spfin_a', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='stcat_a', background_color= 'black', size= 11, justification= 'center') ],
           [sg.Text(key='trap_b', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='nome_b', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='dscorrer_b', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='peso_b', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='split_b', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='bend1_b', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='pos_b', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='tempo_b', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='vtemp_b', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='vmed_b', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='rec_b', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='spfin_b', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='stcat_b', background_color= 'black', size= 11, justification= 'center')  ],
           [sg.Text('   ', background_color= 'black', size= 11, justification= 'center'), sg.Text('DIFERENÇA', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='dscorrer_d', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='peso_d', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='split_d', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='bend1_d', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='pos_d', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='tempo_d', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='vtemp_d', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='vmed_d', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='rec_d', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='spfin_d', background_color= 'black', size= 11, justification= 'center') ],
           [sg.Text('   ', background_color= 'black', size= 11, justification= 'center'), sg.Text('VENCEDOR', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='dscorrer_v', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='peso_v', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='split_v', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='bend1_v', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='pos_v', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='tempo_v', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='vtemp_v', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='vmed_v', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='rec_v', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='spfin_v', background_color= 'black', size= 11, justification= 'center'), sg.Text(key='stcat_v', background_color= 'black', size= 11, justification= 'center')  ],
           [sg.Text('   ', background_color= 'black', size= 11, justification= 'center')],
           [sg.Table(key= 'hist_a', headings=['DATA', 'PISTA', 'DIST', 'TRAP', 'SPLIT', 'BENDS', 'PESO', 'CAT', 'TEMPO', 'VEL MEDIA', 'POS', 'REMARKS'], max_col_width=18, auto_size_columns=True, justification='center', values= [], background_color= 'black'),
           sg.Table(key= 'hist_b', headings=['DATA', 'PISTA', 'DIST', 'TRAP', 'SPLIT', 'BENDS', 'PESO', 'CAT', 'TEMPO', 'VEL MEDIA', 'POS', 'REMARKS'], max_col_width=18, auto_size_columns=True, justification='center', values= [],  background_color= 'black')],
           [sg.Text('TOTAL: A x B',background_color= 'black', size= 11, justification= 'center'), sg.Text(key='tot_a',background_color= 'black', size= 11, justification= 'center'), sg.Text(key='tot_b',background_color= 'black', size= 11, justification= 'center'), sg.Text('VENCEDOR:',background_color= 'black', size= 11, justification= 'center'), sg.Text(key='vencedor',background_color= 'black', size= 11, justification= 'center')],

           [sg.Button('Voltar'), sg.Button('enviar no telegram')]]

janela_comp = None

# Loop para ler eventos da janela principal
while True:
    evento, valores = janela_principal.read()
    if evento == sg.WINDOW_CLOSED:
        break
    elif evento == 'Selecionar Pista':
        opcao_escolhida = valores[0]
        if janela_secundaria is None:
            janela_secundaria = sg.Window('RACES', layout2, size=(400, 200), background_color='black')
            janela_secundaria.Finalize()
        else:
            janela_secundaria.un_hide()
        janela_principal.hide()  # Escondendo a janela principal enquanto a janela secundária está aberta

        # Preenchendo as opções do campo select com o array passado pela janela principal
        id_pista = f_busca.buscar_pista_id(opcao_escolhida)

        races = f_busca.buscar_races_por_pista(id_pista)
        races_h = f_busca.buscar_races_h_por_pista(id_pista)

        opcoes = []
        for i in range(0, len(races)):
            # opcoes.append(race[0])
            opcoes.append(f"{races_h[i][0]} - ({races[i][0]})")


        janela_secundaria['-COMBO-'].update(values=opcoes, set_to_index=0)


    # Loop para ler eventos da janela secundária
    while janela_secundaria is not None:
        evento2, valores2 = janela_secundaria.read()
        if evento2 == sg.WINDOW_CLOSED or evento2 == 'Voltar':
            janela_principal.un_hide()  # Mostrando a janela principal novamente
            janela_secundaria.hide()
            break

        elif evento2 == 'Selecionar Race':
            opcao_escolhida1 = valores2['-COMBO-']
            if janela_ter is None:
                janela_ter = sg.Window('RACES', layout3, size=(400, 200), background_color='black')
                janela_ter.Finalize()
            else:
                janela_ter.un_hide()
            janela_secundaria.hide()

            op = opcao_escolhida1[7:].strip().replace("(","")
            o = op.replace(")", "")
            id_race = f_busca.buscar_race_id(id_pista[0], o)

            dogs = f_busca.buscar_dogs_por_race(id_race)
            trap_dogs = f_busca.buscar_dogs_por_race_trap(id_race)

            opcoes = []
            for i in range(0, len(dogs)):
                opcoes.append(f"{trap_dogs[i][0]} - {dogs[i][0]}")

            janela_ter['-COMBO-'].update(values=opcoes, set_to_index=0)
            janela_ter['-COMBO2-'].update(values=opcoes, set_to_index=1)

        while janela_ter is not None:
            evento3, valores3 = janela_ter.read()
            if evento3 == sg.WINDOW_CLOSED or evento3 == 'Voltar':
                janela_secundaria.un_hide()  # Mostrando a janela principal novamente
                janela_ter.hide()
                break

            elif evento3 == 'Comparar':
                if janela_comp is None:
                    janela_comp = sg.Window('A v B', layout4, background_color='black')
                    janela_comp.Finalize()
                else:
                    janela_comp.un_hide()
                janela_ter.hide()


                d_a = valores3['-COMBO-']
                d_b = valores3['-COMBO2-']

                dist = f_busca.buscar_race_dist(id_race)
                # cat = f_busca.buscar_race_cat(id_race)

                dog_A = d_a[4:]
                dog_B = d_b[4:]
                d_dogs_a, d_dogs_b, venc = fun.compara(id_race,  dog_A, dog_B)


                fun.atribui_dados(id_race, d_a, d_b, valores, janela_comp)


            while janela_comp is not None:
                evento4, valores4 = janela_comp.read()
                if evento4 == sg.WINDOW_CLOSED or evento4 == 'Voltar':
                    janela_ter.un_hide()  # Mostrando a janela principal novamente
                    janela_comp.hide()
                    break
                elif evento4 == 'enviar no telegram':
                    if venc[10] > venc[11]:
                        mensagem = f"{valores[0]}-{opcao_escolhida1} \n {d_dogs_a[0]}-{d_dogs_a[1]} VENCE {d_dogs_b[0]}-{d_dogs_b[1]}"
                    elif venc[10] < venc[11]:
                        mensagem = f"{valores[0]}-{opcao_escolhida1} \n {d_dogs_b[0]}-{d_dogs_b[1]} VENCE {d_dogs_a[0]}-{d_dogs_a[1]}"
                bot.mens_telegram(mensagem)





# Fechando as janelas
janela_principal.close()
if janela_secundaria is not None:
    janela_secundaria.close()
    if janela_ter is not None:
        janela_ter.close()
        if janela_comp is not None:
            janela_comp.close()


