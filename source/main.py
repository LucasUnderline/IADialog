import PySimpleGUI as sg
import threading
import re
import os
import pygame
from pygame import mixer

from speech2Text import Speech2Text
from gpt import gpt
from text2speech import Text2speech




s = Speech2Text()
t = Text2speech()
elevenlabs_api_key = os.environ.get('ELEVENLABS_API_KEY')

gpt_client = gpt()

class IaDialog():
    def __init__(self) -> None:
        self.__user_name = None
        self.__speech_text = None
        self.__dialog_history = []
        self.__ia_response = None

        self.__main_button_text_list = ['Start Talk', 'Stop Talk', 'Stopping', 'Processing', 'Stop Response']
        self.__gpt_client

        self.__audio_channel = mixer.Channel(2)
        self.__playing_audio = False
        pass
        

    def __init_gui(self):
        WINDOW_SIZE = (440, 140)

        collumn_1 = [   [sg.Text('Nice to meet you! say anything to ia, be polite please')],
                        [sg.Text('For better Recognise and results, speak in english.')],
                        [sg.Text('How ia can call you?'), sg.InputText(default_text="João",key="name_input", size=25)],
                        [sg.HorizontalSeparator(color='grey')],
                        [sg.Button('Start Talk', key="main_button", size=20), sg.Button('Restart', key="restart_button", size=20)]]    
          
        collumn_2 = [   [sg.Slider(key="volume")]]
   
        layout = [[sg.Column(collumn_1), sg.Column(collumn_2)]]
        sg.theme('DarkGrey15')

        self.__gui_window = sg.Window('IaDialog', layout, size=WINDOW_SIZE)
        window = self.__gui_window

        main_button = window['main_button']
        restart_button = window['restart_button']
        name_input = window['name_input']

        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            

            if event == sg.WIN_CLOSED: # if user closes window
                break

            if event == 'main_button':
                if main_button.get_text() == self.__main_button_text_list[0]: # app is 0-already
                    self.__user_name = values['name_input']
                    s.start(noise_range=0.6, _callback=self.__start_process_message)
                    main_button.Update(text=self.__main_button_text_list[1], disabled=False)
                    continue

                if main_button.get_text() == self.__main_button_text_list[1]: # app is 1-Talking
                    s.stop_listening()
                    main_button.Update(text=self.__main_button_text_list[2], disabled=True)
                    continue

        window.close()


    def __process_message(self, message):

        formated_message = self.__format_message(message)
        gpt_response = gpt.get_response(formated_message)

        formated_gpt_response = self.__format_gpt_response(gpt_response)
        audio_file = t.get_voice(formated_gpt_response)
        
        self.__play_response_audio(audio_file)


    def __start_process_message(self, text):
        x = threading.Thread(target=self.__process_message, args=[text])
        x.start()


    def __format_message(self, message:str) -> str:
        if self.__user_name == '' or self.__user_name == None:
            self.__user_name = 'Friend'

        if self.__speech_text == '' or self.__speech_text == None:
            self.__speech_text = "Hello!"

        if len(self.__dialog_history) <= 0:
            context = 'without, context. Is that the begin of the dialog.'
        else:
            for each in self.__dialog_history:
                context += f'user: {each[0]}. You: {each[1]};'

        message = f'''Hello AI, please respond to {self.__user_name}'s message: {self.__speech_text}.
                        **Context:**
                        {context}

                        **Instructions:**
                        Your response should be concise, coherent with the conversation, and demonstrate empathy and natural language. Imagine you're chatting with a friend. Please keep your response brief and to the point.

                        **Response format:**
                        Enclose your response in quotation marks. After the response, include a summary of what the user said in parentheses and a summary of your response in brackets. 

                        **Example:**
                        "Hey there, hope you're doing okay. Want to talk about it? Maybe we can figure something out together."
                        (User expressed negative feelings) [AI suggests talking and helping the user]

                        **Your response:**'''
        return message
        
    def __format_gpt_response(self, response:str) -> str:
        parentheses_pattern = r'\((.*?)\)'
        bracket_pattern = r'\[(.*?)\]'
        quotes_pattern = r'\"(.*?)\"'

        parentheses_text = re.findall(parentheses_pattern, response)
        bracket_text = re.findall(bracket_pattern, response)
        quotes_text = re.findall(quotes_pattern, response)


        self.__dialog_history.append((parentheses_text, bracket_text))
        gpt_response_text = quotes_text

        return gpt_response_text

    def __play_response_audio(self, file):
        self.__playing_audio = True

        audio = mixer.Sound(file)
        self.__audio_channel.play(audio)

    def __stop_audio(self):
        if self.__playing_audio:
            self.__audio_channel.stop()


    def start(self):
        pygame.init()
        mixer.init()

        self.__init_gui()




app = IaDialog()
app.start()



