import speech_recognition as sr
import pyaudio
import wave


FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
CHUNK = 1024


class Speech2Text:
    def __init__(self) -> None:
        self.__max_recording_time = 30
        self.__output_file_path = 'output_files/record_output.mp3'

        self.__listening = False

    def __record_audio(self):
        audio = pyaudio.PyAudio()
        
        # start Recording
        stream = audio.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)
        print ("recording...")
        frames = []
        for i in range(0, int(RATE / CHUNK * self.__max_recording_time)):
            data = stream.read(CHUNK)
            frames.append(data)
            if not self.__listening:
                break
        print ("finished recording")
    
        # stop Recording
        stream.stop_stream()
        stream.close()
        audio.terminate()
        
        waveFile = wave.open(self.__output_file_path, 'wb')
        waveFile.setnchannels(CHANNELS)
        waveFile.setsampwidth(audio.get_sample_size(FORMAT))
        waveFile.setframerate(RATE)
        waveFile.writeframes(b''.join(frames))
        waveFile.close()

        return self.__output_file_path

    def __speech2Text(self, wave_file, noise_range=0.2, _callback=None):
        # Initialize the recognizer 
        r = sr.Recognizer()
        file = sr.AudioFile(wave_file)

        with file as source:
            audio = r.record(source)
            r.adjust_for_ambient_noise(source, noise_range)
        try:
            text = r.recognize_google(audio)
            print("Text: "+ text)
        except Exception as e:
            print("Exception: "+str(e))
        
        if _callback != None:
            _callback(text)

    
    def start(self, noise_range, _callback):
        print('start')
        self.__listening = True

        output_path = self.__record_audio()
        self.__speech2Text(output_path, noise_range, _callback)

    def stop_listening(self):
        self.__listening = False
    