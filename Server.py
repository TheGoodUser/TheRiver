import socket
import threading as th
from colorama import *
import time

init() 
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(("127.0.0.1", 9898))
server.listen(5)

clients = []
hostname = []
clients_closed_at = dict()
clients_connected_at = dict()

# it adds two times with format %H:%M:%S onlyt
# t1 : to be subtracted
# t2 : from which subtracted
def sub_times(t1, t2):
    t1 = t1.split(":")
    t2 = t2.split(":")
    h1, m1, s1 = int(t1[0]), int(t1[1]), int(t1[2])
    h2, m2, s2 = int(t2[0]), int(t2[1]), int(t2[2])

    h3, m3, s3 = str((h2-h1)+(m2-m1+(s2-s1)//60)//60), str((m2-m1+(s2-s1)//60)%60), str((s2-s1)%60)
    if len(h3) != 2:
        h3 = "0"+h3
    if len(m3) != 2:
        m3 = "0"+m3
    if len(s3) != 2:
        s3 = "0"+s3
        
    return f"{h3}:{m3}:{s3}"


def msg_forward(FROM, msg):
    if len(msg.split()) != 0:
        if "ac @" in msg:
            for f in clients:
                if f != FROM:
                    f.send(msg.encode())
        elif "CLoSuR3 has occured" in msg:
            for f in clients:
                if f != FROM:
                    f.send(f"{hostname[clients.index(FROM)]} CLoSuR3 has occured".encode())
        else:
            for f in clients:
                if f != FROM:
                    f.send((hostname[clients.index(FROM)]+" "+msg).encode())

def client_handler(con):
    while True:
        # Chat History
        chat_history = open("chat-history.txt", "a")
        
        try:
            msg = con.recv(1024).decode()
            if len(msg) != 0:
                # saving chat hostory
                record = (hostname[clients.index(con)], msg, time.ctime())
                chat_history.write(f"{str(record)}\n")
                chat_history.flush()

                # msg forwarded to everyone
                msg_forward(con, msg)
            else:
                pass
        except:
            # chat_history saved!!
            chat_history.close()

            # forwarding: client "con" got oFFLINE
            #print(hostname[clients.index(con)], "lost connection")
            msg_forward(con, "CLoSuR3 has occured")

            # client(s) details who were OFFLINE
            clients_closed_at.update({hostname[clients.index(con)]: time.ctime()[11:-5]})

            # changing other indexes
            i = clients.index(con)
            clients.remove(con)
            con.close()

            host = hostname[i]
            hostname.remove(host)
            break     

def client_recv():
    while True:
        c, a = server.accept()

        # getting client details
        c.send("nick".encode())
        host = c.recv(1024).decode()

        # client connectection timing format hostname:time
        clients_connected_at.update({host:time.ctime()[11:-5]})
        
        # saving client details 
        hostname.append(host)
        clients.append(c)
        
        print(host, "got connection")
        msg_forward(c, "ac "+"@"+host)
        
        thread = th.Thread(target=client_handler, args=(c,))
        thread.start()

        # forwarding chat messages to client(s) while they were OFFLINE
        # if client(s) is already connected
        if hostname[clients.index(c)] in clients_closed_at:
            # getting info. of when the client(s) got OFFLINE
            msg_from = clients_closed_at[hostname[clients.index(c)]][11:-5]
            
            temp_msg = []

            # finally forwarding all messages upto 5 minutes or more of his disconnection
            with open("chat-history.txt", "r") as f:
                for j in f.readlines(): # here j retuns buch of lines i.e. no single lines
                    try:
                        j = rf"{j}"
                    except:
                        pass
                    
                    # getting single lines from bunch, which are separated by "\n"
                    for m in j.split("\n"):

                        try:
                            if m[0] == "(":
                                temp_msg.append(m)
                            if m[0] != "(":
                                temp_msg.append(m.replace(m[0], ""))
                        except:
                            print("unnecessary lines to be added to the list")
                        
            for f in temp_msg:
                    try:
                        # string to tuple
                        _ = eval(f)
                    except: 
                        pass

                    # timing of every chat of format %H:%M:%S
                    msgs_timing = _[2][11:-5]
                    
                    # messages in btw time: when client(s) connected and just 5 min before it
                    if clients_connected_at[host] >= msgs_timing >= sub_times("00:05:00", clients_connected_at[host]):
                        c.send((_[0]+" "+_[1]).encode())
            continue
        else:
            print('\t-new client recorded')


print("SERVER LIVE\n")     
client_recv()









