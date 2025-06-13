import cv2
import imutils
import numpy as np
import matplotlib.pyplot as plt
import os
from os import listdir


def crop_brain_contour(image, plot=False):
    #import imutils
    #import cv2
    #from matplotlib import pyplot as plt

    # Convert the image to grayscale, and blur it slightly
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # Threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # Find contours in thresholded image, then grab the largest one
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    # Find the extreme points
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])

    # crop new image out of the original image using the four extreme points (left, right, top, bottom)
    new_image = image[extTop[1]:extBot[1], extLeft[0]:extRight[0]]

    if plot:
        plt.figure()

        plt.subplot(1, 2, 1)
        beforeImg = cv2.resize(image,(240,240))
        plt.imshow(beforeImg)

        plt.tick_params(axis='both', which='both',
                        top=False, bottom=False, left=False, right=False,
                        labelbottom=False, labeltop=False, labelleft=False, labelright=False)

        plt.title('Before')

        plt.subplot(1, 2, 2)
        afterImg = cv2.resize(new_image,(240,240))
        plt.imshow(afterImg)

        plt.tick_params(axis='both', which='both',
                        top=False, bottom=False, left=False, right=False,
                        labelbottom=False, labeltop=False, labelleft=False, labelright=False)

        plt.title('After')

        plt.show()

    return new_image

dir_list = ['Testing/glioma_tumor', 'Testing/meningioma_tumor', 'Testing/no_tumor', 'Testing/pituitary_tumor',
            'Validation/glioma_tumor', 'Validation/meningioma_tumor', 'Validation/no_tumor', 'Validation/pituitary_tumor',
            'Training/glioma_tumor', 'Training/meningioma_tumor', 'Training/no_tumor', 'Training/pituitary_tumor']

image_width, image_height = (240, 240)

for directory in dir_list:
    for filename in listdir(directory):
        # load the image
        image = cv2.imread(directory + '\\' + filename)
        # crop the brain and ignore the unnecessary rest part of the image
        image = crop_brain_contour(image, plot=False)
        # resize image
        image = cv2.resize(image, dsize=(image_width, image_height), interpolation=cv2.INTER_CUBIC)

        nFolderPath = 'Processed' + directory
        if not os.path.exists(nFolderPath):
            os.makedirs(nFolderPath)
        cv2.imwrite(os.path.join(nFolderPath, filename), image)


# ex_img = cv2.imread('TestImage/Yes/qwe.jpg')
# ex_new_img = crop_brain_contour(ex_img, True)


