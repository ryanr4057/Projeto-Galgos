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

layout4 = [[sg.Text('TRAP', size= 11, justification= 'center' ), sg.Text('NOME', size= 11, justification= 'center'), sg.Text('DIAS S/ CORRER', size= 11, justification= 'center'), sg.Text('PESO', size= 11, justification= 'center'), sg.Text('MED SPLIT', size= 11, justification= 'center'), sg.Text('MED 1 BEND', size= 11, justification= 'center'), sg.Text('MED POSIÇÃO', size= 11, justification= 'center'), sg.Text('MED TEMPOS', size= 11, justification= 'center'), sg.Text('V MED TEMPO', size= 11, justification= 'center'), sg.Text('VEL MEDIA', size= 11, justification= 'center'), sg.Text('REC/CANSA', size= 11, justification= 'center'), sg.Text('SPLIT FIN', size= 11, justification= 'center') ],
           [sg.Text(key='trap_a', size= 11, justification= 'center'), sg.Text(key='nome_a', size= 11, justification= 'center'), sg.Text(key='dscorrer_a', size= 11, justification= 'center'), sg.Text(key='peso_a', size= 11, justification= 'center'), sg.Text(key='split_a', size= 11, justification= 'center'), sg.Text(key='bend1_a', size= 11, justification= 'center'), sg.Text(key='pos_a', size= 11, justification= 'center'), sg.Text(key='tempo_a', size= 11, justification= 'center'), sg.Text(key='vtemp_a', size= 11, justification= 'center'), sg.Text(key='vmed_a', size= 11, justification= 'center'), sg.Text(key='rec_a', size= 11, justification= 'center'), sg.Text(key='spfin_a', size= 11, justification= 'center') ],
           [sg.Text(key='trap_b', size= 11, justification= 'center'), sg.Text(key='nome_b', size= 11, justification= 'center'), sg.Text(key='dscorrer_b', size= 11, justification= 'center'), sg.Text(key='peso_b', size= 11, justification= 'center'), sg.Text(key='split_b', size= 11, justification= 'center'), sg.Text(key='bend1_b', size= 11, justification= 'center'), sg.Text(key='pos_b', size= 11, justification= 'center'), sg.Text(key='tempo_b', size= 11, justification= 'center'), sg.Text(key='vtemp_b', size= 11, justification= 'center'), sg.Text(key='vmed_b', size= 11, justification= 'center'), sg.Text(key='rec_b', size= 11, justification= 'center'), sg.Text(key='spfin_b', size= 11, justification= 'center') ],
           [sg.Text('   ', size= 11, justification= 'center'), sg.Text('DIFERENÇA', size= 11, justification= 'center'), sg.Text(key='dscorrer_d', size= 11, justification= 'center'), sg.Text(key='peso_d', size= 11, justification= 'center'), sg.Text(key='split_d', size= 11, justification= 'center'), sg.Text(key='bend1_d', size= 11, justification= 'center'), sg.Text(key='pos_d', size= 11, justification= 'center'), sg.Text(key='tempo_d', size= 11, justification= 'center'), sg.Text(key='vtemp_d', size= 11, justification= 'center'), sg.Text(key='vmed_d', size= 11, justification= 'center'), sg.Text(key='rec_d', size= 11, justification= 'center'), sg.Text(key='spfin_d', size= 11, justification= 'center') ],
           [sg.Text('   ', size= 11, justification= 'center'), sg.Text('VENCEDOR', size= 11, justification= 'center'), sg.Text(key='dscorrer_v', size= 11, justification= 'center'), sg.Text(key='peso_v', size= 11, justification= 'center'), sg.Text(key='split_v', size= 11, justification= 'center'), sg.Text(key='bend1_v', size= 11, justification= 'center'), sg.Text(key='pos_v', size= 11, justification= 'center'), sg.Text(key='tempo_v', size= 11, justification= 'center'), sg.Text(key='vtemp_v', size= 11, justification= 'center'), sg.Text(key='vmed_v', size= 11, justification= 'center'), sg.Text(key='rec_v', size= 11, justification= 'center'), sg.Text(key='spfin_v', size= 11, justification= 'center') ],
           [sg.Text('   ', size= 11, justification= 'center')],
           [sg.Table(key= 'hist_a', headings=['DATA', 'PISTA', 'DIST', 'TRAP', 'SPLIT', 'BENDS', 'PESO', 'CAT', 'TEMPO', 'VEL MEDIA', 'POS', 'REMARKS'], max_col_width=18, auto_size_columns=True, justification='center', values= []),
           sg.Table(key= 'hist_b', headings=['DATA', 'PISTA', 'DIST', 'TRAP', 'SPLIT', 'BENDS', 'PESO', 'CAT', 'TEMPO', 'VEL MEDIA', 'POS', 'REMARKS'], max_col_width=18, auto_size_columns=True, justification='center', values= [])],
           [sg.Text('TOTAL: A x B', size= 11, justification= 'center'), sg.Text(key='tot_a', size= 11, justification= 'center'), sg.Text(key='tot_b', size= 11, justification= 'center'), sg.Text('VENCEDOR:', size= 11, justification= 'center'), sg.Text(key='vencedor', size= 11, justification= 'center')],

           [sg.Button('Voltar')]]

janela_comp = None

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

        janela_secundaria['-COMBO-'].update(values=opcoes, set_to_index=0)

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
                    janela_comp = sg.Window('RACES', layout4)
                    janela_comp.Finalize()
                else:
                    janela_comp.un_hide()
                janela_ter.hide()

                dist = f_busca.buscar_race_dist(id_race)
                dog_A = valores3['-COMBO-']
                dog_B = valores3['-COMBO2-']
                d_dogs_a, d_dogs_b, venc = fun.compara(dist[0], dog_A, dog_B)

                a = d_dogs_a
                b = d_dogs_b


                #dias sem correr
                if a[2] > b[2]:
                    dsc_a_cor = 'red'
                    dsc_b_cor = 'green'
                elif a[2] < b[2]:
                    dsc_a_cor = 'green'
                    dsc_b_cor = 'red'
                else:
                    dsc_a_cor = 'white'
                    dsc_b_cor = 'white'

                #peso
                if a[3] > b[3]:
                    p_a_cor = 'green'
                    p_b_cor = 'red'
                elif a[3] < b[3]:
                    p_a_cor = 'red'
                    p_b_cor = 'green'
                else:
                    p_a_cor = 'white'
                    p_b_cor = 'white'

                #split
                if a[4] > b[4]:
                    spl_a_cor = 'red'
                    spl_b_cor = 'green'
                elif a[4] < b[4]:
                    spl_a_cor = 'green'
                    spl_b_cor = 'red'
                else:
                    spl_a_cor = 'white'
                    spl_b_cor = 'white'

                #primeira bend
                if a[5] > b[5]:
                    bnd1_a_cor = 'red'
                    bnd1_b_cor = 'green'
                elif a[5] < b[5]:
                    bnd1_a_cor = 'green'
                    bnd1_b_cor = 'red'
                else:
                    bnd1_a_cor = 'white'
                    bnd1_b_cor = 'white'

                #finalização
                if a[6] > b[6]:
                    pos_a_cor = 'red'
                    pos_b_cor = 'green'
                elif a[6] < b[6]:
                    pos_a_cor = 'green'
                    pos_b_cor = 'red'
                else:
                    pos_a_cor = 'white'
                    pos_b_cor = 'white'

                #tempo
                if a[7] > b[7]:
                    t_a_cor = 'red'
                    t_b_cor = 'green'
                elif a[7] < b[7]:
                    t_a_cor = 'green'
                    t_b_cor = 'red'
                else:
                    t_a_cor = 'white'
                    t_b_cor = 'white'

                #variação media de tempo
                if a[8] > b[8]:
                    vmt_a_cor = 'red'
                    vmt_b_cor = 'green'
                elif a[8] < b[8]:
                    vmt_a_cor = 'green'
                    vmt_b_cor = 'red'
                else:
                    vmt_a_cor = 'white'
                    vmt_b_cor = 'white'

                #velocidade media
                if a[9] > b[9]:
                    vm_a_cor = 'green'
                    vm_b_cor = 'red'
                elif a[9] < b[9]:
                    vm_a_cor = 'red'
                    vm_b_cor = 'green'
                else:
                    vm_a_cor = 'white'
                    vm_b_cor = 'white'

                #recupera / cansa
                if a[10] > b[10]:
                    rec_a_cor = 'green'
                    rec_b_cor = 'red'
                elif a[10] < b[10]:
                    rec_a_cor = 'red'
                    rec_b_cor = 'green'
                else:
                    rec_a_cor = 'white'
                    rec_b_cor = 'white'

                #split final
                if a[11] > b[11]:
                    spf_a_cor = 'green'
                    spf_b_cor = 'red'
                elif a[11] < b[11]:
                    spf_a_cor = 'red'
                    spf_b_cor = 'green'
                else:
                    spf_a_cor = 'white'
                    spf_b_cor = 'white'

                janela_comp['trap_a'].update(value=d_dogs_a[0] )
                janela_comp['nome_a'].update(value=d_dogs_a[1])
                janela_comp['dscorrer_a'].update(value=d_dogs_a[2], text_color = dsc_a_cor)
                janela_comp['peso_a'].update(value=d_dogs_a[3], text_color = p_a_cor)
                janela_comp['split_a'].update(value=d_dogs_a[4], text_color =spl_a_cor)
                janela_comp['bend1_a'].update(value=d_dogs_a[5], text_color =bnd1_a_cor)
                janela_comp['pos_a'].update(value=d_dogs_a[6], text_color =pos_a_cor)
                janela_comp['tempo_a'].update(value=d_dogs_a[7], text_color =t_a_cor )
                janela_comp['vtemp_a'].update(value=d_dogs_a[8], text_color =vmt_a_cor)
                janela_comp['vmed_a'].update(value=d_dogs_a[9], text_color =vm_a_cor)
                janela_comp['rec_a'].update(value=d_dogs_a[10], text_color =rec_a_cor)
                janela_comp['spfin_a'].update(value=d_dogs_a[11], text_color =spf_a_cor)

                janela_comp['trap_b'].update(value=d_dogs_b[0])
                janela_comp['nome_b'].update(value=d_dogs_b[1])
                janela_comp['dscorrer_b'].update(value=d_dogs_b[2], text_color =dsc_b_cor)
                janela_comp['peso_b'].update(value=d_dogs_b[3], text_color = p_b_cor)
                janela_comp['split_b'].update(value=d_dogs_b[4], text_color =spl_b_cor)
                janela_comp['bend1_b'].update(value=d_dogs_b[5], text_color =bnd1_b_cor)
                janela_comp['pos_b'].update(value=d_dogs_b[6], text_color =pos_b_cor)
                janela_comp['tempo_b'].update(value=d_dogs_b[7], text_color =t_b_cor)
                janela_comp['vtemp_b'].update(value=d_dogs_b[8], text_color =vmt_b_cor)
                janela_comp['vmed_b'].update(value=d_dogs_b[9], text_color =vmt_b_cor)
                janela_comp['rec_b'].update(value=d_dogs_b[10], text_color =rec_b_cor)
                janela_comp['spfin_b'].update(value=d_dogs_b[11], text_color =spf_b_cor)

                janela_comp['dscorrer_d'].update(value= abs(d_dogs_a[2] - d_dogs_b[2] ))
                janela_comp['peso_d'].update(value= abs(round(d_dogs_a[3] - d_dogs_b[3], 2)))
                janela_comp['split_d'].update(value= abs(round(d_dogs_a[4] - d_dogs_b[4], 2)))
                janela_comp['bend1_d'].update(value= abs(round(d_dogs_a[5] - d_dogs_b[5], 2)))
                janela_comp['pos_d'].update(value= abs(round(d_dogs_a[6] - d_dogs_b[6], 2)))
                janela_comp['tempo_d'].update(value= abs(round(d_dogs_a[7] - d_dogs_b[7], 2)))
                janela_comp['vtemp_d'].update(value= abs(round(d_dogs_a[8] - d_dogs_b[8], 2)))
                janela_comp['vmed_d'].update(value= abs(round(d_dogs_a[9] - d_dogs_b[9], 2)))
                janela_comp['rec_d'].update(value= abs(round(d_dogs_a[10] - d_dogs_b[10], 2)))
                janela_comp['spfin_d'].update(value= abs(round(d_dogs_a[11] - d_dogs_b[11], 2)))

                janela_comp['dscorrer_v'].update(value=venc[0])
                janela_comp['peso_v'].update(value=venc[1])
                janela_comp['split_v'].update(value=venc[2])
                janela_comp['bend1_v'].update(value=venc[3])
                janela_comp['pos_v'].update(value=venc[4])
                janela_comp['tempo_v'].update(value=venc[5])
                janela_comp['vtemp_v'].update(value=venc[6])
                janela_comp['vmed_v'].update(value=venc[7])
                janela_comp['rec_v'].update(value=venc[8])
                janela_comp['spfin_v'].update(value=venc[9])
                janela_comp['tot_a'].update(value=venc[10])
                janela_comp['tot_b'].update(value=venc[11])

                if venc[10] > venc[11]:
                    janela_comp['vencedor'].update(value=d_dogs_a[0])
                elif venc[10] < venc[11]:
                    janela_comp['vencedor'].update(value=d_dogs_b[0])
                else:
                    janela_comp['vencedor'].update(value='empate')


                a = f_busca.buscar_dog_id(dog_A)
                hist_a = f_busca.buscar_corridas_por_dog(a[0])
                for i in range(0, len(hist_a)):
                    hist_a[i] = hist_a[i][1:]

                b = f_busca.buscar_dog_id(dog_B)
                hist_b = f_busca.buscar_corridas_por_dog(b[0])
                for i in range(0, len(hist_b)):
                    hist_b[i] = hist_b[i][1:]
                # t_races_a = len(hist_a)
                # t_races_b = len(hist_b)

                janela_comp['hist_a'].update(values=hist_a)
                janela_comp['hist_b'].update(values=hist_b)


            while janela_comp is not None:
                evento4, valores4 = janela_comp.read()
                if evento4 == sg.WINDOW_CLOSED or evento4 == 'Voltar':
                    janela_ter.un_hide()  # Mostrando a janela principal novamente
                    janela_comp.hide()
                    break





# Fechando as janelas
janela_principal.close()
if janela_secundaria is not None:
    janela_secundaria.close()
    if janela_ter is not None:
        janela_ter.close()
        if janela_comp is not None:
            janela_comp.close()


