import numpy as np
import cv2
import os
import glob

def imgdesig(img1, img2):  # define a function for getting dark and light pattern
    old_settings = np.seterr(all='ignore')
    img1 = cv2.imread(img1, cv2.IMREAD_GRAYSCALE)
    ret, img1 = cv2.threshold(img1, 10, 255, cv2.THRESH_TOZERO)
    img2 = cv2.imread(img2, cv2.IMREAD_GRAYSCALE)
    ret, img2 = cv2.threshold(img2, 10, 255, cv2.THRESH_TOZERO)
    threshold_img = (((img1 // 2) + (img2 // 2)))

    img123 = (np.divide(img1, threshold_img))
    img123 = img123.astype(np.int16)
    
    finalImg  = (np.divide(img123, img123))
    finalImg = finalImg.astype(np.int16)

    return finalImg

def process_images(directory, output_filename):
    img_names = glob.glob(directory + "*.png")
    vertlino = 720
    horzlino = 1280

    grayimg = np.zeros((vertlino, horzlino), dtype=np.int16)
    camcode = np.zeros((vertlino, horzlino, 2), dtype=np.int16) 
    imgbin3 = np.zeros((vertlino, horzlino, 3), dtype=np.int8)

    for ii in range(3, 22, 2):
        xx = ii - 3
        xx = xx // 2
        filename1 = img_names[ii]
        filename2 = img_names[ii - 1]
        ff = imgdesig(filename1, filename2)
        print('processing %s...' % filename1, (2 ** xx))
        grayimg = grayimg + (2 ** xx) * ff

    for ii in range(0, horzlino):
        for jj in range(0, vertlino):
            camcode[jj][ii][0] = grayimg[jj][ii]
            imgbin3[jj][ii][1] = grayimg[jj][ii] % 256
            imgbin3[jj][ii][2] = 40 * grayimg[jj][ii] / 256
            imgbin3[jj][ii][0] = 4

    img1 = (grayimg % 255)
    cv2.imshow("PWindow2", imgbin3)
    cv2.waitKey(100)

    img1 = cv2.imread(img_names[0], cv2.IMREAD_GRAYSCALE)
    grayimg = (img1 * 0) + 1023
    grayimg = grayimg * 0
    for ii in range(23, 42, 2):
        xx = ii - 22
        xx = xx // 2
        filename1 = img_names[ii]
        filename2 = img_names[ii - 1]
        ff = imgdesig(filename1, filename2)
        print('processing %s...' % filename1, (2 ** xx))
        grayimg = grayimg + (2 ** xx) * ff

    for ii in range(0, horzlino):
        for jj in range(0, vertlino):
            camcode[jj][ii][1] = grayimg[jj][ii]
            imgbin3[jj][ii][0] = (imgbin3[jj][ii][0] + grayimg[jj][ii] % 256) % 256
            imgbin3[jj][ii][2] = 40 * (imgbin3[jj][ii][2] + grayimg[jj][ii] % 256) // 80
            imgbin3[jj][ii][1] = 4

    img1 = (grayimg % 255)
    cv2.imshow("PWindow2", imgbin3)
    cv2.waitKey(2000)

    np.save(output_filename, camcode)
    cv2.destroyAllWindows()
    print('Images processing Done!')

# Process the right camera images
process_images("CAMR/", "CAMR/coloccod.npy")

# Process the left camera images
process_images("CAML/", "CAML/coloccod.npy")
