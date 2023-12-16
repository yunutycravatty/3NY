from src.config import *
from openai import OpenAI
import logging
import time
from src.backend.db.db import sqlitedb

def upload_files(upload_dir, client):
    oldfiles = sqlitedb.load_dict("filedict")
    newfiles = {}
    for file in os.listdir(upload_dir):
        if file in oldfiles:
            newfiles[file] = oldfiles[file]
            continue
        res = client.files.create(
            file=open(os.path.join(upload_dir, file), 'rb'),
            purpose='assistants'
        )
        newfiles[file] = res.id
        
    sqlitedb.save_or_update_dict(newfiles, "filedict")
    return newfiles

class OpenAIClient:
    def __init__(self):
        client = OpenAI(api_key=OPENAI_API_KEY)

        with open(INSTRUCTION_PATH, 'r', encoding='UTF-8', errors="ignore") as f:
            instructions = ''.join([line.rstrip() for line in f])

        files = upload_files(UPLOAD, client)
        file_ids = [id for id in files.values()]
        print(file_ids)
        assistant = client.beta.assistants.create(
		    name="Precurement Assistant",
		    instructions=instructions,
		    tools=[{"type": "code_interpreter"}],
		    model=MODEL,
            file_ids=file_ids[::-1]
	    )
        thread = client.beta.threads.create()

        self.client = client
        self.assistant = assistant
        self.thread = thread
    


    def send_message(self, msg):
        sent_time = time.time()
        self.client.beta.threads.messages.create(
            thread_id = self.thread.id,
            role = "user",
            content = msg
        )
        run = self.client.beta.threads.runs.create(
            thread_id=self.thread.id,
            assistant_id=self.assistant.id
        )
        while True :
            status = self.client.beta.threads.runs.retrieve(
                thread_id=self.thread.id,
                run_id =run.id
            ).status
            if status == 'completed':
                print("Status: completed")
                break

        messages = self.client.beta.threads.messages.list(
			thread_id=self.thread.id
		)

        for message in messages.data:
            if message.role == 'assistant' and message.created_at > sent_time:
                response = message.content[0].text.value
                print(f'Got response {response}')
                return response
            

openAiClient = OpenAIClient()