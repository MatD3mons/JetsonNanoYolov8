#https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_calib3d/py_calibration/py_calibration.html#calibration

import numpy as np
import cv2
import glob
import os

CHECKERBOARD = (9,6)

dir = 'np'
if not os.path.exists(dir):
    os.makedirs(dir)

print(">==> Starting Setup")
# termination criteria
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

# prepare object points, like (0,0,0), (1,0,0), (2,0,0) ....,(6,5,0)
objp = np.zeros((CHECKERBOARD[0]*CHECKERBOARD[1],3), np.float32)
objp[:,:2] = np.mgrid[0:CHECKERBOARD[0], 0:CHECKERBOARD[1]].T.reshape(-1, 2)

# Arrays to store object points and image points from all the images.
objpoints = [] # 3d point in real world space
imgpoints = [] # 2d points in image plane.

images = glob.glob('images/*.png')

for fname in images:
    img = cv2.imread(fname)
    img = cv2.resize(img,(320,240))
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    # Find the chess board corners
    ret, corners = cv2.findChessboardCorners(gray, (9,6),None)

    # If found, add object points, image points (after refining them)
    if ret == True:
        print("good")
        objpoints.append(objp)
        cv2.cornerSubPix(gray,corners,(3,3),(-1,-1),criteria)
        imgpoints.append(corners)

        # Draw and display the corners
        cv2.drawChessboardCorners(img, (9,6), corners,ret)
        cv2.imshow('img',img)
        cv2.waitKey(500)

cv2.destroyAllWindows()

print(">==> Starting calibration")
ret, cam_mtx, dist, rvecs, tvecs = cv2.calibrateCamera(objpoints, imgpoints, gray.shape[::-1], None, None)

#print(ret)
print("Camera Matrix")
print(cam_mtx)
np.save('np/cam_mtx.npy', cam_mtx)

print("Distortion Coeff")
print(dist)
np.save('np/dist.npy', dist)

print(">==> Calibration ended")


h, w = img.shape[:2]
DIM = (w,h)
print("Image Width, Height")
print(DIM)
#if using Alpha 0, so we discard the black pixels from the distortion.  this helps make the entire region of interest is the full dimensions of the image (after undistort)
#if using Alpha 1, we retain the black pixels, and obtain the region of interest as the valid pixels for the matrix.
#i will use Apha 1, so that I don't have to run undistort.. and can just calculate my real world x,y
newcam_mtx, roi =cv2.getOptimalNewCameraMatrix(cam_mtx, dist, DIM, 1, DIM)

print("Region of Interest")
print(roi)
np.save('np/roi.npy', roi)

print("New Camera Matrix")
print(newcam_mtx)
np.save('np/newcam_mtx.npy', newcam_mtx)
print(np.load('np/newcam_mtx.npy'))

inverse = np.linalg.inv(newcam_mtx)
print("Inverse New Camera Matrix")
print(inverse)

# undistort
undst = cv2.undistort(img, cam_mtx, dist, None, newcam_mtx)

# crop the image
x,y,w,h = roi
undst = undst[y:y+h, x:x+w]

cv2.imshow('img1', img) 
cv2.imshow('img1_undst', undst)
cv2.waitKey(0)
cv2.destroyAllWindows()
