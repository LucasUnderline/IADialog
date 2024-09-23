import PySimpleGUI as sg
from speech2Text import Speech2Text
import threading
from g4f.client import Client

s = Speech2Text()




class IaDialog():
    def __init__(self) -> None:
        self.__user_name = None
        self.__speech_text = None
        self.__dialog_history = []


        self.__main_button_text_list = ['Start Talk', 'Stop Talk', 'Stopping', 'Processing', 'Stop Response']
        pass


    def __init_gui(self):
        WINDOW_SIZE = (440, 140)
        
        collumn_1 = [   [sg.Text('Nice to meet you! say anything to ia, be polite please')],
                        [sg.Text('For better Recognise and results, speak in english.')],
                        [sg.Text('How ia can call you?'), sg.InputText(default_text="Pedro",key="name_input", size=25)],
                        [sg.HorizontalSeparator(color='grey')],
                        [sg.ProgressBar(100, key="progress_bar", size=(20, 10))],
                        [sg.Button('Start Talk', key="main_button", size=20), sg.Button('Restart', key="restart_button", size=20)]  ]
        collumn_2 = [
                        [sg.Slider(key="volume")]
            ]

        # All the stuff inside your window.
        layout = [
                    [sg.Column(collumn_1), sg.Column(collumn_2)]
            ]
        
        
        sg.theme('DarkGrey15')

        # Create the Window
        self.__gui_window = sg.Window('IaDialog', layout, size=WINDOW_SIZE)
        window = self.__gui_window

        main_button = window['main_button']
        restart_button = window['restart_button']
        name_input = window['name_input']
        progress_bar = window['progress_bar']

        

        # Event Loop to process "events" and get the "values" of the inputs
        while True:
            event, values = window.read()
            

            if event == sg.WIN_CLOSED: # if user closes window
                break

            if event == 'main_button':
                if main_button.get_text() == self.__main_button_text_list[0]: # app is 0-already
                    s.start(noise_range=0.6, _callback=self.__get_ia_response)
                    main_button.Update(text=self.__main_button_text_list[1])
                    continue

                if main_button.get_text() == self.__main_button_text_list[1]: # app is 1-Talking
                    s.stop_listening()
                    main_button.Update(text=self.__main_button_text_list[2])
                    continue


        window.close()

    
    def __change_app_state_to(self, appStateListIndex:int, window):
        self.__appState = self.appStateList[appStateListIndex]
        window.refresh()

        
    def __format_message(self, message):
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


    def __ia_client(self, text):
        client = Client()
        response = client.chat.completions.create(
            model="gemini-pro",
            messages=[{"role": "user", "content": f'{text}'}],
        )
        print(response.choices[0].message.content)


    def __get_ia_response(self, message):
        text = self.__format_message(message)
        x = threading.Thread(target=self.__ia_client, args=[text])
        x.start()

        self.__gui_window['main_button'].Update(text=self.__main_button_text_list[3])


    def start(self):
        self.__init_gui()


app = IaDialog()
app.start()



