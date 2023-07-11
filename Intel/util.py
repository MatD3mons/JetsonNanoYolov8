import numpy as np
import math
import cv2

#Function
def _get_roll_matrix(theta_x: float = 0.0) -> np.ndarray:
    return np.array(
        [   [1.0, 0.0, 0.0],
            [0.0, np.cos(theta_x), -np.sin(theta_x)],
            [0.0, np.sin(theta_x), np.cos(theta_x)],])

def _get_pitch_matrix(theta_y: float = 0.0) -> np.ndarray:
    theta_y = theta_y - math.pi/2
    return np.array(
        [   [np.cos(theta_y), 0.0, np.sin(theta_y)],
            [0.0, 1.0, 0.0],
            [-np.sin(theta_y), 0.0, np.cos(theta_y)],])

def _get_yaw_matrix(theta_z: float = 0.0) -> np.ndarray:
    return np.array(
        [   [np.cos(theta_z), -np.sin(theta_z), 0.0],
            [np.sin(theta_z), np.cos(theta_z), 0.0],
            [0.0, 0.0, 1.0],])

def get_rotation_matrix(roll: float = 0.0, pitch: float = 0.0, yaw: float = 0.0) -> np.ndarray:
    # Roll
    Rx = _get_roll_matrix(roll)
    # Pitch
    Ry = _get_pitch_matrix(pitch)
    # Yaw
    Rz = _get_yaw_matrix(yaw)
    return Rz @ Ry @ Rx

#https://www.fdxlabs.com/calculate-x-y-z-real-world-coordinates-from-a-single-camera-using-opencv/
def calculate_XYZ(u,v,A,R,T,distance):                  
        #Solve: From Image Pixels, find World Points
        x=np.array([[u,v,1]], dtype=np.float32) * distance#1 3
        x= x.T # 3 1 #. By dividing the matrix product by z c {\displaystyle z_{c}}, the z-coordinate of the camera relative to the world origin, the theoretical value for the pixel coordinates can be found.
        #suv_1=self.scalingfactor*uv_1 #TODO multriply by facteur ?
        x= np.linalg.inv(A).dot(x) # 3 1
        x=x-T # 3 4
        x = -R.T.dot(x)
        #x = np.linalg.inv(R).dot(x)
        x = x.T[0]
        x,y,z = round(x[0],2),round(x[1],2),round(x[2],2)
        return x,y,z

