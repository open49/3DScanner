import numpy as np
import cv2
import os
import glob

horzlino=1280
vertlino=720
img_names = glob.glob("CAML/*.png")
img1=cv2.imread(img_names[0],cv2.IMREAD_GRAYSCALE)
ii=50
# adjusting the threshold for processing area and eliminating shadows
# use 'a' and 'd' key to adjust and press 'q' when finished
textColor = (0, 0, 0) 
while True:
    ret,img1th = cv2.threshold(img1,ii,255,cv2.THRESH_TOZERO)
    cv2.rectangle(img1th,(1,1),(1050,55),255,-1)
    cv2.putText(img1th,"Use 'a' 'd' keys and 'q' when finished, Threshold is "+str(ii), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, textColor)
    cv2.imshow("PWindow2",img1th)
    k = cv2.waitKey(0)  
    if k == 113:
        break
    elif k == 100:
        ii=ii+1
    elif k == 97:
        ii=ii-1

cv2.destroyAllWindows()

np.save("thresholdleft" , ii)
    
img_names = glob.glob("CAMR/*.png")
img1=cv2.imread(img_names[0],cv2.IMREAD_GRAYSCALE)
ii=50
while True:
    ret,img1th = cv2.threshold(img1,ii,255,cv2.THRESH_TOZERO)
    cv2.rectangle(img1th,(1,1),(1050,55),255,-1)
    cv2.putText(img1th,"Use 'a' 'd' keys and 'q' when finished, Threshold is "+str(ii), (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, textColor)
    cv2.imshow("PWindow2",img1th)
    k = cv2.waitKey(0)  
    if k == 113:
        break
    elif k == 100:
        ii=ii+1
    elif k == 97:
        ii=ii-1
        

cv2.destroyAllWindows()
np.save("thresholdright" , ii)
print ('Threshold Done!')
