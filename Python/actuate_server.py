## ArrayControllerServer
## -- recieve command 5x5 arrays and mask by socket
## -- -- acknowledge receipt
## -- command labview instrument
## -- -- mapping mask, phase and amplitude arrays to labview control
## -- recieve stop command

import numpy as np
import socket
from actuate_client import contentCheck

class ArrayControllerServer:
    
    def __init__(self, VI, mappingConfig=None):

        self.amplitude_mat = None
        self.phase_mat = None
        self.mask_mat = None
        self.mappingConfig = None

        self.HOST = socket.gethostname()
        self.PORT = 5005
        self.BUFFER_SIZE = 2048


        self.server_socket = socket.socket()
        self.server_socket.bind((self.HOST, self.PORT))
        print("Server Socket established: {}".format(self.server_socket.getsockname))

        self.server_socket.listen(1)
        self.connection, self.client_address = self.server_socket.accept()
        print("Connection from:  {}".format(self.client_address))


    def recv(self):

        content = None
        
        mode = self.connection.recv(self.BUFFER_SIZE).decode()
        print("Recvd mode : {}".format(mode))
        self.connection.send(mode.encode())

        print("Waiting on content ...")
        content = self.connection.recv(self.BUFFER_SIZE).decode()

        print("Recvd content : {}".format(content))
        ack = self.process_content(mode, content)
        self.connection.send(ack.encode())

        return mode, content, ack

    def command_VI(self):
        pass


    def process_content(self,mode, content):

        # check for error then unpack based on mode
        # generate and return checksum

        return contentCheck(content)

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
        while run:
            # Test incomming socket messages
        
            mode, content, ack = server.recv()
            print("mode: " + mode)
            print("content: " + content)
            print("ack: " + ack)

            if str(mode) == "Z":
                print("Shutting down ...")
                run = False
                server.shutdown()
                

    except KeyboardInterrupt:
        print("Shutting down ...")
        server.shutdown()

    # except:
    #     print("Non-KeyboardInterrupt exception")
        
    
    finally:
        exit(0)


        
