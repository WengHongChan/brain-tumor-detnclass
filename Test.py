import cv2
import numpy as np
from PIL import Image

#image = cv2.imread('ProcessedTesting/glioma_tumor/image(8).jpg')
image = Image.open('ProcessedTraining/glioma_tumor/gg (8).jpg')
image = image.convert("RGB")  # Convert to RGB format if needed
image = np.array(image)
image_gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY).astype('uint8')
ret, thresh = cv2.threshold(image_gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
kernel = np.ones((3, 3), np.uint8)
image_opened = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
sure_bg = cv2.dilate(image_opened, kernel, iterations=3)

# Finding sure foreground area
dist_transform = cv2.distanceTransform(image_opened, cv2.DIST_L2, 5)
ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

# Find unknown region
sure_fg = np.uint8(sure_fg)
unknown = cv2.subtract(sure_bg, sure_fg)

# Marker labelling
ret, markers = cv2.connectedComponents(sure_fg)

# Add one to all labels so that sure background is not 0, but 1
markers = markers + 1

# Now mark the region of unknown with zero
markers[unknown == 255] = 0

# Convert the image to a 3-channel grayscale (BGR) image
image_bgr = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

# Apply the watershed algorithm
markers = cv2.watershed(image_bgr, markers)

# Colorize the image based on the watershed result
image_bgr[markers == -1] = [255, 0, 0]

# Convert the image back to HSV color space
tumorImage = cv2.cvtColor(image_bgr, cv2.COLOR_HSV2BGR)

cv2.imshow("TumorLocation", tumorImage)

cv2.waitKey(0)
cv2.destroyAllWindows()