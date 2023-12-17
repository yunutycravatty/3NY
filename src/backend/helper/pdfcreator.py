from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer, Image, PageTemplate, Frame
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors


def create_pdf(file_name, data):
    # Create a PDF document
    pdf = SimpleDocTemplate(file_name, pagesize=letter)

    # Create a list to hold the content of the PDF
    content = []

    # Add the header with the company logo
    header_logo_path = "company_logo.png"  # Replace with the actual path to your company logo
    header_logo = Image(header_logo_path, width=100, height=50)

    def header(canvas, doc):
        canvas.saveState()
        width, height = letter
        header_logo.drawOn(canvas, width - 120, height - 70)  # Adjust the Y-coordinate to move the logo down
        canvas.restoreState()

    frame = Frame(pdf.leftMargin, pdf.bottomMargin, pdf.width, pdf.height)
    template = PageTemplate(id='header', frames=[frame], onPage=header)

    pdf.addPageTemplates([template])

    # Add a spacer before the headline to move it up
    content.append(Spacer(1, 0.2 * inch))

    # Add the centered and even larger headline
    headline_style = ParagraphStyle(
        "Heading1",
        parent=getSampleStyleSheet()["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=24,  # Increase the font size to make the headline even bigger
        alignment=1  # 0=left, 1=center, 2=right
    )
    content.append(Paragraph("Procurement request #2", headline_style))

    # Add more space between the headline and the table
    content.append(Spacer(1, 0.3 * inch))

    # Create a table and populate it with data from the dictionary
    table_data = [(key, str(value)) for key, value in data.items()]

    # Calculate the width for the table (3/5 of the page width)
    table_width = pdf.width * 3 / 5

    table_style = TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                              ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                              ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                              ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                              ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                              ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                              ('GRID', (0, 0), (-1, -1), 1, colors.black)])

    table = Table(table_data, style=table_style, colWidths=[table_width] * len(table_data[0]))

    content.append(table)

    # Build the PDF document
    pdf.build(content)