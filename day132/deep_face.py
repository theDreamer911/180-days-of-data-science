# Tutorial_from_Data_Magic_Youtube
# pip install deepface

# Import modules
import matplotlib.pyplot as plt
from deepface import DeepFace
import cv2

# Import pictures
img = cv2.imread('arya.jpg')
plt.imshow(img[:, :, ::-1])
plt.show()

# Analyze images
result = DeepFace.analyze(img, actions=['emotion'])

print(result)
