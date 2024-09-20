import PySimpleGUI as sg

WINDOW_SIZE = (520, 140)

# All the stuff inside your window.
layout = [  [sg.Text('Nice to meet you! say anything to Ia, be polite please')],
            [sg.Text('For better Recognise and results, speak in english.')],
            [sg.Text('How Ia can call you?'), sg.InputText(key="name_input")],
            [sg.HorizontalSeparator(color='grey')],
            [sg.ProgressBar(100, key="progress_bar", size=(100, 10))],
            [sg.Button('Start Talking', key="main_button", size=50), sg.Button('Restart', key="restart_button", size=50)] ]

# Create the Window
sg.theme('DarkGrey15')
window = sg.Window('IaDialog', layout, size=WINDOW_SIZE)

# Event Loop to process "events" and get the "values" of the inputs
while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED: # if user closes window
        break

    if event == 'main_button':
        if window['main_button'].get_text() == 'Start Talk': #IF START TALK AS PRESSED, DO ANYTHING AND CHANGE BUTTON
            print('Started')
            window['main_button'].Update(text="Stop Talk")
            continue

        if window['main_button'].get_text() == 'Stop Talk': #IF STOP TALK AS PRESSED, DO ANYTHING AND CHANGE BUTTON
            print('Stoped')
            window['main_button'].Update(text="Start Talk")
            continue


window.close()