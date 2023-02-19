import PySimpleGUI as sg

# Criando a janela principal
layout = [[sg.Text('Escolha uma opção:')],
          [sg.Combo(['Opção 1', 'Opção 2', 'Opção 3', 'Opção 4'], default_value='Opção 1')],
          [sg.Button('Ok'), sg.Button('Mostrar outra janela')]]

janela_principal = sg.Window('Janela principal', layout, size=(400, 200))

# Criando a segunda janela
layout2 = [[sg.Text('Escolha outra opção:')],
           [sg.Combo([], key='-COMBO-')],
           [sg.Button('Ok'), sg.Button('Fechar')]]

janela_secundaria = None

# Loop para ler eventos da janela principal
while True:
    evento, valores = janela_principal.read()
    if evento == sg.WINDOW_CLOSED:
        break
    elif evento == 'Ok':
        opcao_escolhida = valores[0]
        sg.popup(f'Você escolheu a opção {opcao_escolhida}.')
    elif evento == 'Mostrar outra janela':
        if janela_secundaria is None:
            janela_secundaria = sg.Window('Janela secundária', layout2)
            janela_secundaria.Finalize()
        else:
            janela_secundaria.un_hide()
        janela_principal.hide()  # Escondendo a janela principal enquanto a janela secundária está aberta

        # Preenchendo as opções do campo select com o array passado pela janela principal
        opcoes = ['Opção A', 'Opção B', 'Opção C', 'Opção D']
        janela_secundaria['-COMBO-'].update(values=opcoes)

    # Loop para ler eventos da janela secundária
    while janela_secundaria is not None:
        evento2, valores2 = janela_secundaria.read()
        if evento2 == sg.WINDOW_CLOSED or evento2 == 'Fechar':
            janela_principal.un_hide()  # Mostrando a janela principal novamente
            janela_secundaria.hide()
            break
        elif evento2 == 'Ok':
            opcao_escolhida = valores2['-COMBO-']
            sg.popup(f'Você escolheu a opção {opcao_escolhida} na segunda janela.')

# Fechando as janelas
janela_principal.close()
if janela_secundaria is not None:
    janela_secundaria.close()
