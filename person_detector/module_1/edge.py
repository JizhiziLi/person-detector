import cv2
from ..config import *
import os
# from matplotlib import pyplot as plt
# Note: if encounter Anaconda Runtime Error:python is not installed as a framework
# Simply use `conda install matplotlib` to fix the problems.

class edge:
    # Reason we are not doing cv2.imshow or plt.imshow is because:
    # libc++abi.dylib: terminating with uncaught exception of type NSException
    def __init__(self,imageName):
        self.imageName = imageName
        imagePath = os.path.join(UPLOAD_FOLDER, imageName)
        edgePath = os.path.join(DOWNLOAD_FOLDER, 'test.jpg')
        # delete the edge file if it exists.
        if os.path.isfile(edgePath):
            os.remove(edgePath)
        self.img = cv2.imread(imagePath,0)
        if self.img is None:
            raise ValueError('There is no such image: %s existed.' % imageName)
    

    # Reference: Canny Edge Detection
    # http://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_imgproc/py_canny/py_canny.html
    def save_detected_edge(self):
        '''
            Accept constructor.
            Detect edge based on original image.
            Save processed edge in folder /processed with name 'edge.jpg'
        '''
        edge = cv2.Canny(self.img, 100,200)
        #save the processed image to the download folder
        cv2.imwrite(os.path.join(DOWNLOAD_FOLDER, 'edge.jpg'), edge)
        cv2.waitKey(0)

 