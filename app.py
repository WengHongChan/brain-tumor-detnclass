import os
import numpy as np
import tensorflow as tf
from PIL import Image
from skimage import transform
import cv2
from pathlib import Path
import tensorflow_hub as hub

#Flask utils
from flask import Flask, request, render_template, jsonify

# Define a flask app
app = Flask(__name__)

# Model saved with Keras model.save()
model = tf.keras.models.load_model(('btc_vgg_final_model2.hdf5'), custom_objects={'KerasLayer': hub.KerasLayer})


def model_predict(image_to_Predict, model):
    np_image = np.array(image_to_Predict).astype('float32')  #/255
    np_image = transform.resize(np_image,(224,224,3))
    np_image = np.expand_dims(np_image, axis=0)
    result = model.predict(np_image)

    predicted_label_index = np.argmax(result)
    class_labels = ['glioma_tumor','meningioma_tumor','no_tumor','pituitary_tumor']
    predicted_label = class_labels[predicted_label_index]

    result = dict()

    if predicted_label == 'no_tumor':
        result['detectTumor'] = "No"
        result['typeTumor'] = "-"
    else:
        result['detectTumor'] = "Yes"
        if predicted_label == 'glioma_tumor':
            result['typeTumor'] = "Glioma Tumor"
        elif predicted_label == 'meningioma_tumor':
            result['typeTumor'] = "Meningioma Tumor"
        elif predicted_label == 'pituitary_tumor':
            result['typeTumor'] = "Pituitary Tumor"

    return result

@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        image_File = request.files['file']
        image_to_Predict = Image.open(image_File)

        # Make prediction
        result = model_predict(image_to_Predict, model)
        return result
    return None


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('base.html')

@app.route('/locateTumorRegion', methods=['GET'])
def ltregion():
    # Second page
    return render_template('locateTR.html')

@app.route('/tumorInfo', methods=['GET'])
def tinfo():
    # Third page
    return render_template('tInfo.html')


@app.route('/checkGreyscale', methods=['GET', 'POST'])
def is_grey_scale():
    if request.method == 'POST':
        image_File = request.files['file']
        img = Image.open(image_File).convert('RGB')
        w, h = img.size
        for i in range(w):
            for j in range(h):
                r, g, b = img.getpixel((i,j))
                if r != g != b:
                    return "0"
        return "1"
    return None

@app.route('/highlightTumorRegion', methods=['GET', 'POST'])
def hlTumorReg():
    if request.method == 'POST':
        # Get the file from the post request
        image_File = request.files['file']
        image = Image.open(image_File)
        image = image.convert("RGB")  # Convert to RGB format if needed
        image = np.array(image)
        image_gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY).astype('uint8')
        ret,thresh = cv2.threshold(image_gray,0,255,cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
        kernel = np.ones((3,3),np.uint8)
        image_opened = cv2.morphologyEx(thresh,cv2.MORPH_OPEN,kernel,iterations=2)
        sure_bg = cv2.dilate(image_opened,kernel,iterations=3)

        # Finding sure foreground area
        dist_transform = cv2.distanceTransform(image_opened,cv2.DIST_L2,5)
        ret,sure_fg = cv2.threshold(dist_transform,0.7 * dist_transform.max(),255,0)

        # Find unknown region
        sure_fg = np.uint8(sure_fg)
        unknown = cv2.subtract(sure_bg,sure_fg)

        # Marker labelling
        ret,markers = cv2.connectedComponents(sure_fg)

        # Add one to all labels so that sure background is not 0, but 1
        markers = markers + 1

        # Now mark the region of unknown with zero
        markers[unknown == 255] = 0

        # Convert the image to a 3-channel grayscale (BGR) image
        image_bgr = cv2.cvtColor(image,cv2.COLOR_RGB2BGR)

        # Apply the watershed algorithm
        markers = cv2.watershed(image_bgr,markers)

        # Colorize the image based on the watershed result
        image_bgr[markers == -1] = [255,0,0]

        # Convert the image back to HSV color space
        tumorImage = cv2.cvtColor(image_bgr,cv2.COLOR_HSV2BGR)

        nFolderPath = "static/upload"
        filename = "tempImg.jpg"
        imgAddress = os.path.join(nFolderPath,filename).replace("\\","/")
        img_Path = Path(imgAddress)
        num = 0
        while img_Path.exists():
            num += 1
            filename = "tempImg"+ str(num) +".jpg"
            imgAddress = os.path.join(nFolderPath,filename).replace("\\","/")
            img_Path = Path(imgAddress)

        cv2.imwrite(imgAddress,tumorImage)

        return imgAddress
    return None

if __name__ == '__main__':
    app.run(debug=False)