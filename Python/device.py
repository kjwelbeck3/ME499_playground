from cmath import phase
from labview_automation import LabVIEW
import numpy as np
import random

class DeviceManager:

    # def __init__(self, vi_path=r"C:\Users\Ping Guo\Documents\onedrive_backup\OneDrive - Northwestern University\Desktop\KojoWelbeck\ProjectEnvironment\Python\playground\30ControlsToIndicators.vi"):
    def __init__(self, vi_path=r"C:\Users\Ping Guo\Documents\onedrive_backup\OneDrive - Northwestern University\Desktop\KojoWelbeck\ProjectEnvironment\NI VIs\Test1.vi"):
        
        self.labview = LabVIEW()
        self.labview.start()
        # self.labviewClient = self.labview.client()
        self.vi_path = vi_path
        
        self.mapping = self.genMapping()
        # self.indicator_names = [
        # "p 1", "a 1", "p 2", "a 2", "p 3", "a 3", "p 4", "a 4", "p 5", "a 5", 
        # "p 6", "a 6", "p 7", "a 7", "p 8", "a 8", "p 9", "a 9", "p 10", "a 10" 
        # "p 11", "a 11", "p 12", "a 12", "p 13", "a 13", "p 14", "a 14", "p 15", "a 15", 
        # "p 16", "a 16", "p 17", "a 17", "p 18", "a 18", "p 19", "a 19", "p 20", "a 20" 
        # "p 21", "a 21", "p 22", "a 22", "p 23", "a 23", "p 24", "a 24", "p 25", "a 25", 
        # "p 26", "a 26", "p 27", "a 27", "p 28", "a 28", "p 29", "a 29", "p 30", "a 30" 
        # ]

    def genMapping(self):

        mapping = np.zeros((10,12), dtype=np.int8)
        submap = np.zeros((int(10/2), int(12/2)))

        submap[:, 0] = np.arange(5, 0, -1)
        submap[:, 1] = np.arange(10, 5, -1)
        submap[:, 2] = np.arange(15, 10, -1)
        submap[:, 3] = np.arange(20, 15, -1)
        submap[:, 4] = np.arange(25, 20, -1)
        submap[:, 5] = np.arange(30, 25, -1)

        mapping[0:5, 0:6] = submap
        mapping[0:5, 6:12] = submap
        mapping[5:10, 0:6] = submap
        mapping[5:10, 6:12] = submap

        return mapping

    def genResetControl(self, dictionary_prefix=""):
        _dict = {}
        for i in range (1,33):
            _dict[dictionary_prefix+str(i)] = 0
        return _dict

    def genControlDict(self, mask, control, dictionary_prefix=""):
        ## Should verify mask and control size matches 

        ## Populate mask footprint with matched control vals
        mask_controls = np.zeros((10,12), dtype=int)
        mask_controls[mask.nonzero()] = control.flatten()
        
        ## Mask the mapping
        mask_map = np.copy(self.mapping)
        mask_map[mask==0] = 0

        ## Get gontrol idxs from mask_map and control vals from mask_controls
        ## Combine into a control dict
        control_idxs = mask_map[mask>0]
        control_vals = mask_controls[mask>0]
        control_dict = self.genResetControl(dictionary_prefix)
        for i,v in enumerate(control_idxs):
            control_dict[dictionary_prefix + str(v)] = float(control_vals[i])
            # print(i, v, control_vals[i])
        
        return control_dict

    def forwardControlDict(self, control_dict):
        resp = None
        with self.labview.client() as c:
            resp = c.run_vi_synchronous(self.vi_path, control_dict)

        return resp
        ## might have to create a new client each time

    def start(self):
        # self.labviewClient
        pass

    def stop(self):
        pass

    def shutdown(self):
        ## might have to stop/decommish the self.labviewClient
        self.labview.stop()

def maskFromCentroid(shape=(10,12), centroid=(4,5), mask_width=5):
    from math import floor, ceil
    x, y = centroid
    n_rows, n_cols = shape
    
    x_min = max(0, x - floor(mask_width/2))
    x_max = min(n_cols, x + ceil(mask_width/2))
    
    y_min = max(0, y - floor(mask_width/2))
    y_max = min(n_rows, y + ceil(mask_width/2))
    
    mask = np.zeros((shape))
    mask[y_min:y_max, x_min:x_max] = 1
    
    return mask

if __name__ == "__main__":
    
    device = DeviceManager()
    
    test_mask = maskFromCentroid()
    # test_phase_mat = np.ones((5,5), dtype=float)*random.randint(0,200)
    test_phase_mat = np.random.randint(0, 359, (5,5))
    test_amplitude_mat = np.ones((5,5), dtype=float)*5

    phase_control_dict = device.genControlDict(test_mask, test_phase_mat, "phase ")
    print(phase_control_dict)
    resp = device.forwardControlDict(phase_control_dict)
    print(resp)

    amplitude_control_dict = device.genControlDict(test_mask, test_amplitude_mat, "amplitude ")
    amplitude_control_dict.update(phase_control_dict)
    print(amplitude_control_dict)
    resp = device.forwardControlDict(amplitude_control_dict)
    print(resp)

    # while True:
    #     try:
    #         time.sleep(1)
    #     except KeyboardInterrupt:
    #         exit()