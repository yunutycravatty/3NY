from flask import Blueprint, request, jsonify

from src.backend.schemas.gpt_request_schema import GptRequestSchema
from src.backend.services.gpt_request_service import gptRequestService

from flask import send_file, send_from_directory

gpt_request_route = Blueprint('gpt_request_route', __name__, url_prefix='/api/gpt-request')


@gpt_request_route.route('/', methods=['POST'])
def gpt_request():
    """
    Route for handling GPT-3.5 requests.
    """
    data = request.get_json()

    try:
        result = GptRequestSchema().load(data)
    except KeyError as e:
        return jsonify({'error': f'Missing required field: {e}'}), 400

    message = result['message']

    answer, sendpdf = gptRequestService.process_message(message) 
    print(answer)
    if sendpdf:
        
        print("send pdf")
        # Assuming answer contains the path to the PDF file
        file_path = ""+answer

        # Clean up the file after reading its content

        """ return jsonify({
            'contentType': 'application/pdf',
            'file': {
                'content': file_content.decode('latin1').encode('base64').decode('utf-8'),
                'name': 'pdfReport.pdf',
            }
        }), 200 """
        
        response = send_file(file_path, download_name='pdfReport.pdf', as_attachment=True, mimetype='application/pdf')
        response.headers['contentType'] = 'application/pdf'
        response.headers['filePath'] = file_path
        return response
        
        #return send_file(answer, download_name=answer.split('/')[-1], as_attachment=True) 
        """ return jsonify(
            {
                'contentType': 'application/pdf',
                
                'file': {
                        'downloadUrl': answer,
                        'name': 'pdfReport.pdf',
                    }
                
            }
        ),200 """
        #return send_file(answer, download_name='pdfReport.pdf', as_attachment=True)
    
    return jsonify({'answer': answer}), 200

