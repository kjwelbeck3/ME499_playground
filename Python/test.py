
## Testing Keyboard wait

# while True:
#     text = input("Enter to continue/exit to close\n")
#     if text.lower() == "exit":
#         exit(0)


## Testing April Tags pose
from ctypes.wintypes import tagSIZE
import pupil_apriltags
import numpy as np
import pyrealsense2 as rs
import cv2
import math


# Calculates rotation matrix to euler angles
# The result is the same as MATLAB except the order
# of the euler angles ( x and z are swapped ).
def rotationMatrixToEulerAngles(R) :
 
    # assert(isRotationMatrix(R))
 
    sy = math.sqrt(R[0,0] * R[0,0] +  R[1,0] * R[1,0])
 
    singular = sy < 1e-6
 
    if  not singular :
        x = math.atan2(R[2,1] , R[2,2])
        y = math.atan2(-R[2,0], sy)
        z = math.atan2(R[1,0], R[0,0])
    else :
        x = math.atan2(-R[1,2], R[1,1])
        y = math.atan2(-R[2,0], sy)
        z = 0
 
    return np.array([x, y, z])

detector = pupil_apriltags.Detector(families="tag36h11")


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
# pipeline.start(config)

cfg = pipeline.start(config)
profile = cfg.get_stream(rs.stream.color)
intr = profile.as_video_stream_profile().get_intrinsics()
# print(intr)
# print(intr.ppx)

camera_params=(intr.fx, intr.fy, intr.ppx, intr.ppy)
print(camera_params)
# print(ps.coeffs)


try:
    while True:

        # Wait for a coherent color frame
        frames = pipeline.wait_for_frames()
        color_frame = frames.get_color_frame()
        if not color_frame:
            continue

        # Convert image to numpy arrays
        color_image = np.asanyarray(color_frame.get_data())

        gray_img = cv2.cvtColor(color_image, cv2.COLOR_RGB2GRAY)
        # print(gray_img)
        gray_img = gray_img.astype(np.uint8)
        
        res = detector.detect(gray_img, estimate_tag_pose=True, camera_params=camera_params, tag_size=0.05558)

        if res:
            # print(res[0].pose_R)
            print(res[0])
            print(rotationMatrixToEulerAngles(res[0].pose_R)[2])

        cv2.namedWindow('RealSense', cv2.WINDOW_AUTOSIZE)
        cv2.imshow('RealSense', gray_img)
        cv2.waitKey(1)


finally:

    # Stop streaming
    pipeline.stop()


# ## Testing the zeroing out of matrice0s
# from __ex__levitate_control import zeroOutMiddleCell, zeroOutMiddleCells
# import numpy as np

# print("Testing zeroOutMiddleCells")
# print("5x5")
# print(zeroOutMiddleCells())
# print("5x6")
# print(zeroOutMiddleCells(mat=np.ones((5,6))))
# print("6x6")
# print(zeroOutMiddleCells(mat=np.ones((6,6))))
# print("2x2")
# print(zeroOutMiddleCells(mat=np.ones((2,2))))
# print()

# print("Testing zeroOutMiddleCell")
# print("5x5")
# print(zeroOutMiddleCell())
# print("5x6")
# print(zeroOutMiddleCell(mat=np.ones((5,6))))
# print("6x6")
# print(zeroOutMiddleCell(mat=np.ones((6,6))))
# print("2x2")
# print(zeroOutMiddleCell(mat=np.ones((2,2))))