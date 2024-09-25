import os
import requests
from elevenlabs import VoiceSettings
from elevenlabs.client import ElevenLabs

elevenlabs_api_key = os.environ.get('ELEVENLABS_API_KEY')

CHUNK_SIZE = 1024
 
class Text2speech:
  def __init__(self) -> None:
    self.__voice_id = "EXAVITQu4vr4xnSDxMaL"
    self.__request_url = "https://api.elevenlabs.io/v1/text-to-speech/" + self.__voice_id
    self.__output_file_path = 'output_files/elevenlabs_output.mp3'


  def __api_request(self, text):
    headers = {
      "Accept": "audio/mpeg",
      "Content-Type": "application/json",
      "xi-api-key": f'{elevenlabs_api_key}',
    }

    data = {
      "text": f'{text}',
      "model_id": "eleven_monolingual_v1",
      "voice_settings": {
      "stability": 0.5,
      "similarity_boost": 0.5
    }
    }

    response = requests.post(self.__request_url, json=data, headers=headers)
    with open(self.__output_file_path, 'wb') as f:
      for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
        if chunk:
          f.write(chunk)


  def config(self, **kwargs):
    self.__voice_id = kwargs.get('voice_id', 'EXAVITQu4vr4xnSDxMaL')
    self.__output_file_path = kwargs.get('output_file_location', 'output.mp3')


  def get_voice(self, text:str) -> str:
    self.__api_request(text)
    return self.__output_file_path