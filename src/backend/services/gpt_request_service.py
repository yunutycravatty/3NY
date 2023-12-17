from src.backend.apis.openai_api.client import OpenAiClient
from backend.helper.pdfcreator import PDFCreator
import re

from flask import send_file

class GptRequestService:
	def __init__(self):
		self.openai_client = OpenAiClient()
		self.pdf = PDFCreator()
		pass

	def process_message(self, msg):
		res = self.openAiClient(msg)
		pattern = "\{([^}]*)\}"
		matches = re.findall(pattern, res)

		if not matches:
			return res, False

		print(f'Pattern found: {matches[0]} Create PDF')

		pdf_path = self.pdf.create_pdf(matches[0], '/src/backend/resources/output/pdfreport.pdf')

		return pdf_path, True

gptRequestService = GptRequestService()