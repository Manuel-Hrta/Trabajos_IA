import cv2 as cv
import numpy as np


cap= cv.VideoCapture(0)

while(True):
    ret,img =cap.read()
    if(ret == True):
        cv.imshow('marco', img)
        x,y = img.shape[:2]
        img2 = np.zeros((x,y), dtype='uint8')
        
        # hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
        # cv.imshow('hsv', hsv)
        b,g,r = cv.split(img)
        bm = cv.merge([b, img2, img2])
        gm = cv.merge([img2, g, img2])
        rm = cv.merge([img2, img2, r])

        cv.imshow('b', bm)
        cv.imshow('g', gm)
        cv.imshow('r', rm)


        k=cv.waitKey(1) & 0xFF
        if k == 27 :
            break
    else:
        break
cap.release()
cv.destroyAllWindows()



# img = cv.imread('perrito.jpg', 0)
# print(img.shape)
# x,y = img.shape
# img2= np.zeros((x*2, y*2), dtype='uint8')
# for i in range(x):
#     for j in range(y):
#         img2[i*2, j*2]=img[i,j]
# cv.imshow('img', img)
# cv.imshow('img2', img2)
# cv.waitKey()
# cv.destroyAllWindows()



# img = cv.imread('perrito.jpg', 1)
# gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
# rgb = cv.cvtColor(img, cv.COLOR_BGR2RGB)
# hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# cv.imshow('img', img)
# cv.imshow('gray', gray)
# cv.imshow('rgb', rgb)
# cv.imshow('hsv', hsv)

# cv.waitKey(0)
# cv.destroyAllWindows()