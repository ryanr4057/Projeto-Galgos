import PySimpleGUI as sg
import f_busca

pistas = f_busca.buscar_todas_pistas()

# Definindo opções para o campo select
opcoes_p = []
for pista in pistas:
    opcoes_p.append(pista[0])

# Criando a janela
layout_p = [[sg.Text('Escolha a pista:')],
          [sg.Combo(opcoes_p, default_value=opcoes_p[0])],
          [sg.Button('Ok')]]

janela_pistas = sg.Window('Pistas', layout_p)

def c_layout_r(opcoes_r):
    layout_r = [[sg.Text('Escolha a corrida:')],
            [sg.Combo(opcoes_r, default_value=opcoes_r[0])],
            [sg.Button('Ok')]]
    janela_races = sg.Window('Janela com Select', c_layout_r(opcoes_r))
    return(janela_races)



# Loop para ler eventos da janela
while True:
    evento, valores = janela_pistas.read()
    if evento == sg.WINDOW_CLOSED:
        break

    elif evento == 'Ok':
        pista_escolhida = valores[0]
        id_pista = f_busca.buscar_pista_id(pista_escolhida)
        races = f_busca.buscar_races_por_pista(id_pista)
        # print(races)
        opcoes_r = []
        for race in races:
            opcoes_r.append(race[0])

        l = c_layout_r(opcoes_r)
        janela_pistas.close()
        evento, valores = l.read()
        if evento == sg.WINDOW_CLOSED:
            break
        elif evento == 'Ok':
            race_escolhida = valores[0]
            sg.popup(f'Você escolheu a opção {race_escolhida}.')

# Fechando a janela
# janela_pistas.close()
