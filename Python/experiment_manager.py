import numpy as np
from data_collection import DataCollector
from statemachine import StateMachine, State

class ExperimentManager:



    def __init__(self, PhaseMatrixList, AmplitudeMatrixList, filename, run_duration=2):
        
        if len(PhaseMatrixList) != len(AmplitudeMatrixList):
            raise Exception("The lengths of the respective Control Matrix lists do not match. {len(PhaseMatrixList)} != {len(AmplitudesMatrixList)}")
        
        if len(PhaseMatrixList) == 0 or type(PhaseMatrixList) != list:
            raise Exception("arg PhaseMatrixList must be a non-empty list of 5x5 matrices")

        if len(AmplitudeMatrixList) == 0 or type(AmplitudeMatrixList) != list:
            raise Exception("arg AmplitudeMatrixList must be a non-empty list of 5x5 matrices")

        
        self.filename = filename
        self.PhaseList = PhaseMatrixList
        self.AmplitudeList = AmplitudeMatrixList
        self.run_duration = run_duration #secs

        self.i = 0
        self.currentPhaseMat = None
        self.currentAmplitudeMat = None

        self.dC = DataCollector(actuator_host="10.42.0.100",filename=filename)
        print("Setting up stream")
        self.dC.setupStream()
        
        # self.in_progress = True


    def start(self):
        self.state = "paused"
        in_progress = True
        while in_progress:
            if self.state == "paused":
                self.on_paused()
            if self.state == "running":
                self.on_run()

    
    def on_paused(self):
        command = input("[Paused] Press ENTER to continue. ('exit' to close)")
        if command.lower() == "exit":
            print("Closing preemptively...")
            exit(0)
        if self.i >= len(self.PhaseList):
            print("Finished Running through Control Matrix List")
            print("Experiment Complete")
            print(f"Experiment data saved to {self.filename}")
            print("exiting ...")
            self.in_progress = False
            exit(0)
        self.run()

    def on_run(self):
        print(f"[Run] #: {self.i}")
        self.currentPhaseMat = self.PhaseList[self.i]
        self.currentAmplitudeMat = self.AmplitudeList[self.i]
        self.dC.runOnce(self.currentPhaseMat, self.currentAmplitudeMat, secs=self.run_duration, showSubGrid=True)
        self.i +=1
        self.pause()

    def run(self):
        self.state = "running"

    def pause(self):
        self.state = "paused"
        
if __name__ == "__main__":
    eM = ExperimentManager([np.zeros((5,5), dtype=int)]*10, [3*np.ones((5,5), dtype=int)]*10, "testing.csv")
    eM.start()

        
