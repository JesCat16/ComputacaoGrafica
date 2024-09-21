import cv2

def capturar_clique(event, x,y, flags, param):

    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordenadas do clique: X={x*0.004125}, Y={y*0.004125}")



# Lê a imagem
imagem1 = cv2.imread('C:/Users/unifjjesus/Documents/img1_x1_B0.8.jpeg',1)
imagem2 = cv2.imread('C:/Users/unifjjesus/Documents/img1_x2_B0.8.jpeg',1)

alt1 = imagem1.shape[0]
lar1 = imagem1.shape[1]

alt2 = imagem2.shape[0]
lar2 = imagem2.shape[1]

x1 = int(lar1/2)
y1 = int(alt1/2)

x2 = int(lar2/2)
y2 = int(alt2/2)



# Exibe a imagem em uma janela
cv2.imshow('Imagem1', imagem1)
cv2.imshow('Imagem2', imagem2)

cv2.setMouseCallback('Imagem1',capturar_clique)
cv2.setMouseCallback('Imagem2',capturar_clique)

# Aguarda uma tecla ser pressionada
cv2.waitKey(0)
# Fecha todas as janelas abertas
cv2.destroyAllWindows()