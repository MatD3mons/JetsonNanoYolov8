# Imports
import pyrealsense2 as rs
from pyniryo import *
import numpy as np
import math
import util

# - Constants
robot_ip_address = "10.10.195.200"
threshold_area = 100     #threshold area 

#Regler ça a chaque fois si possible ( si déplacement )
cam_X = 0.205#X
cam_Y = 0.198#Z
cam_Z = 0.37#Y
cam_ROLL = math.pi/2 #- math.pi/15 # rotation par rapport a X
cam_PITCH = math.pi - math.pi/2# rotation par rapport a Z
cam_YAW = 0#rotation par rapport a Y

#camera a de base un décalage de pi/2 en X et -pi/2 en Z

# The pose from where the image processing happens
observation_pose = PoseObject( x=0.25, y=0, z=0.3, roll=0, pitch=math.pi/2, yaw=0)
place_haut_pose = PoseObject( x=0.0, y=0.25, z=0.3, roll=0.0, pitch=1.57, yaw=1.57)

# Connect to robot
robot = NiryoRobot(robot_ip_address)
# Calibrate robot if the robot needs calibration
robot.calibrate_auto()
# Updating tool
robot.update_tool()
# Moving to observation pose
robot.move_pose(observation_pose)
# release tool
robot.release_with_tool()
# Get conveyor
conveyor_id = robot.set_conveyor()
# Turning conveyor on
#robot.run_conveyor(conveyor_id)

print("load")

cam_mtx = np.load("np/cam_mtx.npy")
dist = np.load("np/dist.npy")
newcam_mtx = np.load("np/newcam_mtx.npy")
roi = np.load("np/roi.npy")

# Variable vision
A = newcam_mtx
R = util.get_rotation_matrix(roll=cam_ROLL,pitch=cam_PITCH,yaw=cam_YAW) 
T = np.array([[cam_X,cam_Y,cam_Z]]).T

# Configure depth and color streams
pipeline = rs.pipeline()
config = rs.config()

config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 960, 540, rs.format.bgr8, 30)
profile = config.resolve(pipeline)

# Start streaming
pipeline.start(config)

# Declare sensor object and set options
#depth_sensor = profile.get_device().first_depth_sensor()
#depth_sensor.set_option(rs.option.visual_preset, 5) # 5 is short range, 3 is low ambient light

#Pour mettre la courte distance, attention elle sauvegarde après dans sa mémoire.
sensor = pipeline.get_active_profile().get_device().query_sensors()[0]
sensor.set_option(rs.option.min_distance, 0)
sensor.set_option(rs.option.enable_max_usable_range,0)

# Create an align object
align_to = rs.stream.color
align = rs.align(align_to)

STOP = [0]
TAKEN = True
count = 0
size = 0.01

while "User do not press Escape neither Q":

    frames = pipeline.wait_for_frames()

    # Align the depth frame to color frame
    aligned_frames = align.process(frames)
    
    # Get aligned frames
    depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
    color_frame = aligned_frames.get_color_frame()

    # Getting the depth sensor's depth scale (see rs-align example for explanation)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()

    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_frame = np.asanyarray(color_frame.get_data())
    
    depth_image_dim = depth_image.shape
    color_frame_dim = color_frame.shape

    img = color_frame.copy()

    # Uncompressing image
    img = cv2.undistort(img, cam_mtx, dist, None, newcam_mtx)
    depth_image = cv2.undistort(depth_image, cam_mtx, dist, None, newcam_mtx)
    # crop the image
    x,y,w,h = roi

    img = img[y:y+h, x:x+w]
    depth_image = depth_image[y:y+h, x:x+w]

    #Code here#################################

    #contours, _ = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_NONE)
    img_hsv=cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    
    #Red mask
    # lower = np.array([160,50,0])
    # upper = np.array([190,255,255])
    # r1 = cv2.inRange(img_hsv, lower, upper)
    # # join my masks
    # thresh = cv2.threshold(r1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # # Morph open with a elliptical shaped kernel
    # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
    # o1 = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    #####################################################################
    #Green mask
    lower = np.array([55,100,0])
    upper = np.array([85,255,255])
    r2 = cv2.inRange(img_hsv, lower, upper)
    # join my masks
    thresh = cv2.threshold(r2, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Morph open with a elliptical shaped kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
    o2 = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)
    #####################################################################
    #Blue mask           
    lower = np.array([100,100,0])
    upper = np.array([120,255,255])
    r3 = cv2.inRange(img_hsv, lower, upper)
    # join my masks
    thresh = cv2.threshold(r3, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Morph open with a elliptical shaped kernel
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (7,7))
    o3 = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=3)

    ######################################################################
    opening = o2 + o3
    
    # Find contours and create perfect circle on mask
    cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = cnts[0] if len(cnts) == 2 else cnts[1]
    ###########################################
    Rx,Ry,Rz = 0,0,0
    for cnt in cnts:
        cnt = cnts[0]
        area = cv2.contourArea(cnt)        
        if area < threshold_area:
            continue
        # récupère le centre d'une forme
        barycenter_x, barycenter_y = get_contour_barycenter(cnt)
       
        if barycenter_x < 300 or barycenter_x > 560 or barycenter_y < 200 or barycenter_y > 800:
            continue 

        cv2.drawContours(img,cnt,-1,(60,255,255),4)

        d = depth_image[barycenter_y,barycenter_x] * depth_scale
        Rx,Ry,Rz = util.calculate_XYZ(barycenter_x,barycenter_y,A,R,T,d)
        Rz = - Rz
        # dessine le tout
        img = draw_barycenter(img, barycenter_x, barycenter_y)
        #img = cv2.putText(img, str(barycenter_x)+", "+str(barycenter_y), (barycenter_x-15,barycenter_y-15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255),1)
        img = cv2.putText(img, "x:"+str(Rx)+", y:"+str(Ry)+", z:"+str(Rz), (barycenter_x-45,barycenter_y-40), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255),1)    
        img = cv2.putText(img, "dist:"+str(np.round(d,3)), (barycenter_x-15,barycenter_y-15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,0,255),1)
    
        #robot.move_pose(PoseObject( x=Rx, y=Ry, z=0.25, roll=0, pitch=math.pi/2, yaw=0))       

    if TAKEN == True:
        if Rx != 0:
            STOP[0] = STOP[0] + 1
        else:
            STOP[0] = 0
            robot.run_conveyor(conveyor_id)

        if(STOP[0] > 2):
            robot.move_pose(PoseObject( x=Rx, y=Ry, z=Rz, roll=0, pitch=math.pi/2, yaw=0))
            robot.grasp_with_tool()

            robot.move_pose(PoseObject( x=Rx, y=Ry, z=Rz+0.1, roll=0, pitch=math.pi/2, yaw=0))
            #robot.wait(1)
            robot.move_pose(place_haut_pose)
            robot.move_pose(PoseObject( x=0.0, y=0.25, z=0.135+count*size, roll=0.0, pitch=1.57, yaw=1.57))
            count = count + 1
            robot.release_with_tool()
            robot.move_pose(place_haut_pose)

            # Moving to observation pose
            robot.move_pose(observation_pose)
            #robot.wait(0.5)
            STOP[0] = 0

        if(STOP[0] >= 1):
            robot.stop_conveyor(conveyor_id)
            #robot.wait(0.1)

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    img = np.hstack((img, depth_colormap))

    #print("show")
    cv2.imshow("debug", img)
    #cv2.imshow("mask",opening)

    #cv2.imshow("mask", opening)
    if cv2.waitKey(30) in [27, ord("q")]: # Will break loop if the user press Escape or Q
        break


#########
robot.stop_conveyor(conveyor_id)
robot.unset_conveyor(conveyor_id)
robot.go_to_sleep()
robot.close_connection()

