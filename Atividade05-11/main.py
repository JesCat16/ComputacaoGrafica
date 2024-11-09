import cv2
import numpy as np

im0norm = cv2.imread('marcador03.png')
im1norm = cv2.imread('marcador04.png')
im0 = cv2.imread('marcador03.png',cv2.IMREAD_GRAYSCALE)
im1 = cv2.imread('marcador04.png',cv2.IMREAD_GRAYSCALE)
cv2.namedWindow('Original',2)

sift = cv2.SIFT_create(nfeatures = 500,
nOctaveLayers = 10,
contrastThreshold = 0.01,
edgeThreshold = 20,
sigma = 0.5)

keypoints1 ,descritores1 = sift.detectAndCompute(im0, None)
keypoints2 ,descritores2 = sift.detectAndCompute(im1, None)

bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=True)
matches = bf.match(descritores1, descritores2)

imagem_correspondencias = cv2.drawMatches(
im0norm, keypoints1,
im1norm, keypoints2,
matches, None,
flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
cv2.imshow('Original',imagem_correspondencias)

cv2.waitKey(0)