import openai


class OpenAIClient:
    def __init__(self, api_key):
        openai.api_key = api_key