import os

script_dir = os.path.dirname(__file__)
rel_path_instr = 'backend/resources/gpt_preprompt.txt'
rel_path_api_key = 'backend/resources/.OPENAI_API_KEY'
abs_file_path_instr = os.path.join(script_dir, rel_path_instr)
abs_file_path_api_key= os.path.join(script_dir, rel_path_instr)

INSTRUCTION_PATH=abs_file_path_instr
with open(abs_file_path_api_key) as f:
	key = ''.join([s for s in f.readlines()])
OPENAI_API_KEY = key
MODEL = "gpt-4-1106-preview"