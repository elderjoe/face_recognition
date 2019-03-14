from io import BytesIO
import requests
from requests.exceptions import (
    InvalidURL,
    MissingSchema,
    Timeout
)
from PIL import Image
from flask import (
    Blueprint,
    jsonify,
    request,
)
from flask_restful import Resource
from face_recognition import (
    compare_faces,
    load_image_file
)
from .utils import (
    enhance_image,
    check_blur,
    find_face,
    rotate_image
)
from .settings import (
    TOLERANCE,
    ALLOWED_EXTENSIONS,
    MAX_SIZE,
    THRESHOLD
)
from .statics import ERR

class CheckImage(Resource):

    @staticmethod
    def allowed_file(filename):
        return ('.' in filename and filename.split('.')[1]) \
            or ('/' in filename and filename.split('/')[1]) \
            in ALLOWED_EXTENSIONS
    
    @staticmethod
    def _download_image(url=None):
        try:
            IMAGE_SIZE = int(requests.head(url).headers['content-length'])
            if not CheckImage.allowed_file(
                requests.head(url).headers['content-type']):
                raise ValueError('NOT_SUPPORTED')
            if  IMAGE_SIZE > MAX_SIZE:
                raise Exception('FILE_SIZE')
            response = requests.get(url)
            return load_image_file(BytesIO(response.content))
        except InvalidURL:
            raise InvalidURL(ERR['INV_URL'])
        except MissingSchema:
            raise MissingSchema(ERR['INV_SCHEMA'])
        except Timeout:
            raise Timeout(ERR['TIMEOUT'])
        except AttributeError:
            raise
    
    @staticmethod
    def check_image(id_picture, selfie):
        """
        Process the image for recognition

        :Parameter:
            id_picture : (face_recognition obj) face(s) source for comparison
            selfie : (face_recognition obj) source for specimen to be analyze
        
        :Return:
            boolean
            True for a successful identification or same face
            False for no images given, too blur to analyze or face does not
            match the face(s) source
        """
        image_a = enhance_image(id_picture)
        image_b = enhance_image(selfie)

        if check_blur(image_a) < THRESHOLD or \
            check_blur(image_b) < THRESHOLD:
            return False

        face_locations_a, image_a = rotate_image(image_a)
        face_locations_b, image_b = rotate_image(image_b)

        IDX, FACES_A = find_face(face_locations_a, image_a)
        SPECIMEN = FACES_A.pop(IDX)
        _, FACES_B = find_face(face_locations_b, image_b)
        
        return compare_faces(FACES_B, SPECIMEN, TOLERANCE)

    def post(self):
        try:
            if hasattr(request, 'json'):
                id_picture = self._download_image(request.json['id_picture'])
                selfie = self._download_image(request.json['selfie'])
                result = self.check_image(id_picture, selfie)
            return jsonify({'result': str(result[0])})
        except requests.RequestException as e:
            return {'message': str(e)}
        except Exception as e:
            return {'message': str(e)}
