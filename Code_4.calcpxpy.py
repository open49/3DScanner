import numpy as np
import cv2
import os
import glob
import operator

old_settings = np.seterr(all='ignore')

horzlino = 1280
vertlino = 720

Direct = "CAMR/"
rightcamcode = np.load(os.path.join(Direct, "coloccod.npy"))
Direct = "CAML/"
leftcamcode = np.load(os.path.join(Direct, "coloccod.npy"))

thresholdleft = np.load("thresholdleft.npy")
thresholdright = np.load("thresholdright.npy")

# Convert thresholds to the appropriate data type
thresholdleft = thresholdleft.astype(np.float64)
thresholdright = thresholdright.astype(np.float64)

imgmaskrightf = "CAMR/CAM0-01.png"
img1 = cv2.imread(imgmaskrightf, cv2.IMREAD_GRAYSCALE)
ret, img1 = cv2.threshold(img1, float(thresholdright), 255, cv2.THRESH_TOZERO)
imgmaskright = np.divide(img1, img1)

imgmaskleftf = "CAML/CAM1-01.png"
img1 = cv2.imread(imgmaskleftf, cv2.IMREAD_GRAYSCALE)
ret, img1 = cv2.threshold(img1, float(thresholdleft), 255, cv2.THRESH_TOZERO)
imgmaskleft = np.divide(img1, img1)

kkl = 0
kkr = 0
colocright = []
colocleft = []

leftsrt = []
rightsrt = []

# finding similar points in both cameras based on projected pattern
for ii in range(0, horzlino):
    for jj in range(0, vertlino):
        if (rightcamcode[jj][ii][0] != 0 and rightcamcode[jj][ii][1] != 0 and imgmaskright[jj][ii] != 0):
            colocright.append(np.uint32([rightcamcode[jj][ii][0] + rightcamcode[jj][ii][1] * 1024, ii, jj]))
            rightsrt.append(rightcamcode[jj][ii][0] + rightcamcode[jj][ii][1] * 1024)
            kkl += 1
        if (leftcamcode[jj][ii][0] != 0 and leftcamcode[jj][ii][1] != 0 and imgmaskleft[jj][ii] != 0):
            colocleft.append(np.uint32([leftcamcode[jj][ii][0] + leftcamcode[jj][ii][1] * 1024, ii, jj]))
            leftsrt.append(leftcamcode[jj][ii][0] + leftcamcode[jj][ii][1] * 1024)
            kkr += 1

print("total points on right and left cameras", kkr, kkl)
np.savetxt("leftcod", colocleft, fmt='%d', delimiter=', ', newline='\n')
np.savetxt("rightcod", colocright, fmt='%d', delimiter=', ', newline='\n')

colocrightsrt = sorted(colocright, key=operator.itemgetter(0))
colocleftsrt = sorted(colocleft, key=operator.itemgetter(0))
rightsrtt = sorted(rightsrt)
leftsrtt = sorted(leftsrt)

kkr = 0
np.save("colocrightsrt", colocrightsrt)
np.save("colocleftsrt", colocleftsrt)
newlistl = np.unique(leftsrtt)
np.savetxt("colocleftsrtuniq", newlistl, fmt='%d', delimiter=', ', newline='\n')
newlistr = np.unique(rightsrtt)
np.savetxt("colocrightsrtuniq", newlistr, fmt='%d', delimiter=', ', newline='\n')

# finding common points in both cameras
camunio = np.intersect1d(newlistl, newlistr)

kkl = 0
kkr = 0
kk = 0
matchpixels = np.zeros((np.size(camunio), 4), dtype=np.int16)

for i in camunio:
    while newlistr[kkr] != i:
        kkr += 1
    matchpixels[kk][0] = colocrightsrt[kkr][1]  # right camera x pixel coordinate
    matchpixels[kk][1] = colocrightsrt[kkr][2]  # right camera y pixel coordinate
    while newlistl[kkl] != i:
        kkl += 1
    matchpixels[kk][2] = colocleftsrt[kkl][1]  # left camera x pixel coordinate
    matchpixels[kk][3] = colocleftsrt[kkl][2]  # left camera y pixel coordinate
    kk += 1

np.savetxt("colocuniq", matchpixels, fmt='%d', delimiter=',', newline='\n')
print('Stereo matching Done!')
