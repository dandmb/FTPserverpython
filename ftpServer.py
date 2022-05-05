from pydoc import doc
import socket
from time import ctime
import os
import json

# Get the list of all files and directories
dirName="myfiles"
path=os.path.abspath(os.getcwd())+"//"+dirName


dir_list = os.listdir(path)

allfiles="Files to be downloaded"

# pour le decodage
code=""
# contenu du fichier
contents=""
# message codE en binary
newContents=""
# lettres unique du fichier
compressedContent=""
# du binary message en lettre
decodedContent=""
# characters for huffman tree
chars=[]
# frequency of characters
freq=[]
# list containing unused nodes
nodes = []

huffVal=[]
huffCode=[]
Dict = {}

# Initialisation des infos pour le server

HOST = 'localhost'
PORT = 12345
BUFSIZ = 1024
ADDR = (HOST, PORT)

server_socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server_socket.bind(ADDR)
server_socket.listen(5)
server_socket.setsockopt( socket.SOL_SOCKET,socket.SO_REUSEADDR, 1 )

# liste des fichiers se trouvant dans mon dossier
def listOffiles():
    global allfiles
    for i in range(len(dir_list)):
        if(i==0):
            allfiles=allfiles+'\n\n'
            allfiles=allfiles+str(i+1)+'. '+dir_list[i]+'\n'
        else:
            allfiles=allfiles+str(i+1)+'. '+dir_list[i]+'\n'



# A Huffman Tree Node
class node:
	def __init__(self, freq, symbol, left=None, right=None):
		# frequency of symbol
		self.freq = freq

		# symbol name (character)
		self.symbol = symbol

		# node left of current node
		self.left = left

		# node right of current node
		self.right = right

		# tree direction (0/1)
		self.huff = ''


#Lecture du contenu du fichier a envoyer
def readContent(filename):
    global contents
    global path
    with open(path+"//"+filename) as f:
        contents = f.read()
        #print(contents)

    return contents

#calcul de la frequence de lettres
def frequenceCalc(mystr):
    global chars
    global freq
    global compressedContent
    for str in mystr:
        frequence=mystr.count(str)
        # number of times element exists in list
        exist_count = chars.count(str)

        # checking if it is more then 0
        if exist_count <= 0:
            chars.append(str)
            compressedContent=compressedContent+str
            freq.append(frequence)

# utility function to print huffman
# codes for all symbols in the newly
# created Huffman tree
def printNodes(node, val=''):

    global huffVal
    global huffCode
    global Dict
    # huffman code for current node
    
    newVal = val + str(node.huff)
	
    # if node is not an edge node
	# then traverse inside it
    if(node.left):
        printNodes(node.left, newVal)
    if(node.right):
        printNodes(node.right, newVal)

		# if node is edge node then
		# display its huffman code
    if(not node.left and not node.right):
        
        Dict[node.symbol]=newVal

# Convertir les contenus du fichier en binary
def encodage():
    global Dict
    global contents
    global newContents

    for c in contents:
        newContents=newContents+Dict[c]

# construction du huffman tree
def huffman():
    global nodes
    for x in range(len(chars)):
        nodes.append(node(freq[x], chars[x]))

    while len(nodes) > 1:
        # sort all the nodes in ascending order
        # based on theri frequency
        nodes = sorted(nodes, key=lambda x: x.freq)

        # pick 2 smallest nodes
        left = nodes[0]
        right = nodes[1]

        # assign directional value to these nodes
        left.huff = 0
        right.huff = 1

        # combine the 2 smallest nodes to create
        # new node as their parent
        newNode = node(left.freq+right.freq, left.symbol+right.symbol, left, right)

        # remove the 2 nodes and add their
        # parent as new node among others
        nodes.remove(left)
        nodes.remove(right)
        nodes.append(newNode)


# Lancer le serveur

def runServer():
    listOffiles()
    global server_socket
    global allfiles
    global BUFSIZ
    global dir_list
    global newContents
    
    global chars
    global freq
    global nodes
    global Dict

    global newContents

    while True:
        print('Server waiting for connection...')
        client_sock, addr = server_socket.accept()

        print('Client connected from: ', addr)

        
        client_sock.send(bytes(allfiles, 'utf-8'))
        


        while True:
            # reunitialisation en cas du second appel pour les variables communes
            chars.clear()
            freq.clear()
            nodes.clear()
            Dict.clear()
            newContents=""

            data = client_sock.recv(BUFSIZ)
            if not data or data.decode('utf-8') == 'END':
                break
            print("The number received from the client: %s" % data.decode('utf-8'))
            docid=int(data.decode('utf-8'))

            if(docid):
                if(docid>len(dir_list) or docid<=0):
                    print("The selected number is incorrect")
                    client_sock.send(bytes("Incorrect value", 'utf-8'))
                else:
                    
                    print("Sending the file name %s to the client"%dir_list[docid-1])
                    client_sock.send(bytes(dir_list[docid-1], 'utf-8'))

                    data = client_sock.recv(BUFSIZ)

                    contents=readContent(dir_list[docid-1])
                    print("The content of the file is: %s" %contents)
                    frequenceCalc(contents)
                    huffman()
                    printNodes(nodes[0])
                    encodage()

                    try:
                        client_sock.send(bytes(newContents, 'utf-8'))
                        dicsign = client_sock.recv(BUFSIZ)
                        data_string = json.dumps(Dict)
                        client_sock.send(bytes(data_string, 'utf-8'))
                    except KeyboardInterrupt:
                        print("Exited by user")
            else:
                print("The selected number is incorrect")
                client_sock.send(bytes("Incorrect value", 'utf-8'))
                
        client_sock.close()
    server_socket.close()


# Lancer le serveur


runServer()

