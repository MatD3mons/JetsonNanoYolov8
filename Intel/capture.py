# Imports
import pyrealsense2 as rs
from pyniryo import *
import numpy as np
import cv2
import os

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

dir = 'images'
if not os.path.exists(dir):
    os.makedirs(dir)

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

# Get device product line for setting a supporting resolution
pipeline_wrapper = rs.pipeline_wrapper(pipeline)
pipeline_profile = config.resolve(pipeline_wrapper)
device = pipeline_profile.get_device()
device_product_line = str(device.get_info(rs.camera_info.product_line))

found_rgb = False
for s in device.sensors:
    if s.get_info(rs.camera_info.name) == 'RGB Camera':
        found_rgb = True
        break
if not found_rgb:
    print("The demo requires Depth camera with Color sensor")
    exit(0)

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)

if device_product_line == 'L500':
    config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
else:
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)


i = 0
try:
    while True:
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()

        # Uncompressing image
        color_frame = np.asanyarray(color_frame.get_data())
        img = color_frame.copy()
        resized_color_image = cv2.resize(img, dsize=(300,300), interpolation=cv2.INTER_AREA)

        gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
        ret, corners = cv2.findChessboardCorners(gray, (9,6),None)
        if ret == True:
            # Draw and display the corners
            cv2.drawChessboardCorners(img, (9,6), corners,ret)
        #img_test = undistort_image(img_raw, mtx, dist)
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', img)

        if cv2.waitKey(1) in [27, ord("q")]: # Will break loop if the user press Escape or Q
            break

        if cv2.waitKey(1) == ord('a'): # Will break loop if the user press Escape or a
            cv2.imwrite("images/Capture_"+str(i)+".png", color_frame)
            print("print "+str(i))
            i = i + 1

finally:

    # Stop streaming
    pipeline.stop()