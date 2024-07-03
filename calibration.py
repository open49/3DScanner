import numpy as np
import cv2

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

objp = np.zeros((7 * 7, 3), np.float32)
objp[:, :2] = np.mgrid[0:7, 0:7].T.reshape(-1, 2)

objpoints = []
imgpoints = []

cap = cv2.VideoCapture(0)
capture = False

def capture_image(event, x, y, flags, param):
    global capture
    if event == cv2.EVENT_LBUTTONDOWN:
        print("Capturing Image...")
        capture = True

cv2.namedWindow('img')
cv2.setMouseCallback('img', capture_image)

while True:
    ret, img = cap.read()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if capture:
        ret, corners = cv2.findChessboardCorners(gray, (7, 7), None)

        if ret:
            corners2 = cv2.cornerSubPix(gray, corners, (11, 11), (-1, -1), criteria)
            imgpoints.append(corners2.tolist())
            objpoints.append(objp)

            img = cv2.drawChessboardCorners(img, (7, 7), corners2, ret)
            cv2.imshow('img', img)
            cv2.waitKey(500)

            capture = False

    cv2.imshow('img', img)

    key = cv2.waitKey(1)

    if key & 0xFF == ord('q'):
        break

# Calibration
ret, img = cap.read()
shape = img.shape[:2]

if len(objpoints) > 0:
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, shape[::-1], None, None)

    # Kích thước pixel
    fcl = mtx[0, 0]
    fcr = mtx[1, 1]

    # Góc quay
    tetl, phil, _ = cv2.Rodrigues(rvecs[0])
    tetr, phir, _ = cv2.Rodrigues(rvecs[1])

    # Toạ độ không gian
    x0l, y0l, z0l = tvecs[0].flatten()
    x0r, y0r, z0r = tvecs[1].flatten()

    # Tiêu cự
    ccddl = dist[0][0]
    ccddr = dist[1][0]

    # In ra các giá trị
    print("\nKích thước pixel:")
    print("fcl:", fcl)
    print("fcr:", fcr)

    print("\nGóc quay:")
    print("tetl:", tetl)
    print("tetr:", tetr)
    print("phil:", phil)
    print("phir:", phir)

    print("\nToạ độ không gian:")
    print("x0l:", x0l)
    print("y0l:", y0l)
    print("z0l:", z0l)
    print("x0r:", x0r)
    print("y0r:", y0r)
    print("z0r:", z0r)

    print("\nTiêu cự:")
    print("ccddl:", ccddl)
    print("ccddr:", ccddr)
else:
    print("No valid calibration images.")

cap.release()
cv2.destroyAllWindows()