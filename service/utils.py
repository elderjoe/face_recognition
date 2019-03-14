from face_recognition import (
    face_locations,
    face_encodings,
)
from PIL import Image
import numpy as np
import cv2
from .settings import THRESHOLD


def enhance_image(image):
    """
    Sharpens the image for face retrieval
    
    :Parameter:
        image : (face recognition object) image object
    
    :Return:
        numpy array : sharpened image
    """
    kernel_sharpening = np.array([[-1,-1,-1], 
                                [-1, 9,-1],
                                [-1,-1,-1]])
    sharpened = cv2.filter2D(image, -1, kernel_sharpening)
    return np.asarray(sharpened)

def check_blur(image):
    """
    Returns the numerical value of the image blurriness

    :Parameter:
        image : (numpy obj) image object

    :Return:
        decimal : blurriness level (0 = lowest)
    """
    return cv2.Laplacian(image, cv2.CV_64F).var()

def find_face(face_locations, image):
    """
    Locates the faces in the image

    :Parameter:
        face_locations : (array) array of coordinates from image data
    
    :Return:
        FACE_IDX : (int) index
        FACES : (list) array of encoded face images 
    """
    # By getting the difference of right and left, we determine that 
    # the image is the largest that will be use to compare other face samples
    HIGH = 0
    FACE_IDX = 0
    # Array of encoded images
    FACES = []
    # Iterates the array for faces
    for idx, face_location in enumerate(face_locations):
        # Collect coordinates
        top, right, bottom, left = face_location
        # Access the face
        face_image = image[top:bottom, left:right]
        # Get images from coordinates
        pil_image = Image.fromarray(face_image)
        # Convert face_recognition object to numpy
        image_data = np.asarray(pil_image)
        # Check image quality again
        if check_blur(image_data) < THRESHOLD:
            pass
        # Detecting face from the image
        temp = right - left
        if HIGH < temp:
            HIGH = temp
            FACE_IDX = idx
        try:
            FACES.append(face_encodings(image_data)[0])
        except IndexError:
            pass
    return FACE_IDX, FACES

def rotate_image(image):
    """
    Aligns the image to retrieve face coordinates

    :Parameter:
        image : (numpy object) image object
    
    :Return:
        
    """
    coordinates = None
    coordinates = face_locations(image)
    angles = (90, 180, 270)
    if not coordinates:
        for angle in angles:
            # Get image height and width
            (h, w) = image.shape[:2]
            scale = 1.0
            # Calculate the center of the image
            (cX, cY) = (w//2, h//2)
            M = cv2.getRotationMatrix2D((cX, cY), -angle, scale)
            cos = np.abs(M[0, 0])
            sin = np.abs(M[0, 1])

            nW = int((h * sin) + (w * cos))
            nH = int((h * cos) + (w * sin))

            M[0, 2] += (nW / 2) - cX
            M[1, 2] += (nH / 2) - cY

            image = cv2.warpAffine(image, M, (nW, nH))
            coordinates = face_locations(image)
            if coordinates:
                break
                # Returns the coordinates and the rotated image
    return coordinates, image


