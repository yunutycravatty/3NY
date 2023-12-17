from flask import Blueprint, request, jsonify, redirect

from src.backend.services.gpt_request_service import gptRequestService

upload_image_route = Blueprint('upload_image_route', __name__, url_prefix='/api/upload-image')

@upload_image_route.route('/', methods=['POST'])
def upload_image():
    # get img path from request
    data = request

    # post to gpt_request_route message = <image uploaded>
    message = { 'message': '<image uploaded> under ' + data }
    answer, sendpdf = gptRequestService.process_message(message)

    # return response
    return jsonify({'answer': 'image uploaded'}), 200


