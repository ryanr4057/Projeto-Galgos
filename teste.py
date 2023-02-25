# import PySimpleGUI as sg
# import keyboard

# layout = [[sg.Text('Pressione ESC para fechar')]]

# window = sg.Window('Janela', layout)

# while True:
#     event, values = window.read()
#     print(keyboard.read_key())

#     if event == sg.WINDOW_CLOSED:
#         break

#     if keyboard.is_pressed('a'):
#         window.close()
#         break

# window.close()



import keyboard

while True:
    event = keyboard.read_event()

    if event.event_type == 'down':
        print('Tecla pressionada:', event)

    if event.event_type == 'up':
        print('Tecla liberada:', event)
