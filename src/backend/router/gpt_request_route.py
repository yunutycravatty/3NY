from flask import Blueprint, request, jsonify

from src.backend.schemas.gpt_request_schema import GptRequestSchema
from src.backend.apis.openai_api.client import openAiClient

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

    answer = openAIClient.send_message(message)

    return jsonify({'answer': answer}), 200
