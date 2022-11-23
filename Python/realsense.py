import pyrealsense2 as rs
import numpy as np
import cv2
import vision

# Configure puck and stage tracking
pT = vision.puckTracker()
perception_corrected = False

# Configure color streams
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
    print("Could not detect the Color sensor")
    exit(0)

config.enable_stream(rs.stream.color, 1280, 720, rs.format.bgr8, 30)

# Start streaming
pipeline.start(config)

try:
    while True:

        # Wait for a coherent color frame
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert image to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())

        if not perception_corrected:
            isSuccess, res = pT.locateStage(color_image,showTags=False)
            if not isSuccess:
                # print(res)
                continue

            framed_image, cornerLocs = pT.frameStage(color_image, res, showFramed=False) 
            corrected_image = pT.correctPerspective(framed_image, cornerLocs, showCorrection=False, overrideTransform=True)
            # cv2.imwrite("test5.png", corrected_image)
            perception_corrected = True
            continue

        
        corrected_image = pT.correctPerspective(color_image)

        puckLoc = pT.locatePuck(corrected_image)
        if not puckLoc.get("center",None):
            continue

        print(puckLoc)
        locImage = pT.framePuck(corrected_image, puckLoc)

        # _, circles_img = pT.locateCircles(corrected_image)

        # Show image
        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        # cv2.imshow('RealSense', images)
        # cv2.imshow('RealSense', corrected_image)
        # cv2.imshow('RealSense', circles_img)
        cv2.imshow('RealSense', locImage)
        cv2.waitKey(1)

finally:

    # Stop streaming
    pipeline.stop()