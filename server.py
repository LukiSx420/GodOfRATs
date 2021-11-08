import time, os, json
from tools import NewServer

class Server:
    def __init__(self, ip, port):
        if os.path.exists("connDB.json"):
            self.connDB = self.loadDatabase()
        else:
            print("[!] No connetion database was found, creating one now...")
            self.connDB = {"history": []}
            self.saveDatabase()
        self.s = NewServer(ip, port, database=self.connDB, discordNotifications=True)
        print("[.] Server initalized")

    def loadDatabase(self):
        f = open("connDB.json", 'r')
        db = json.loads(f.read())
        f.close()
        return db
    
    def saveDatabase(self):
        f = open("connDB.json", 'w')
        f.write(json.dumps(self.connDB, sort_keys=True, indent=2))
        f.close()

    def run(self):
        self.s.listen()
        print("[.] Listening at", self.s.server[0], "at port", self.s.server[1], "for connections...")
        print("[.] Press CTRL + C to exit the server...")
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("[.] Exiting...")
        self.s.shutdown()
        self.connDB = self.s.exportDatabase()
        self.saveDatabase()
        del self.s
        exit("Done")

if __name__ == "__main__":
    s = Server("localhost", 4444)
    s.run()