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
g = gpt()



class IaDialog():
    def __init__(self) -> None:
        self.__my_threads = []
        self.__user_name = None
        self.__dialog_history = []
        self.__main_button_text_list = ['Start Talk', 'Stop Talk', 'Stopping', 'Processing', 'Stop Response']
        self.__audio_channel = None
        self.__playing_audio = False
        pass
        

    def __init_gui(self):
        WINDOW_SIZE = (440, 140)

        collumn_1 = [   [sg.Text('Nice to meet you! say anything to ia, be polite please')],
                        [sg.Text('For better Recognise and results, speak in english.')],
                        [sg.Text('How ia can call you?'), sg.InputText(default_text="João",key="name_input", size=25)],
                        [sg.HorizontalSeparator(color='grey')],
                        [sg.Button('Start Talk', key="main_button", size=32)]]
          
        collumn_2 = [   [sg.Slider(key="volume")]]
   
        layout = [[sg.Column(collumn_1), sg.Column(collumn_2)]]
        sg.theme('DarkGrey15')

        self.__gui_window = sg.Window('IaDialog', layout, size=WINDOW_SIZE)
        window = self.__gui_window
        
        # Event Loop to process "events" and get the "values" of the inputs
        main_button = window['main_button']
        while True:
            event, values = window.read()
            
            if event == sg.WIN_CLOSED: # if user closes window
                break

            if event == 'main_button':
                if main_button.get_text() == self.__main_button_text_list[0]: # button text is Start Talking
                    self.__user_name = values['name_input']
                    self.__thread_start_speech2text(noise_range=0.6, _callback=self.__thread_start_process_message)
                    main_button.Update(text=self.__main_button_text_list[1], disabled=False)
                    continue

                if main_button.get_text() == self.__main_button_text_list[1]: # button text is Stop Talking
                    s.stop_listening()
                    main_button.Update(text=self.__main_button_text_list[2], disabled=True)
                    continue

                if main_button.get_text() == self.__main_button_text_list[4]: # button text is Stop Response
                    self.__audio_stop()
                    main_button.Update(text=self.__main_button_text_list[1], disabled=False)
                    continue
        window.close()


    def __process_message(self, message):
        self.__gui_window['main_button'].Update(text=self.__main_button_text_list[3], disabled=True)

        formated_message = self.__format_message(message)
        gpt_response = g.get_response(formated_message)

        formated_gpt_response = self.__format_gpt_response(gpt_response)
        audio_file = t.get_voice(formated_gpt_response)
        
        self.__audio_play_response(audio_file)

        #end of process line
        self.__gui_window['main_button'].Update(text=self.__main_button_text_list[0])


    def __thread_start_speech2text(self, noise_range=0.2, _callback=None):
        print('calling')
        x = threading.Thread(target=s.start, args=[noise_range, _callback])
        x.daemon = True
        x.start()
        
        self.__my_threads.append(x)

    def __thread_start_process_message(self, text):
        x = threading.Thread(target=self.__process_message, args=[text])
        x.daemon = True
        x.start()

        self.__my_threads.append(x)


    def __format_message(self, message:str) -> str:
        if self.__user_name == '' or self.__user_name == None:
            self.__user_name = 'Friend'

        user_message = message
        if message == '' or message == None:
            user_message = "Hello!"  

        if len(self.__dialog_history) <= 0:
            context = 'without, context. Is that the begin of the dialog.'
        else:
            context = ''
            for each in self.__dialog_history:
                context += f'user: {each[0]}. You: {each[1]};'

        message = f'''Hello AI, please respond to {self.__user_name}'s message: {user_message}.
                        **Context:**
                        {context}

                        **Instructions:**
                        Your response should be concise, coherent with the conversation, and demonstrate empathy and natural language. Imagine you're chatting with a friend. Please keep your response brief and to the point. DONT USE EMOJI.

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


    def __audio_play_response(self, file):
        self.__gui_window['main_button'].Update(self.__main_button_text_list[4], disabled=False)

        self.__playing_audio = True

        audio = mixer.Sound(file)
        self.__audio_channel.play(audio)


    def __audio_stop(self):
        if self.__playing_audio:
            self.__audio_channel.stop()


    def start(self):
        pygame.init()
        mixer.init()
        self.__audio_channel = mixer.Channel(2)

        self.__init_gui()




app = IaDialog()
app.start()



