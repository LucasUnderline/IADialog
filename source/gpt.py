import re
import threading
from g4f.client import Client



class gpt:
    def __init__(self) -> None:
        self.__gpt_model = "gemini-pro"
        self.__gpt_role = "user"
        pass

    def __ia_client(self, text:str) -> str:
        client = Client()
        response = client.chat.completions.create(
            model=self.__gpt_model,
            messages=[{"role": f'{self.__gpt_role}', "content": f'{text}'}],
        )
        print(response.choices[0].message.content)
        return response.choices[0].message.content

    def config(self, **kwargs):
        model = kwargs.get('model', "gemini-pro")
        role = kwargs.get('role', 'user')

    def get_response(self, text):
        gpt_response = self.__ia_client(text)
        return gpt_response
