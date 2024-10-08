import cv2
import numpy as np
# Carregar a imagem
imagem = cv2.imread('low-contrast01.png')
# Converter a imagem para escala de cinza
imagem_gray = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)
#-----------------------------------------------------------
#Normaliza a imagem
imagem_normalizada = imagem_gray / 255.0
im_result = np.power(imagem_normalizada, 0.5)
#-----------------------------------------------------------
#Média da Imagem
kernel = np.ones((3, 3), np.float32) / 9
imagem_filtrada = cv2.filter2D(imagem_normalizada, -1, kernel)
#retorna a ser imagem
imagem_filtrada = np.uint8(imagem_filtrada * 255)
imagem_filtrada = cv2.medianBlur(imagem_gray, 3)
#-----------------------------------------------------------
#Equaliza a Imagem
imagem_equalizada = cv2.equalizeHist(imagem_gray)
#-----------------------------------------------------------
#Imagem binarizada ou segmentada
#limiar_minimo = 127 # Valor do limiar
#limiar_maximo = 255 # Valor máximo (cor branca)
#imagem_binarizada = cv2.threshold(imagem_gray,limiar_minimo, limiar_maximo, cv2.THRESH_BINARY)
#-----------------------------------------------------------
#Calculo do limiar de imagem
bordas_laplacianas = cv2.Laplacian(imagem_gray, cv2.CV_64F)
#Com bordas:
bordas_laplacianas = cv2.convertScaleAbs(bordas_laplacianas)
#----------------------------------------------------------
#Calcular limiar com o filtro Sobel
#X:
sobelx = cv2.Sobel(imagem_gray, cv2.CV_64F, 1, 0, ksize=3)
#Y:
sobely = cv2.Sobel(imagem_gray, cv2.CV_64F, 0, 1, ksize=3)
#Normalizando:
sobelx = cv2.convertScaleAbs(sobelx)
sobely = cv2.convertScaleAbs(sobely)
#Combinando sobely x e y em uma só imagem:
sobe_combined = cv2.addWeighted(sobelx, 0.5, sobely, 0.5, 0)
#-----------------------------------------------------------

# Exibir a imagem em escala de cinza
cv2.imshow('Imagem em Escala de Cinza', sobe_combined)
#print(imagem_binarizada)
cv2.waitKey(0)
cv2.destroyAllWindows()