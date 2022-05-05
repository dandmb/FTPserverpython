import socket
import json
import os

HOST = 'localhost'
PORT = 12345
BUFSIZ = 1024
folderName="Received"
path=os.path.abspath(os.path.join(os.getcwd(), folderName))


def decodage(Dict,newContents):
    
    
    decodedContent=""
    code=""
    for c in newContents:
        code=code+c
        for mykey,myval in Dict.items():
            if myval==code:
                decodedContent=decodedContent+mykey
                code=""
    
    return decodedContent


def runClient():
    global HOST
    global PORT
    global BUFSIZ
    global folderName
    global path

    client_sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    #host = input("Enter hostname [%s]: " %HOST) or HOST
    #port = input("Enter port [%s]: " %PORT) or PORT
    sock_addr = (HOST, PORT)
    client_sock.connect(sock_addr)
    #payload = 'GET TIME'
    docselect=1
    # to help resend choice to server
    flash=0
    dict=""
    

    
    try:
        while True:
            if(flash==0):
                reception = client_sock.recv(BUFSIZ)
                print(reception.decode('utf-8'))
                docnum = input("Enter document number to download: ")
                client_sock.send(docnum.encode('utf-8'))
            
                data = client_sock.recv(BUFSIZ)
                if(data.decode('utf-8')=="Incorrect value"):
                    print(data.decode('utf-8'))
                else:

                    print("The selected file is %s "%data.decode('utf-8'))
                    fileName=data.decode('utf-8')
                    client_sock.send(docnum.encode('utf-8'))

                    data = client_sock.recv(BUFSIZ)
                    print("The encoded message is %s "%data.decode('utf-8'))
                    dec = "1"
                    
                    if(data):
                        client_sock.send(dec.encode('utf-8'))
                        dict=client_sock.recv(BUFSIZ)
                        print("The dictionary is %s "%dict.decode('utf-8'))
                        data_loaded = json.loads(dict)
                        message=decodage(data_loaded,data.decode('utf-8'))
                        print("The decoded message is : ",message)

                        if(os.path.exists(path)):
                            with open(path+"//"+fileName, 'w') as f:
                                f.write(message)
                        else:
                            os.mkdir(path)
                            with open(path+"//"+fileName, 'w') as f:
                                f.write(message)

                more = input("Do you Want to download more files from the server[y/n]:")
                if more.lower() == 'y':
                    docnum = input("Enter document number to download: ")
                    flash=flash+1
                else:
                    break
            else:
                client_sock.send(docnum.encode('utf-8'))
            
                data = client_sock.recv(BUFSIZ)
                

                if(data.decode('utf-8')=="Incorrect value"):
                    print(data.decode('utf-8'))
                else:

                    print("The selected file is %s "%data.decode('utf-8'))
                    fileName=data.decode('utf-8')
                    client_sock.send(docnum.encode('utf-8'))

                    data = client_sock.recv(BUFSIZ)
                    print("The encoded message is %s "%data.decode('utf-8'))
                    dec = "1"
                    
                    if(data):
                        client_sock.send(dec.encode('utf-8'))
                        dict=client_sock.recv(BUFSIZ)
                        print("The dictionary is %s "%dict.decode('utf-8'))
                        data_loaded = json.loads(dict)
                        message=decodage(data_loaded,data.decode('utf-8'))
                        print("The decoded message is : ",message)

                        if(os.path.exists(path)):
                            with open(path+"//"+fileName, 'w') as f:
                                f.write(message)
                        else:
                            os.mkdir(path)
                            with open(path+"//"+fileName, 'w') as f:
                                f.write(message)

                more = input("Do you Want to download more files from the server[y/n]:")
                if more.lower() == 'y':
                    docnum = input("Enter document number to download: ")
                    flash=flash+1
                else:
                    break

    except KeyboardInterrupt:
        print("Exited by user")
    client_sock.close()


runClient()