# Imports
import pyrealsense2 as rs
from pyniryo import *
import numpy as np
import math
import util
from ultralytics import YOLO

# Load the YOLOv8 model
model = YOLO('../best.pt')

# - Constants
robot_ip_address = "10.10.195.200"

#Regler ça a chaque fois si possible ( si déplacement )
cam_X = 0.165#X
cam_Y = 0.19#Z
cam_Z = 0.365#Y
cam_ROLL = math.pi/2 # rotation par rapport a X
cam_PITCH = math.pi - math.pi/2# rotation par rapport a Z
cam_YAW = 0#rotation par rapport a Y

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

config.enable_stream(rs.stream.depth, 320, 240, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
profile = config.resolve(pipeline)

# Start streaming
pipeline.start(config)

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
First = True

while "User do not press Escape neither Q":

    frames = pipeline.wait_for_frames()

    # Align the depth frame to color frame
    aligned_frames = align.process(frames)
    
    # Get aligned frames
    depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()

    # Getting the depth sensor's depth scale (see rs-align example for explanation)
    depth_sensor = profile.get_device().first_depth_sensor()
    depth_scale = depth_sensor.get_depth_scale()

    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_frame = np.asanyarray(color_frame.get_data())
    
    depth_image = cv2.resize(depth_image,(320,240))
    color_frame = cv2.resize(color_frame,(320,240))

    img = color_frame.copy()

    if First == True:
        depth_before = depth_image
        First = False

    depth_image = (depth_image + depth_before)/2    
    depth_before = depth_image

    # Uncompressing image
    img = cv2.undistort(img, cam_mtx, dist, None, newcam_mtx)
    depth_image = cv2.undistort(depth_image, cam_mtx, dist, None, newcam_mtx)
    # crop the image
    x,y,w,h = roi

    img = img[y:y+h, x:x+w]
    depth_image = depth_image[y:y+h, x:x+w]

    #Code here#################################

    results = model(img,conf=0.8)

    # Visualize the results on the frame
    annotated_frame = results[0].plot()

    result = results[0]
    Rx,Ry,Rz = 0,0,0
    good = False
    if len(result.boxes) > 0:
        box = result.boxes[0]
        x1, y1, x2, y2 = box.xyxy[0]
        conf = box.conf[0]
        classe = box.cls[0]
        #########, y##################################, y
        barycenter_x = int((min(x1,x2) + abs((x2-x1))/2).cpu().numpy())
        barycenter_y = int((min(y1,y2) + 5).cpu().numpy())

        if barycenter_x > 100 and barycenter_x < 300 and barycenter_y > 20 and barycenter_y < 200:
            depth_np = np.array(depth_image)
            moyenne = np.mean(depth_np[barycenter_y+9:barycenter_y+11,barycenter_x-1:barycenter_x+1])
            d = moyenne * depth_scale
            Rx,Ry,Rz = util.calculate_XYZ(barycenter_x,barycenter_y,A,R,T,d)
            Rz = - Rz
            if d < 0.35 and d > 0.15:
                 good = True
        
            # dessine le tout
            annotated_frame = cv2.putText(annotated_frame, "x:"+str(Rx)+", y:"+str(Ry)+", z:"+str(Rz), (barycenter_x-45,barycenter_y+40), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255,0),1)
            annotated_frame = cv2.putText(annotated_frame, "dist:"+str(np.round(d,2)), (barycenter_x-15,barycenter_y+15), cv2.FONT_HERSHEY_SIMPLEX,0.5, (0,255,0),1)       
            annotated_frame = cv2.circle(annotated_frame, (barycenter_x,barycenter_y), 1, color=(0,255,0), thickness=-1)

    if good:
        STOP[0] = STOP[0] + 1
    else:
        STOP[0] = 0
        robot.run_conveyor(conveyor_id)

    if STOP[0] > 2 and TAKEN == True :
        robot.move_pose(PoseObject( x=Rx, y=Ry, z=Rz+0.1, roll=0, pitch=math.pi/2, yaw=0))
        robot.move_pose(PoseObject( x=Rx, y=Ry, z=Rz, roll=0, pitch=math.pi/2, yaw=0))
        robot.grasp_with_tool()

        robot.move_pose(PoseObject( x=Rx, y=Ry, z=Rz+0.1, roll=0, pitch=math.pi/2, yaw=0))
        robot.move_pose(place_haut_pose)

	#check ici

        robot.move_pose(PoseObject( x=0.0, y=0.25, z=0.22, roll=0.0, pitch=1.57, yaw=1.57))
        count = count + 1
        robot.release_with_tool()
        robot.move_pose(place_haut_pose)

        # Moving to observation pose
        robot.move_pose(observation_pose)
        STOP[0] = 0

    if(STOP[0] >= 1):
        robot.stop_conveyor(conveyor_id)

    # Apply colormap on depth image (image must be converted to 8-bit per pixel first)
    depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)

    print(annotated_frame.shape)
    print(depth_colormap.shape)
    img = np.hstack((annotated_frame, depth_colormap))

    # Display the annotated frame
    cv2.imshow("YOLOv8 Inference", img)

    #cv2.imshow("mask", opening)
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break


#########
robot.stop_conveyor(conveyor_id)
robot.unset_conveyor(conveyor_id)
robot.go_to_sleep()
robot.close_connection()

