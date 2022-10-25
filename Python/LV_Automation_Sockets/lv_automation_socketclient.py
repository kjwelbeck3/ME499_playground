import socket

def run_client(host, port):
    
    
    socket_client = socket.socket()
    socket_client.connect((host, port))


    # control_values = {
    #     "phase 1": 5,
    #     "amplitude 1": 10,
    #     "phase 2": 10,
    #     "amplitude 2": 5
    # }

    control_values = {
	"phase 1" : 5,
	"amplitude 1" : 10,
	"phase 2" : 5,
	"amplitude 2" : 10,
	"phase 3" : 5,
	"amplitude 3" : 10,
	"phase 4" : 5,
	"amplitude 4" : 10,
	"phase 5" : 5,
	"amplitude 5" : 10,
	"phase 6" : 5,
	"amplitude 6" : 10,
	"phase 7" : 5,
	"amplitude 7" : 10,
	"phase 8" : 5,
	"amplitude 8" : 10,
	"phase 9" : 5,
	"amplitude 9" : 10,
	"phase 10" : 5,
	"amplitude 10" : 10,

	"phase 11" : 5,
	"amplitude 11" : 20,
	"phase 12" : 5,
	"amplitude 12" : 20,
	"phase 13" : 5,
	"amplitude 13" : 20,
	"phase 14" : 5,
	"amplitude 14" : 20,
	"phase 15" : 5,
	"amplitude 15" : 20,
	"phase 16" : 5,
	"amplitude 16" : 20,
	"phase 17" : 5,
	"amplitude 17" : 20,
	"phase 18" : 5,
	"amplitude 18" : 20,
	"phase 19" : 5,
	"amplitude 19" : 20,
	"phase 20" : 5,
	"amplitude 20" : 20,

	"phase 21" : 5,
	"amplitude 21" : 30,
	"phase 22" : 5,
	"amplitude 22" : 30,
	"phase 23" : 5,
	"amplitude 23" : 30,
	"phase 24" : 5,
	"amplitude 24" : 30,
	"phase 25" : 5,
	"amplitude 25" : 30,
	"phase 26" : 5,
	"amplitude 26" : 30,
	"phase 27" : 5,
	"amplitude 27" : 30,
	"phase 28" : 5,
	"amplitude 28" : 30,
	"phase 29" : 5,
	"amplitude 29" : 30,
	"phase 30" : 5,
	"amplitude 30" : 30,
    }

    # pre-send: serialize then execute encode
    # post-recieve: decode then evaluate

    socket_client.send(str(control_values).encode())
    data = socket_client.recv(2048).decode()

    print(data)


if __name__ =="__main__":
    host = socket.gethostname()
    # host = "10.42.0.101"
    port = 5000

    run_client(host, port)