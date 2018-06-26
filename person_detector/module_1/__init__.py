from .edge import *
from .validate import *
from .extract_frame import *
from .extract_size import * 

def _processImage(imageName):
    print('image processed by module1')


def _detectEdge(imageName):
    '''
        Accept a name of image from request.
        Detect edge based on original image.
        Save processed edge in folder /processed with name 'edge.jpg'
    '''
    try:
        _edge = edge(imageName)
        _edge.save_detected_edge()
    except:
        raise ValueError('There is no such image: %s existed.' % imageName)


def _validateImage(imageName):
    '''
        Accept a name of image from request.
        Validate image based on human detection.
        Return a boolean as result for if/not validate.
    '''
    try:
        _validate = validate(imageName)
        _validate.detect_people()
        return _validate.detect_people()
    except:
        raise ValueError('There is no such image: %s existed.' % imageName)
    
def _validateImageTest():
    '''
        Validate images in test folder and print out results in folder.
    '''
    try:
        _validate = validate()
        _validate.test_HOG_in_folder()
        return True
    except Exception as e:
        return(str(e))

def _extractFrame(body):
    '''
        Validate images in test folder and print out results in folder.
    '''
    try:
        _extract_frame = extract_frame(**body)
        _extract_frame.loadmodel()
        return True
    except Exception as e:
        return(str(e))


def _extractSize(body):
    '''
        Validate images in test folder and print out results in folder.
    '''
    try:
        _extract_size = extract_size(**body)
        size = _extract_size._get_size_dictionary()
        return size
    except Exception as e:
        return(str(e))