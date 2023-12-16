from src.config import *
from openai import OpenAI
import logging
import time

class OpenAIClient:
    def __init__(self):
        client = OpenAI(api_key=config.OPENAI_KEY)

        with open(config.INSTRUCTION_PATH, 'r') as f:
            instructions = ''.join([line.rstrip for line in f])

        assistant = client.beta.assistants.create(
		    name="Precurement Assistant",
		    instructions=instructions,
		    tools=[{"type": "code_interpreter"}],
		    model=config.MODEL
	    )
        thread = client.beta.threads.create()

        self.client = client
        self.assistant = assistant
        self.thread = thread


    def send_message(self, msg):
        self.client.beta.threads.messages.create(
            thread_id = self.thread.id,
            role = "user",
            content = msg
        )
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id,
            instructions="Please address the user as Nico. The user has a premium account."
        )
        while(True):
            status = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id =run.id
            ).status

            if status == 'completed':
                break

        messages = self.client.beta.threads.messages.list(
			thread_id=self.thread.id
		)

        sent_time = time.time()

        for message in messages.data:
            if message.role == 'assistant' and message.created_at > sent_time:
                response = message.content[0].text.value
                logging.INFO(f'Got response {response}')
                return response
            

