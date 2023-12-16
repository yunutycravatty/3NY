from flask import Flask
from flask_cors import CORS

from router.gpt_request_route import gpt_request_route


def create_app():
    app = Flask(__name__)
    CORS(app)
    app.register_blueprint(gpt_request_route)
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)