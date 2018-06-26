import cv2
from ..config import *
from imutils.object_detection import non_max_suppression
import os
import imutils
from imutils import paths
import numpy as np
import shutil


index = 0
class validate:
    def __init__(self, imageName=None):
        if imageName is not None:
            f = os.path.join(UPLOAD_FOLDER, imageName)
            self.img = cv2.imread(f)
            if self.img is None:
                raise ValueError('There is no such image: %s existed.' % imageName)

    def validate_image(self):
        validate = False
        return validate

    def detect_people(self):
        '''
        Accept a photo.
        Validate if there is a full body people in it.
        Return the result as True/Flase as validation.
        Reference: https://www.pyimagesearch.com/2015/11/09/pedestrian-detection-opencv/
                   http://mccormickml.com/2013/05/09/hog-person-detector-tutorial/
        '''
        # initialize the HOG descriptor/person detector
        hog = cv2.HOGDescriptor()
        hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
        # load the image and resize it to (1) reduce detection time
        # and (2) improve detection accuracy
        image = imutils.resize(self.img, width=min(400, self.img.shape[1]))
        orig = image.copy()
        # detect people in the image
        (rects, weights) = hog.detectMultiScale(
            image, winStride=(4, 4), padding=(8, 8), scale=1.05)
        # draw the original bounding boxes
        for (x, y, w, h) in rects:
            cv2.rectangle(orig, (x, y), (x + w, y + h), (0, 0, 255), 2)
        # apply non-maxima suppression to the bounding boxes using a
            # fairly large overlap threshold to try to maintain overlapping
            # boxes that are still people
        rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
        pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
            # draw the final bounding boxes
        for (xA, yA, xB, yB) in pick:
            cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)

        # # show some information on the number of bounding boxes
            # filename = imagePath[imagePath.rfind("/") + 1:]
            # print("[INFO] {}: {} original boxes, {} after suppression".format(
            #     filename, len(rects), len(pick)))
        # cv2.imwrite(os.path.join(DOWNLOAD_FOLDER, 'original.jpg'), orig)
        cv2.imwrite(os.path.join(DOWNLOAD_FOLDER, 'validate.jpg'), image)
        cv2.waitKey(0)

        return len(pick)!=0


    def test_HOG_in_folder(self):
        '''
        Process all images in folder `VALIDATE_TEST_FOLDER`
        Validate them and print results in folder `VALIDATE_RESULT_FOLDER`
        '''
        shutil.rmtree(VALIDATE_RESULT_FOLDER)
        os.makedirs(VALIDATE_RESULT_FOLDER)
        global index
        # except Exception as e:
        for imagePath in paths.list_images(VALIDATE_TEST_FOLDER):
            print('Processing: %s' % str(imagePath))
            hog = cv2.HOGDescriptor()
            hog.setSVMDetector(cv2.HOGDescriptor_getDefaultPeopleDetector())
            img = cv2.imread(imagePath)
            image = imutils.resize(img, width=min(400, img.shape[1]))
            (rects, weights) = hog.detectMultiScale(
            image, winStride=(4, 4), padding=(8, 8), scale=1.05)
            rects = np.array([[x, y, x + w, y + h] for (x, y, w, h) in rects])
            pick = non_max_suppression(rects, probs=None, overlapThresh=0.65)
            for (xA, yA, xB, yB) in pick:
                cv2.rectangle(image, (xA, yA), (xB, yB), (0, 255, 0), 2)
            validateName = str(index)+'_'+str(len(pick)!=0)+'_'+str(len(pick))+'.jpg'
            cv2.imwrite(os.path.join(VALIDATE_RESULT_FOLDER, validateName), image)
            cv2.waitKey(0)
            index = index+1
            


