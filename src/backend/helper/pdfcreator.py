from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
import os

class PDFCreator:
	def __init__():
		pass

	def create_pdf(self, data_dict, filename):
		# Set up the document with the specified filename and page size
		doc = SimpleDocTemplate(filename, pagesize=letter)
		story = []
		styles = getSampleStyleSheet()

		# Table Data - starting with the headers
		table_data = [['Key', 'Value']]

		# Adding data from the dictionary
		for key, value in data_dict.items():
			table_data.append([key, value])

		# Define the style for the table
		table_style = TableStyle([
			('BACKGROUND', (0, 0), (-1, 0), colors.lightblue),  # Header row background color
			('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header row text color
			('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align all cells to the left
			('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header row font
			('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding in header row
			('BACKGROUND', (0, 1), (-1, -1), colors.whitesmoke),  # Background color for the rest of the table
			('GRID', (0, 0), (-1, -1), 1, colors.black),  # Grid lines
		])

		# Create a table for the data
		key_value_table = Table(table_data, colWidths=[200, 300], hAlign='LEFT')
		key_value_table.setStyle(table_style)
		story.append(key_value_table)

    	# Build the document
		doc.build(story)

		if os.path.exists(filename):
			print(f'File created at ${filename}')
			return filename
		else:
			print("File creation failed!")
			return None