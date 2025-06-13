import numpy as np
import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
from skimage import transform

model = tf.keras.models.load_model(('btc_vgg_final_model2.hdf5'), custom_objects={'KerasLayer': hub.KerasLayer})

np_image = Image.open("ProcessedTraining/no_tumor/image(40).jpg")
np_image = np.array(np_image).astype('float32') #/255
np_image = transform.resize(np_image, (224, 224, 3))
np_image = np.expand_dims(np_image, axis=0)

result = model.predict(np_image)

predicted_label_index = np.argmax(result)
class_labels = ['glioma_tumor', 'meningioma_tumor', 'no_tumor', 'pituitary_tumor']
predicted_label = class_labels[predicted_label_index]
print("Predicted label:", predicted_label)