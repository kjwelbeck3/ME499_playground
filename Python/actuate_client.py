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
        print(f"Client Socket created : {self.socket_client}")

        ## wait for socket
        print(f"Waiting/Looking for Server Socket at {host_ip}:{host_port} ...")
        connected = False
        while not connected:
            try:
                self.socket_client.connect((self.HOST, self.PORT))
                # self.socket_client.close()
                connected = True
            except Exception as e:
                pass
        print()

    def send(self, mode:str, content=None):

        self.socket_client.send(str(mode).encode())
        ack = self.socket_client.recv(2048).decode()
        print("Received ack: {}".format(ack))
        if ack != mode:
            content = "[Error]: ACK does not match MODE. Not forwarding content"
            print(content)

        # if content:
        expected_ack = contentAck(content)

        self.socket_client.send(str(content).encode())
        ack = self.socket_client.recv(2048).decode()
        # print("ack")
        # print(ack)
        # print(type(ack))

        # print("expected_ack")
        # print(expected_ack)
        # print(type(expected_ack))
        # if ack != expected_ack:
        #     resp = f"[Error]: ACK does not match EXPECTED_ACK. Recvd: {ack}" 
        #     print(resp)
        #     return False, resp, expected_ack
            
        return True, "Done", expected_ack
            

    def send_control(self,mask_mat, phase_mat, amplitude_mat):
        mask_str = " ".join([str(i) for i in mask_mat.flatten().tolist()])
        ampl_str = " ".join([str(i) for i in amplitude_mat.flatten().tolist()])
        phase_str = " ".join([str(i) for i in phase_mat.flatten().tolist()])
        
        print("mask_str")
        print(mask_str)
        print(type(mask_str))

        print("phase_str")
        print(phase_str)
        print(type(phase_str))

        print("ampl_str")
        print(ampl_str)
        print(type(ampl_str))


        isSuccess, resp, _ = self.send("0", mask_str)
        if not isSuccess:
            return False, resp

        isSuccess, resp, _ = self.send("1", phase_str)
        if not isSuccess:
            return False, resp

        isSuccess, resp, _ = self.send("2", ampl_str)
        if not isSuccess:
            return False, resp 
        
        return True, "Done"


    def send_start(self):
        isSuccess, resp, _ = self.send("Y", "START")
        return isSuccess, resp

    def send_stop(self):
        isSuccess, resp, _ = self.send("N", "STOP")
        return isSuccess, resp

def contentAck(content):
    content = str(content)

    try:
        ack = str(sum([int(i) for i in content.split()]))
    
    except ValueError:

        ack = content[:2] + content[-2:]

    return ack


if __name__ == "__main__":

    amplitude_mat = np.ones((5,5), dtype=int)
    phase_mat = 15*np.ones((5,5), dtype=int)
    mask_mat = np.zeros((10,12), dtype=int)
    mask_mat[2:7,2:7] = 1

    ## Configure client socket
    # host = socket.gethostname()
    host = "10.42.0.100"
    client = ArrayControllerClient(host)

    ## Test sending messages
    # isSuccess, resp, expected_ack = client.send("1", "1 2 3 4 5 6 6 7 8 8 9 9 7 6 5 9 9 7 6 5 9 9 7 6 5")
    # print("isSuccess: " + str(isSuccess))
    # print("resp: " + resp)
    # time.sleep(3)
    # print()
    
    # isSuccess, resp, expected_ack = client.send("2", "1 2 3 4 5 6 6 7 8 8 9 9 7 6 5 1 2 3 4 5 6 6 7 8 8")
    # print("isSuccess: " + str(isSuccess))
    # print("resp: " + resp)
    # time.sleep(3)
    # print()

    # isSuccess, resp, expected_ack = client.send("3", "1 2 3 4 5 6 6 7 8 8 9 9 7 6 5")
    # print("isSuccess: " + str(isSuccess))
    # print("resp: " + resp)
    # time.sleep(3)
    # print()

    # isSuccess, resp, expected_ack = client.send("00", "2 6 2 6")
    # print("isSuccess: " + str(isSuccess))
    # print("resp: " + resp)
    # time.sleep(3)
    # print()

    # mask_str = " ".join([str(i) for i in mask_mat.flatten().tolist()])
    # print(mask_str)
    # isSuccess, resp, expected_ack = client.send("0", mask_str)
    # print("isSuccess: " + str(isSuccess))
    # print("resp: " + resp)
    # time.sleep(3)
    # print()


    # isSuccess, resp, expected_ack = client.send("1", "1 2 3 4 5 6 6 7 8 8 9 9 7 6 5 9 9 7 6 5 9 9 7 6 5")
    # print("isSuccess: " + str(isSuccess))
    # print("resp: " + resp)
    # time.sleep(3)
    # print()
    
    # isSuccess, resp, expected_ack = client.send("2", "1 2 3 4 5 6 6 7 8 8 9 9 7 6 5 1 2 3 4 5 6 6 7 8 8")
    # print("isSuccess: " + str(isSuccess))
    # print("resp: " + resp)
    # time.sleep(3)
    # print()

    isSuccess, resp = client.send_control(mask_mat, phase_mat, amplitude_mat)
    print("isSuccess: " + str(isSuccess))
    print("resp: " + resp)
    print()

    # isSuccess, resp, expected_ack = client.send("Z", "SHUTDOWN")
    # print("isSuccess: " + str(isSuccess))
    # print("resp: " + resp)
    # print("expected_ack: " + expected_ack)
    # print()


    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Closing...")
        exit()


### CURRENT ISSUE WITH SENDING 0