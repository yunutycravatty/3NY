INSTRUCTIONS='/recourses/gpt_preprompt.txt'
with open('/resources/.OPENAI_API_KEY') as f:
	key = ''.join([s for s in f.readlines()])
OPENAI_API_KEY = key
MODEL = "gpt-4-1106-preview"