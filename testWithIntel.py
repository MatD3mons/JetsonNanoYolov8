import cv2
from ultralytics import YOLO
import numpy as np
import pyrealsense2 as rs

# Load the YOLOv8 model
model = YOLO('best.onnx')

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


# Loop through the video frames
while "User do not press Escape neither Q":
    # Read a frame from the video
    frames = pipeline.wait_for_frames()

    # Align the depth frame to color frame
    aligned_frames = align.process(frames)

    # Get aligned frames
    depth_frame = aligned_frames.get_depth_frame()
    color_frame = aligned_frames.get_color_frame()

    # Convert images to numpy arrays
    depth_image = np.asanyarray(depth_frame.get_data())
    color_frame = np.asanyarray(color_frame.get_data())

    #depth_image = cv2.resize(depth_image,(160,120))
    color_frame = cv2.resize(color_frame,(320,240))

    # Run YOLOv8 inference on the frame
    results = model(color_frame)#, conf=0.8)

    # Visualize the results on the frame
    annotated_frame = results[0].plot()

    # Display the annotated frame
    cv2.imshow("YOLOv8 Inference", annotated_frame)

    # Break the loop if 'q' is pressed
    if cv2.waitKey(10) & 0xFF == ord("q"):
        break

#close the display window
cv2.destroyAllWindows()
pipeline.stop()
