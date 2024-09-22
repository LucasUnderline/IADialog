import speech_recognition as sr
import pyttsx3
import threading



class speech2Text:
    def __init__(self) -> None:
        self.__listening == False
        self.__text = ''

    
    def __speech2Text(self, noise_range=0.2, _callback=None) -> None:
        # Initialize the recognizer 
        r = sr.Recognizer()
        while True:  
            running += 1  
            # Exception handling to handle
            # exceptions at the runtime
            try:
                # use the microphone as source for input.
                with sr.Microphone() as mic:       
                    # adjust the energy threshold based on
                    # the surrounding noise level 
                    r.adjust_for_ambient_noise(mic, noise_range)
                    
                    #listens for the user's input 
                    audio = r.listen(mic, timeout=30)
                    
                    # Using google to recognize audio
                    text = r.recognize_google(audio)
                    text = text.lower()

                    self.__text += text 

                    print('Did you say: ', text)
                    
            except sr.RequestError as e:
                print('Could not request results; {0}'.format(e))
                break
                
            except sr.UnknownValueError:
                print('unknown error occurred')
                break

            if not self.__listening:
                break

        
        if _callback != None:
            _callback(self.__text)

    
    def start(self, noise_range=0.2, _callback=None):
        self.__listening = True

        x = threading.Thread(target=self.__speech2Text, args=[noise_range, _callback])
        x.start()

    def stop_listening(self):
        self.__listening = False