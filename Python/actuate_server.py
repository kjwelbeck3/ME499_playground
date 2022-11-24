## ArrayControllerServer
## -- recieve command 5x5 arrays and mask by socket
## -- -- acknowledge receipt
## -- command labview instrument
## -- -- mapping mask, phase and amplitude arrays to labview control
## -- recieve stop command

import numpy as np
import socket
from actuate_client import contentAck
import device

class ArrayControllerServer:
    
    def __init__(self, VI, mappingConfig=None):

        self.ampl_mat = None
        self.phase_mat = None
        self.mask_mat = None
        self.phase_control_dict
        self.ampl_control_dict

        self.device = device.DeviceManager()

        self.HOST = socket.gethostname()
        self.PORT = 5005
        self.BUFFER_SIZE = 2048

        self.server_socket = socket.socket()
        self.server_socket.bind((self.HOST, self.PORT))
        print("Server Socket established: {}".format(self.server_socket.getsockname()))

        self.server_socket.listen(1)
        self.connection, self.client_address = self.server_socket.accept()
        print("Connection from:  {}".format(self.client_address))


    def recv(self):
        
        mode = self.connection.recv(self.BUFFER_SIZE).decode()
        print("Recvd mode : {}".format(mode))
        self.connection.send(mode.encode())

        print("Waiting on content ...")
        content = self.connection.recv(self.BUFFER_SIZE).decode()

        print("Recvd content : {}".format(content))
        success, ack = self.process_content(mode, content)
        self.connection.send(ack.encode())

        return mode, content, ack

    def process_content(self,mode, content):

        # check for error then unpack based on mode
        # generate and return checksum

        if not content:
            return False, "Expected truthy content."

        if mode == "00":
            try:
                y_start, y_end, x_start, x_end = [int(i) for i in content.split()]
                self.mask_mat = np.zeros((10, 12))
                self.mask_mat[y_start:y_end, x_start:x_end] = 1
            except ValueError:
                return False, f"Expected string of exactly 4 whitespace-separated numbers"

        if mode == "0":
            try:
                mask_list = [int(i) for i in content.split()]
                self.mask_mat = np.array(mask_list, dtype=np.int16).reshape((10,12))
                self.phase_control_dict = self.device.genControlDict(self.mask_mat, self.phase_mat, "p ")
                self.ampl_control_dict = self.device.genControlDict(self.mask_mat, self.ampl_mat, "a ")
            except ValueError:
                return False, f"Expected string of exactly 120 whitespace-separated numbers"

        if mode == "1":
            try:
                phase_list = [int(i) for i in content.split()]
                self.phase_mat = np.array(phase_list, dtype=np.int16).reshape((5,5))
                self.phase_control_dict = self.device.genControlDict(self.mask_mat, self.phase_mat, "p ")
            except ValueError:
                return False, f"Expected string of exactly 25 whitespace-separated numbers"

            
        if mode == "2":
            try:
                ampl_list = [int(i) for i in content.split()]
                self.ampl_mat = np.array(ampl_list, dtype=np.int16).reshape((5,5))
                self.ampl_control_dict = self.device.genControlDict(self.mask_mat, self.ampl_mat, "a ")
            except ValueError:
                return False, f"Expected string of exactly 25 whitespace-separated numbers"
                

        return True, contentAck(content)


    # def updateControls(self):
    #     """ Generate control dictionary """

    #     self.phase_control_dict = self.device.genControlDict(self.mask_mat, self.phase_mat, "p ")
    #     self.phase_control_dict = self.device.genControlDict(self.mask_mat, self.ampl_mat, "a ")
    #     pass

    def command_VI(self, command=None):
        # if command == "start":
        #     pass ## send the start command

        if command == "stop":
            pass ## send the stop command

        if command == "phase":
            resp = self.device.forwardControlDict(self.phase_control_dict)


        if command == "amplitude":
            resp = self.device.forwardControlDict(self.ampl_control_dict)

        if command == "all":
            ampls_and_phases = {} 
            ampls_and_phases.update(self.ampl_control_dict) 
            ampls_and_phases.update(self.phase_control_dict)

            resp = self.device.forwardControlDict(ampls_and_phases)

        return resp


    def shutdown(self):
        self.server_socket.close()
        self.server_socket.shutdown()


if __name__ == "__main__":
    run = True
    amplitude_mat = 0
    phase_mat = 0
    mask_mat = 0

    # Configure server socket
    server = ArrayControllerServer(0)

    try:
        while run:  ## TODO Reimplement as event based with an event loop --> aysncio

            # Test incomming socket messages
            mode, content, ack = server.recv()
            print("sending ack: " + ack)
            print()

            if str(mode) == "Z":
                print("Shutting down ...")
                run = False
                server.shutdown()    
            
            if str(mode) == "Y":
                server.command_VI("start")

            if str(mode) == "N":
                server.command_VI("stop")


    except KeyboardInterrupt:
        print("Shutting down ...")
        server.shutdown()
    
    finally:
        exit(0)


        
