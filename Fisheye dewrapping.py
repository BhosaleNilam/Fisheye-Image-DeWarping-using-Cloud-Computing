#!/usr/bin/env python
# coding: utf-8

# In[4]:


import cv2
import numpy as np
import matplotlib.pyplot as plt
import imageio
import imutils

def main_extract(imgInput, Crop, offset):
    
    # Copying the Image
    img = imgInput

    # Mapping of width and height of Image
    def constructMap(width, height, substract, Betax, Betay):
        map_a = np.zeros((height, width), np.float32)
        map_b = np.zeros((height, width), np.float32)
        i = 1
        while i < int(height):
            for j in range(1, int(width)):
                theta = (float(j-offset) / float(width)) * 2.0 * np.pi
                map_a.itemset((i, j), int(Betax + (float(i) / float(height)) * substract * np.sin(theta)))
                map_b.itemset((i, j), int(Betay + (float(i) / float(height)) * substract * np.cos(theta)))
            i+=1
        return map_a, map_b

    # Extracting and rotating the image
    def extract(img, amap, bmap):
        output = cv2.remap(img, amap, bmap, cv2.INTER_LINEAR)
        Rotated_image = imutils.rotate(output, angle=180)
        return Rotated_image

    # Final Image Size
    Width = int(abs(2.0 * (Crop - img.shape[0]/2 / 2) * np.pi))
    Height = int(abs(Crop - img.shape[0]/2))

    #Calling the constructMap Function
    amap, bmap = constructMap(Width, Height, Crop - img.shape[0]/2, img.shape[0]/2, img.shape[1]/2)

    # Calling the extraction method
    result = extract(img, amap, bmap)
    return result

image = imageio.imread(r'fish_eye.jpg')
plt.imshow(image)
plt.show()
out = main_extract(image, 40, 1500) # Cropping image size to 40 from the bottom and passing 1500 as offset
plt.imshow(out)
plt.show()
imageio.imwrite(r"output.jpg",out)

