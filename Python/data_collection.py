import numpy as np
import csv
import actuate_client
# import realsense
import vision
import pyrealsense2 as rs
import threading
from datetime import datetime
import time


class DataCollector:
    def __init__(self, actuator_host="10.42.0.100", filename="samples.csv") -> None:
        self.filename = filename
        
        # ## Configure Actuator Client
        # self.actuator_client = actuate_client.ArrayControllerClient(actuator_host)

        # Configure puck and stage tracking
        self.pT = vision.puckTracker()
        self.perception_corrected = False

        # Configure color streams
        self.setupStream()
        self.isRecording = threading.Event()
        

    def setupStream(self):

        self.pipeline = rs.pipeline()
        config = rs.config()

        # Get device product line for setting a supporting resolution
        pipeline_wrapper = rs.pipeline_wrapper(self.pipeline)
        pipeline_profile = config.resolve(pipeline_wrapper)
        device = pipeline_profile.get_device()
        # device_product_line = str(device.get_info(rs.camera_info.product_line))
        

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
        self.pipeline.start(config)

        try:
            while not self.perception_corrected:
                
                # Wait for a coherent color frame
                frames = self.pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                if not color_frame:
                    continue

                # Convert image to numpy arrays
                color_image = np.asanyarray(color_frame.get_data())

                isSuccess, res = self.pT.locateStage(color_image,showTags=False)
                if not isSuccess:
                    # print(res)
                    continue

                framed_image, cornerLocs = self.pT.frameStage(color_image, res, showFramed=False) 
                corrected_image = self.pT.correctPerspective(color_image, cornerLocs, showCorrection=False, overrideTransform=True)
                # cv2.imwrite("test5.png", corrected_image)
                self.perception_corrected = True
                print("[DataCollection]: Stream Setup complete")
            
        finally:
            self.pipeline.stop()
            

    def _locatePuck(self):
        found = False
        self.pipeline.start()
        try:
            while not found:

                ## Get coherent color frame
                frames = self.pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
               
                if not color_frame:
                    continue

                # Convert image to numpy arrays
                color_image = np.asanyarray(color_frame.get_data())

                # Correct/Crop to ROI
                corrected_image = self.pT.correctPerspective(color_image)

                # Locate the puck's apriltag 
                puckLoc = self.pT.locatePuck(corrected_image)
                if not puckLoc.get("center",None):
                    continue

                found = True
        finally:
            self.pipeline.stop()

        return puckLoc["center"], corrected_image

    def recordPuck(self):
        
        self.timestamps = []
        self.pixel_locs = []
        timestamp = None
        self.pipeline.start()
        try:
            self.isRecording.set()
            while self.isRecording.is_set():

                ## Get coherent color frame and timestamp
                frames = self.pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                if not timestamp:
                    start_time = datetime.now()
                timestamp = datetime.now() - start_time  #referenced from time of the record call 
                if not color_frame:
                    continue

                # Convert image to numpy arrays
                color_image = np.asanyarray(color_frame.get_data())

                # Correct/Crop to ROI
                corrected_image = self.pT.correctPerspective(color_image)

                # Locate the puck's apriltag 
                puckLoc = self.pT.locatePuck(corrected_image)
                if not puckLoc.get("center",None):
                    continue
                
                # Save data sample
                self.timestamps.append(str(timestamp))
                self.pixel_locs.append(puckLoc.get("center"))
        finally:
            self.pipeline.stop()

        # return timestamps, pixel_locs

    
    def saveRecord(self, phase_matrix, ampl_matrix):
        """Concatenate components of run, and write to CSV"""

        phase_list_of_strings = [str(i) for i in phase_matrix.flatten().tolist()]
        amplitude_list_of_strings = [str(i) for i in ampl_matrix.flatten().tolist()]
        pixel_locs_list_of_strings = [str(i) for i in self.pixel_locs]
        concat = phase_list_of_strings + amplitude_list_of_strings + self.timestamps + pixel_locs_list_of_strings
        
        with open(self.filename, 'a') as file:
            
            writer = csv.writer(file)
            writer.writerow(concat)
            print(f"wrote to {self.filename}")
        

    def stopRecord(self):
        if self.isRecording.is_set():
            self.isRecording.clear()
            return True, "Done Recording"
        
        return False, "No Recording to Stop"



    def runOnce(self, phase_mat=np.zeros((5,5)), ampl_mat=np.ones((5,5))*1, showSubGrid=False):
        """Find puck loc, Start recording, actuate for spec'd time, stop recording, save recording"""
        
        centroid, img = self._locatePuck()#[0]["center"]
        mask, cell, subgrid_cells, subgrid_px = self.pT.getMaskMatFromCentroid(img, centroid, showSubGrid)
        print("centroid")
        print(centroid)
        print("mask")
        print(mask)
        print("cell")
        print(cell)
        # print("subgrid_cells")
        # print(subgrid_cells)
        # print("subgrid_px")
        # print(subgrid_px)

        thread = threading.Thread(target=self.recordPuck)
        thread.start()

        # ## Actuate array and wait for spec'd seconds
        # isSuccess, resp = self.actuator_client.send_control(mask, phase_mat, ampl_mat)
        # print(isSuccess)
        # print(resp)

        # isSuccess, resp = self.actuator_client.send_start()
        # print(isSuccess)
        # print(resp)

        time.sleep(2)
        # isSuccess, resp = self.actuator_client.send_control(mask, np.zeros((5,5)), np.zeros((5,5)))

        # isSuccess, resp = self.actuator_client.send_stop()
        # print(isSuccess)
        # print(resp)

        __, msg = self.stopRecord()
        print(msg)
        thread.join()
        print("Run Complete")
        self.saveRecord(phase_mat, ampl_mat)


if __name__ == "__main__":
    dc = DataCollector("10.42.0.100")
    print("setting up stream")
    dc.setupStream()
    print("running once")
    dc.runOnce(showSubGrid=True)
