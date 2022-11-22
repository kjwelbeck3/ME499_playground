## ArrayControllerClient
## -- send 5X5 arrays with mask by socket
## -- -- wait for acknowledgement
## -- stop by socket

import socket
import numpy as np
import time


class ArrayControllerClient:
    def __init__(self, host_ip, host_port=5005, buffersize=2048):

        self.HOST = host_ip
        self.PORT = host_port
        self.BUFFER_SIZE = buffersize

        self.socket_client = socket.socket()
        print(self.socket_client)
        self.socket_client.connect((self.HOST, self.PORT))


    def send(self, mode, content=None):

        self.socket_client.send(str(mode).encode())
        ack = self.socket_client.recv(2048).decode()
        print("ACK: {}".format(ack))
        if ack != mode:
            content = "[Error]: ACK does not match MODE. Not forwarding content"
            print(content)

        # if content:
        expected_ack = contentCheck(content)
        self.socket_client.send(str(content).encode())
        ack = self.socket_client.recv(2048).decode()
        if ack != expected_ack:
            resp ="[Error]: ACK does not match EXPECTED_ACK." 
            print(resp)
            return False, resp
            
        return True, "Done"
            

    def send_control(self,mask_mat, phase_mat, amplitude_mat):
        pass


    def stop(self):
        pass

def contentCheck(content):
    content = str(content)
    return content[:2] + content[-2:]


if __name__ == "__main__":

    amplitude_mat = 0
    phase_mat = 0
    mask_mat = 0

    ## Configure client socket
    host = socket.gethostname()
    client = ArrayControllerClient(host)

    ## Test sending messages
    isSuccess, resp = client.send("1", "1 2 3 4 5 6 6 7 8 8 9 9 7 6 5")
    print("isSuccess: " + str(isSuccess))
    print("resp: " + resp)
    time.sleep(3)
    
    isSuccess, resp = client.send("2", "1 2 3 4 5 6 6 7 8 8 9 9 7 6 5")
    print("isSuccess: " + str(isSuccess))
    print("resp: " + resp)
    time.sleep(3)

    isSuccess, resp = client.send("3", "1 2 3 4 5 6 6 7 8 8 9 9 7 6 5")
    print("isSuccess: " + str(isSuccess))
    print("resp: " + resp)
    time.sleep(3)

    isSuccess, resp = client.send("0", "noneonoe")
    print("isSuccess: " + str(isSuccess))
    print("resp: " + resp)
    time.sleep(3)

    isSuccess, resp = client.send("Z", "Recvd SHUTDOWN")
    print("isSuccess: " + str(isSuccess))
    print("resp: " + resp)



### CURRENT ISSUE WITH SENDING 0