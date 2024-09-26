import PySimpleGUI as sg
import threading
import re
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
        self.__user_name = None
        self.__dialog_history = [] #list with tuples
        self.__main_button_text_list = ['Start Talk', 'Stop Talk', 'Stopping', 'Processing']
        self.__audio_channel = None
        pass
        

    def __init_gui(self) -> None:
        WINDOW_SIZE = (440, 140)

        #set collumns of GUI
        collumn_1 = [   [sg.Text('Nice to meet you! say anything to ia, be polite please')],
                        [sg.Text('For better Recognise and results, speak in english.')],
                        [sg.Text('How ia can call you?'), sg.InputText(default_text="João",key="name_input", size=25)],
                        [sg.HorizontalSeparator(color='grey')],
                        [sg.Button('Start Talk', key="main_button", size=32)]]
          
        collumn_2 = [   [sg.Slider(key="volume", range=(1, 10), default_value=5, enable_events=True)]]
   
        #apply collumns to layout and set theme
        layout = [[sg.Column(collumn_1), sg.Column(collumn_2)]]
        sg.theme('DarkGrey15')

        #setting GUI window end extract it for another methods use
        self.__gui_window = sg.Window('IaDialog', layout, size=WINDOW_SIZE)
        window = self.__gui_window
        
        # Event Loop to process "events" and get the "values" of the inputs
        main_button = window['main_button']
        while True:
            event, values = window.read()
            
            if event == sg.WIN_CLOSED: # if user closes window
                break

            if event == 'main_button':
                if main_button.get_text() == self.__main_button_text_list[0]: # if button text is Start Talking
                    self.__user_name = values['name_input'] # set username
                    self.__thread_start_speech2text(noise_range=0.6, _callback=self.__thread_start_process_message) #call speech2text an pass process method callback
                    main_button.Update(text=self.__main_button_text_list[1], disabled=False) # set button to Stop Talk
                    continue

                if main_button.get_text() == self.__main_button_text_list[1]: # if button text is Stop Talking
                    s.stop_listening() # stop the voice record
                    main_button.Update(text=self.__main_button_text_list[2], disabled=True) # set button to sttoping
                    continue

            #get volume slider input
            if event == 'volume':
                self.__audio_channel.set_volume(values['volume']/5) # slider_value=5 = 1.0 volume
                                                                    # slider_value=10 = 2.0 volume
                                                                    # slider_value=1 = 0.2 volume
        window.close()

    #process the text from speech
    def __process_message(self, message:str):
        self.__gui_window['main_button'].Update(text=self.__main_button_text_list[3], disabled=True) #change button to Processing

        formated_message = self.__format_message(message) #get prompt
        gpt_response = g.get_response(formated_message) #pass prompt to IA client

        formated_gpt_response = self.__format_gpt_response(gpt_response) #format GPT response with pattern
        audio_file = t.get_voice(formated_gpt_response) #pass only the response for elevenlabs API and get the audio file path
        
        self.__audio_play_response(audio_file) #play audio

        #end of process line
        self.__gui_window['main_button'].Update(text=self.__main_button_text_list[0], disabled=False) #change button to Start Talk again

    #start speech2text in another thread
    def __thread_start_speech2text(self, noise_range:float=0.2, _callback=None) -> None:
        x = threading.Thread(target=s.start, args=[noise_range, _callback])
        x.daemon = True # set to kill thread if main thread has killed
        x.start()

    #start the __process_message method in another thread
    def __thread_start_process_message(self, text:str) -> None:
        x = threading.Thread(target=self.__process_message, args=[text])
        x.daemon = True # set to kill thread if main thread has killed
        x.start()

    #format speech text to IA prompt
    def __format_message(self, message:str) -> str:
        #if user name field is empty username = friend
        if self.__user_name == '' or self.__user_name == None:
            self.__user_name = 'Friend'

        #if user said nothing, message = Hello!
        user_message = message
        if message == '' or message == None:
            user_message = "Hello!"  

        #If its the benning of dialog or have context
        if len(self.__dialog_history) <= 0:
            context = 'Its the beginning.'
        else:
            context = ''
            #If have context, put it on context variable
            for each in self.__dialog_history:
                context += f'{self.__user_name}: {each[0]}. You: {each[1]};'

        message = f'''Hello AI, please respond to {self.__user_name}'s message: {user_message}.
                        **Conversation history:**
                        {context}

                        **Instructions:**
                        Your response should be concise, coherent with the conversation, and demonstrate empathy and natural language. Imagine you're chatting with a friend. Please keep your response brief and to the point. DONT USE EMOJI.

                        **Response format:**
                        Enclose your response in quotation marks. After the response, include a summary of what the user said in parentheses and a summary of your response in brackets. **Be sure to include key details and specific points from the conversation.**

                        **Examples:**

                        "Hey there, hope you're doing okay. Want to talk about it? Maybe we can figure something out together."
                        (User expressed negative feelings) [AI suggests talking and helping the user]

                        **Your response:**'''
        return message
        
    #format GPT response with the pattern passed on prompt
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


    #play audio file
    def __audio_play_response(self, file):
        audio = mixer.Sound(file)
        self.__audio_channel.play(audio)

    #stop audio file **UNUSED**
    def __audio_stop(self):
        if self.__playing_audio:
            self.__audio_channel.stop()

    #start the application
    def start(self):
        pygame.init()
        mixer.init()
        self.__audio_channel = mixer.Channel(2)

        self.__init_gui()




app = IaDialog()
app.start()



