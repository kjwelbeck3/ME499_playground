from bson import encode
from labview_automation import LabVIEW
import socket

def run_server(vi_path, indicator_names):
    
    host = socket.gethostname()
    port = 5000

    socket_server = socket.socket()
    socket_server.bind((host, port))

    socket_server.listen(1)
    conn, address = socket_server.accept()
    print("Connection from:  {}".format(address))

    data = eval(conn.recv(1024).decode())
    print(data)

    lv = LabVIEW()
    lv.start()

    with lv.client() as c:
        indicators = c.run_vi_synchronous(vi_path, data, indicator_names=indicator_names)

    conn.send(str(indicators).encode())
    



if __name__ == "__main__":
    vi_path = r"C:\Users\Ping Guo\Documents\onedrive_backup\OneDrive - Northwestern University\Desktop\KojoWelbeck\ProjectEnvironment\Python\playground\30ControlsToIndicators.vi"
    indicator_names = [
        "p 1", "a 1", "p 2", "a 2", "p 3", "a 3", "p 4", "a 4", "p 5", "a 5", 
        "p 6", "a 6", "p 7", "a 7", "p 8", "a 8", "p 9", "a 9", "p 10", "a 10" 
        "p 11", "a 11", "p 12", "a 12", "p 13", "a 13", "p 14", "a 14", "p 15", "a 15", 
        "p 16", "a 16", "p 17", "a 17", "p 18", "a 18", "p 19", "a 19", "p 20", "a 20" 
        "p 21", "a 21", "p 22", "a 22", "p 23", "a 23", "p 24", "a 24", "p 25", "a 25", 
        "p 26", "a 26", "p 27", "a 27", "p 28", "a 28", "p 29", "a 29", "p 30", "a 30" 
        ]
    run_server(vi_path, indicator_names)
