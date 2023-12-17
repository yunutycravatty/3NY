from src.backend.apis.openai_api.client import OpenAIClient
from src.backend.helper.pdfcreator import PDFCreator
import re
import os
import json 
from src.config import *

#from flask import send_file, jsonify

class GptRequestService:
	def __init__ (self):
		self.openai_client = OpenAIClient()
		self.pdf = PDFCreator()

	def process_message(self, msg):
		res = self.openai_client.send_message(msg)
		pattern = "\{([^}]*)\}"
		matches = re.findall(pattern, res)

		if not matches:
			return res, False

		print(f'Pattern found: {matches[0]} Create PDF')

		js = "{" + matches[0] + "}"
		print("js: ",js)
		data = json.loads(js)
		#data = jsonify(matches[0])

		print(data)
		#script_dir = os.path.dirname(__file__)
		#abs_file_path_pdf = os.path.join(script_dir, '../resources/output/pdfReport.pdf')
		pdf_path = self.pdf.create_pdf(data, ROOT_DIR + '/backend/resources/output/pdfReport.pdf')

		return pdf_path, True

gptRequestService = GptRequestService()