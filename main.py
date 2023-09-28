# This kinda gives "false" positives
    # If the script pings a host and the output of ping is (windows) "TTL expired in transit", it will deem the host as up.
    # Majority of the hosts that will be in the "UP" file will be active but not ALL.
    # If you just grab and use the hosts without doing one extra check that maybe the reason why your connection is slow.

import os
import time
import sys
import subprocess
import string
import random
import platform
from threading import Thread
from colorama import Fore, Back, Style, init

Dim = Style.DIM
Red = Fore.RED
Gre = Fore.GREEN
Yel = Fore.YELLOW

sys = platform.system()

Banner = Dim + '''

.--.                .--.                .--.
|__| .-------.      |__| .-------.      |__| .-------.
|=.| |.-----.|      |=.| |.-----.|      |=.| |.-----.|
|--| || 001 || ---> |--| || 002 || ---> |--| || 003 ||
|  | |'-----'|      |  | |'-----'|      |  | |'-----'|
|__|~')_____('      |__|~')_____('      |__|~')_____('

                   Author - Almight

'''

init(autoreset=True)

class Sweeper():

    Up: list[tuple] = []

    def __init__(self, fileName, log) -> None:

        self.fileName = fileName
        self.log = log
    
    def Ping(self, ip: str, port: int):
            
            chars = string.ascii_letters + string.digits
            new_file = "UP-" + ("".join(random.choice(chars) for _ in range(8)) + ".txt")
            
            match sys:

                case "Windows":
                    res = subprocess.Popen(["ping","-n", "2", ip], stdout=subprocess.PIPE).communicate()[0]
                    if b"Lost = 0" in res:
                        self.Up.append((ip, port))
                        if self.log == True:
                            with open(f"misc/{new_file}", "a+") as log:
                                log.write(ip + ":" + str(port) + "\n")
                case "Linux":
                    res = subprocess.Popen(["ping","-c", "2", ip], stdout=subprocess.PIPE).communicate()[0]
                    if b"0% packet loss" in res:
                        self.Up.append((ip, port))
                        if self.log == True:
                            with open(f"misc/{new_file}", "a+") as log:
                                log.write(ip + ":" + str(port) + "\n")

    def Sweep(self):

        with open(self.fileName) as file:
            for i in file:

                serv = i.split(":", 1)
                ip = serv[0]
                port = int(serv[1])

                print(Dim + Yel + f"[!] Pinging -> {ip}:{port}", flush=True)
                t = Thread(target=Sweeper.Ping, args=(self, ip, port))
                t.start()
                time.sleep(2)

def main(debug):

    if debug == True:
        file = "misc/local.txt"
    else:
        match sys:

            case "Windows":
                os.system("cls")
            case "Linux":
                os.system("clear")

        file = input(Dim + "IP File > ")

    s = Sweeper(file, log=True)

    print(Banner)
    s.Sweep()
    
    for i in s.Up:

        new_ip = i[0]
        new_port = i[1]
        print(Dim + Gre + f"[UP] {new_ip}:{new_port}")
                   
if __name__ == "__main__":
    
    try:
        main(debug=False)
    except KeyboardInterrupt:
        print(Dim + Red + "Exiting. . .\n")
        exit(0)
