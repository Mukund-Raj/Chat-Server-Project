"""Server script"""
import socket
import json
from threading import Thread
import mysql.connector
con=mysql.connector.connect(host="localhost",user="root",password="",database="users")

def accept_incoming_connections():
    """Sets up handling for incoming clients."""
    while True:
        client, client_address = SERVER.accept()
        print("%s:%s has connected." % client_address)
        #client.send(bytes("Welcome to the chat! Now type your name and press enter!", "utf8"))
        addresses[client] = client_address
        Thread(target=handle_single_client, args=(client,client_address)).start()


def handle_single_client(client,client_address):  # Takes client socket as argument.
    """Handles a single client connection."""
    welcome=""
    name=""
    while True:
        name_msg = client.recv(BUFSIZE)
        n=json.loads(name_msg.decode("utf8"))
        for i in n.keys():
            key=i
        name=key
        password=n[key]
        print("name,password",name,password)
    
        if name=="newuser":
            name=createnewaccount(client)
            welcome= 'Welcome %s! If you ever want to quit, type "good bye" to exit.' % name
            break
        else: 
            f=checkdetails(name,password)
            if f=="found101":
                welcome = 'Welcome back %s! If you ever want to quit, type "good bye" to exit.' % name
                client.send(bytes("found101","utf-8"))
                break
            else:
                client.send(bytes("notfound404","utf-8"))
                continue

    client.send(bytes(welcome,"utf-8"))
    msg = "[%s has joined the chat!]" % name
    broadcast(msg)
    connections=''
    
    if len(name_client)==0:
        connections="no connections are available"
    else:
        for Name in name_client.keys():
            connections=connections+Name
            connections=connections+","
        connections=connections[:-1]
        connections+=" are available"
        
    clients[client] = name
    name_client[name]=client
    
    client.send(bytes("\n"+connections,"utf-8"))
    print(welcome)
    
    while True:
        try:
            msg = client.recv(BUFSIZE)
            recv_client=""
            try:
                d=json.loads(msg.decode("utf-8"))
            except:
                client.send(bytes("can't able to send message","utf-8"))
            for key in d.keys():
                recv_name=key

            print(recv_name)
            message_client=d[recv_name]

            print(message_client)

            if recv_name!="all":
                for Name in name_client.keys():
                    if recv_name==Name:
                        recv_client=name_client[Name]
                        break

            if recv_client=="" and recv_name!="all":
                m={}
                m[name]="message not sent,wrong name"
                client.send(json.dumps(m).encode("utf-8"))
            else:
                if recv_name=="all":
                    if message_client !="good bye":
                        broadcast(message_client, name+": ")
                    elif message_client=='good bye':
                        #client.send(bytes("good bye", "utf8"))
                        
                        print("good bye working")
                        del clients[client]
                        del name_client[name]
                        client.close()
                        broadcast("[%s has left the chat.]" % name)
                        break
                else:
                    singleClient(recv_client,client,name,recv_name,message_client)
        except OSError:
            continue

    print(name_client)

def broadcast(msg, prefix=""):  # prefix is for name identification.
    """Broadcasts a message to all the clients."""
    for sock in clients:
        try:
            sock.send(bytes(prefix+msg,"utf8"))
        except OSError:
            continue

def singleClient(receiver,sender,name,recv_name,message_client):
    msg=name+"::"+recv_name+": "+message_client
    receiver.send(bytes(msg,"utf-8"))
    sender.send(bytes(msg,"utf-8"))

def checkdetails(name,password):
    cur=con.cursor()
    query="select * from `login` where `user`='{}' and `password`='{}'". format(name,password)
    cur.execute(query)
    result=cur.fetchall()
    if result:
        return "found101"
    else:
        return "notfound404"

def createnewaccount(Client):
    while True:
        name_msg = Client.recv(BUFSIZE)
        n=json.loads(name_msg.decode("utf8"))
        for i in n.keys():
            key=i
        name=key
        password=n[key]
        print(name,password)
        cur=con.cursor()
        name_check="select * from `login` where `user`='{}'". format(name)
        cur.execute(name_check)
        result=cur.fetchall()
        if result:
            print("user name taken")
            Client.send(bytes("405",'utf-8'))
            continue
        else:
            query="insert into `login`(`user`,`password`) values('{}','{}')". format(name,password)
            cur.execute(query)
            con.commit()
            Client.send(bytes("404",'utf-8'))
            break
    
    return name

  
clients = {}
addresses = {}
name_address={}
name_client={}
HOST = socket.gethostname()
PORT = 65100
BUFSIZE = 4096
#ADDR = (HOST,PORT)

SERVER = socket.socket()
SERVER.bind((HOST,PORT))

if __name__ == "__main__":
    SERVER.listen(5)
    print("Waiting for connection...")
    ACCEPT_THREAD = Thread(target=accept_incoming_connections)
    ACCEPT_THREAD.start()
    ACCEPT_THREAD.join()
SERVER.close()
