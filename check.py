import cv2
import numpy as np

def calibrate_camera(images, chessboard_size):
    # Prepare object points, like (0,0,0), (1,0,0), (2,0,0), ..., (6,5,0)
    objp = np.zeros((chessboard_size[0] * chessboard_size[1], 3), np.float32)
    objp[:, :2] = np.mgrid[0:chessboard_size[0], 0:chessboard_size[1]].T.reshape(-1, 2)

    # Arrays to store object points and image points from all the images.
    objpoints = []  # 3D points in real world space
    imgpoints = []  # 2D points in image plane.

    for image in images:
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Find the chessboard corners
        ret, corners = cv2.findChessboardCorners(gray, chessboard_size, None)

        # If found, add object points, image points (after refining them)
        if ret:
            objpoints.append(objp)

            corners2 = cv2.cornerSubPix(
                gray, corners, (11, 11), (-1, -1), criteria=(cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
            )
            imgpoints.append(corners2)

    # Perform camera calibration
    ret, mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

    # Extract relevant parameters
    Hres, Vres = gray.shape[::-1]
    fcl = mtx[0, 0]
    fcr = mtx[1, 1]
    ccddl = (mtx[0, 2], mtx[1, 2])

    # Assuming tetl, tetr, phil, phir, x0l, x0r, y0l, y0r, z0l, z0r from rvecs and tvecs
    tetl, tetr, phil, phir = rvecs[0], rvecs[1], rvecs[2], rvecs[3]
    x0l, x0r, y0l, y0r, z0l, z0r = tvecs[0], tvecs[1], tvecs[2], tvecs[3], tvecs[4], tvecs[5]

    return Hres, Vres, fcl, fcr, tetl, tetr, phil, phir, x0l, x0r, y0l, y0r, z0l, z0r, ccddl

# Example usage
# Replace 'images_path' with the path to your images and adjust 'chessboard_size' based on the dimensions of your calibration pattern
images_path = "path/to/your/images/"



# CHÚ Ý: ĐỔI TÊN CHỖ NÀY
image_names = [f"CAM1-{i:02d}.png" for i in range(1, 43)]
#image_names = [f"CAM0-{i:02d}.png" for i in range(1, 43)]

images = [cv2.imread(images_path + image_name) for image_name in image_names]
chessboard_size = (7, 7)  # Modify according to your calibration pattern

Hres, Vres, fcl, fcr, tetl, tetr, phil, phir, x0l, x0r, y0l, y0r, z0l, z0r, ccddl = calibrate_camera(images, chessboard_size)

# Print or use the obtained parameters as needed
print("Hres:", Hres)
print("Vres:", Vres)
print("fcl:", fcl)
print("fcr:", fcr)
print("tetl:", tetl)
print("tetr:", tetr)
print("phil:", phil)
print("phir:", phir)
print("x0l:", x0l)
print("x0r:", x0r)
print("y0l:", y0l)
print("y0r:", y0r)
print("z0l:", z0l)
print("z0r:", z0r)
print("ccddl:", ccddl)

