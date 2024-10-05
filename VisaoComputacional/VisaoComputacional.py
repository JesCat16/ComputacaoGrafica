import cv2
import numpy as np

im0 = cv2.imread('low-contrast01.png',cv2.IMREAD_GRAYSCALE)

cv2.namedWindow('Original',2)
cv2.imshow('Original',im0)


#im_result = np.power(im0/255.0, 0.0) * 255.0
#im_result = 255 - im0
#im_result = im_result.astype(np.uint8)

im1_equalizada = cv2.blur(im0,(5,5))

cv2.namedWindow('resultado',2)
cv2.imshow('resultado', im1_equalizada)










cv2.waitKey(0)