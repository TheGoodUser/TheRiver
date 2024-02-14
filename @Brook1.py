import socket
import threading as th
from colorama import *

# socket.gethostname() = "Client-3"
nick = '<Brook1>'

init()
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# trying to connect to server
try:
    client.connect(("127.0.0.1", 9898))
    print(Fore.LIGHTBLUE_EX+nick+Fore.RESET+Fore.GREEN+" you are online now\n"+Fore.RESET)
except:
    print(Fore.RED+"SERVER OFFLINE"+Fore.RESET)
    exit()

# to get all the messages continously
def recv_msg():
    while True:
        try:
            msg = client.recv(1024).decode()
            if msg == 'nick':
                client.send(nick.encode())
            elif "CLoSuR3 has occured" in msg:
                msg = msg.replace("<", "")
                msg = msg.replace(">", "")
                msg = msg.split()[0]
                msg = "[OFFLINE]"+" @"+msg
                msg = msg.split()
                msg = Fore.LIGHTYELLOW_EX+msg[0]+Fore.RESET+Fore.RED+" "+msg[1]+Fore.RESET
                print(msg)
            elif "ac @" in msg:
                msg = msg[msg.find('ac ')+3:]
                msg = msg.replace("<", "")
                msg = msg.replace(">", "")
                msg = "[ONLINE]"+" "+msg
                msg = msg.split()
                msg = Fore.LIGHTYELLOW_EX+msg[0]+Fore.RESET+Fore.BLUE+" "+msg[1]+Fore.RESET
                print(msg)
            else:
                msg = msg.split(">")
                print(Fore.RED+msg[0][1:]+Fore.RESET+ msg[1])
        except:
            client.close()
            break


def server_send():
    while True:
        sn = input()
        # nothing input
        if len(sn) == 0:
            continue
        client.send(sn.encode())
        
recv_thread = th.Thread(target=recv_msg)
recv_thread.start()

server_send_thread = th.Thread(target=server_send)
server_send_thread.start()












