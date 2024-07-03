import cv2
import os
import numpy as np  # Import NumPy here to resolve the NameError
import pandas as pd

Hres = 1280.0  # Horizontal resolution of camera Microsoft lifecam cinema
Vres = 720.0  # Vertical resolution of camera

CV_CAP_PROP_BRIGHTNESS = 10
CV_CAP_PROP_CONTRAST = 11
CV_CAP_PROP_SATURATION = 12
CV_CAP_PROP_EXPOSURE = 15
CV_CAP_PROP_WHITE_BALANCE = 17

# video capture right camera
video_capture0 = cv2.VideoCapture(3)
video_capture0.set(CV_CAP_PROP_BRIGHTNESS, 30.0)
video_capture0.set(CV_CAP_PROP_CONTRAST, 5.0)
video_capture0.set(CV_CAP_PROP_SATURATION, 100.0)
video_capture0.set(CV_CAP_PROP_EXPOSURE, -8.0)
video_capture0.set(CV_CAP_PROP_WHITE_BALANCE, 10000.0)

print(video_capture0.get(4))
video_capture0.set(3, Hres)
video_capture0.set(4, Vres)
print(video_capture0.get(4))

# video capture left camera
video_capture1 = cv2.VideoCapture(2)
print(video_capture1.get(4))
video_capture1.set(3, Hres)
video_capture1.set(4, Vres)
print(video_capture1.get(4))
print(video_capture1.get(9))

video_capture1.set(CV_CAP_PROP_BRIGHTNESS, 30.0)
video_capture1.set(CV_CAP_PROP_CONTRAST, 5.0)
video_capture1.set(CV_CAP_PROP_SATURATION, 100.0)
video_capture1.set(CV_CAP_PROP_EXPOSURE, -8.0)
video_capture1.set(CV_CAP_PROP_WHITE_BALANCE, 10000.0)

# show frames from cameras
ret, frame0 = video_capture0.read()
cv2.imshow("cam0", frame0)
ret, frame1 = video_capture1.read()
cv2.imshow("cam1", frame1)
cv2.waitKey(3000)

ret, frame0 = video_capture0.read()
cv2.waitKey(100)
ret, frame1 = video_capture1.read()
cv2.waitKey(100)

cv2.destroyAllWindows()
horzlino = 1280
vertlino = 720
for ii in range(0, 19):
    print(ii, video_capture1.get(ii))

# open a borderless window for showing projector images as a second display
cv2.namedWindow("Projector Window", cv2.WND_PROP_FULLSCREEN)
cv2.setWindowProperty("Projector Window", 0, 1)
cv2.resizeWindow("Projector Window", 2048, 1420)

imggray = np.load('proj.npy') 

# Capture images from left and right cameras after showing the pattern in the projector
for x in range(1, 43):
    cv2.imshow("Projector Window", imggray[:, :, x - 1])
    filename0 = 'CAMR/CAM0-%02d.png' % (x,)
    filename1 = 'CAML/CAM1-%02d.png' % (x,)
    print(filename0)
    print(filename1)
    print(imggray[:, :, x - 1])
    df = pd.DataFrame(imggray[:, :, x - 1], index=None)
    rows = len(df.axes[0])
    cols = len(df.axes[1])
    print("Number of Rows: ", rows)
    print("Number of Columns: ", cols)
    
      
    ret, frame0 = video_capture0.read()
    cv2.waitKey(100)
    ret, frame1 = video_capture1.read()
    cv2.waitKey(100)
    cv2.imwrite(filename0, frame0)
    cv2.imwrite(filename1, frame1)

video_capture0.release()
video_capture1.release()
cv2.destroyAllWindows()
print('pcapture Done!')