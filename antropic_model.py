from langchain_anthropic import ChatAnthropic
import os
from dotenv import find_dotenv, load_dotenv

dotenv_path = find_dotenv()
load_dotenv(dotenv_path)

api_key = os.getenv('ANTHROPIC_API_KEY')


class ClaudeModelAntropic:
    def __init__(self):
        self.__model = ChatAnthropic(model='claude-3-5-sonnet-20240620')

    def getModel(self):
        return self.__model
