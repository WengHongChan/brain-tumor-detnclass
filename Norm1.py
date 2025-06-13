import numpy as np
import matplotlib.pyplot as plt
import cv2

# Load the grayscale image
image_data = plt.imread('Test1/qweXNorm.jpg')

# Normalize the image
normalized_image = image_data / 255.0

# Plot the original and normalized images side by side
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 5))

# Plot the original image
ax1.imshow(image_data, cmap='gray')
ax1.set_title('Original Image')

# Plot the normalized image
ax2.imshow(normalized_image)
ax2.set_title('Normalized Image')

# Hide the axes ticks
ax1.set_xticks([])
ax1.set_yticks([])
ax2.set_xticks([])
ax2.set_yticks([])

# Show the plot
plt.show()