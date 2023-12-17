from flask import Blueprint, request, jsonify

from src.backend.schemas.gpt_request_schema import GptRequestSchema
from src.backend.services.gpt_request_service import gptRequestService

from flask import send_file

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
       send_file(answer, attachment_filename=answer.split('/')[-1]) 
    
    return jsonify({'answer': answer}), 200

