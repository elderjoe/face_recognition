import os
from flask import Flask
from flask_restful import Resource, Api
from dotenv import load_dotenv

from service.routes import CheckImage
from service.settings import MAX_SIZE

# Load environment variables
load_dotenv()
SECRET_KEY = os.getenv('SECRET_KEY')
PORT = os.getenv('PORT')
HOST = os.getenv('HOST')
DEBUG = os.getenv('DEBUG')

app = Flask(__name__)
api = Api(app=app)
app.config['MAX_CONTENT_LENGTH'] = MAX_SIZE

# Add the API routes
api.add_resource(CheckImage, '/check_image/')

app.secret_key = SECRET_KEY

if __name__ == '__main__':
    app.run(debug=DEBUG, host=HOST, port=PORT)
