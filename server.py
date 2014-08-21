__author__ = 'DmitryShumsky'
#This is server side script. Wait for connect on specified port
import string
from os import urandom
from Crypto.Cipher import AES
import select
import socket
global auth
import hashlib
import random
auth = {}
IV = 16 * '\x00'
char_set = string.ascii_uppercase + string.digits
def parseConfig(configFile):
#Parse main config file
    import csv
    import StringIO
    #global configArray
    configArray = {}
    configFileDescription = open(configFile, 'r')
    configFileContent = configFileDescription.readlines();
    #Parse config
    for contentString in configFileContent:
        if contentString[0]!="#":
            f = StringIO.StringIO(contentString)
            reader = csv.reader(f, delimiter='=')
            for row in reader:
                firstElem = row[0].strip()
                secondElem = row[1].strip()
                configArray[firstElem]=secondElem
    return configArray;
def listenPort(portNumber, listenIP):
#main function: listen specified port and handle requests

    portNumber=int(portNumber)
    global server_socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((listenIP, portNumber))
    server_socket.listen(5)
    print ('Listening on port',portNumber)

    read_list = [server_socket]
    while True:
        readable, writable, errored = select.select(read_list, [], [])
        for s in readable:
            if s is server_socket:
                client_socket, address = server_socket.accept()
                read_list.append(client_socket)
                #print "Connection from", address
            else:
                data = s.recv(2048)
                if data:
                    dataWithoutSymbols = data.strip()
                    dataToWrite = encryption(dataWithoutSymbols)
                    client_socket.send(str(dataToWrite))
                #else:
                    #s.close()
                    #read_list.remove(s)
def encryption(receivedMessage):
#in this function we generate, encrypt and decrypt all messages
    if receivedMessage == 'hello':
        clientID = hashlib.md5(urandom(120)).hexdigest().upper()
        try:
            auth[clientID]
        except KeyError:
            auth[clientID] = {'encryptionStage': 0, 'key':'','id':clientID}
            print clientID+'         client ID'
            return "hello;"+clientID
    elif receivedMessage[:5] == 'hello':
        clientID = receivedMessage[6:]
        #generate puplic key
        auth[clientID]['key'] = hashlib.md5(''.join(random.sample(char_set*6, 15))).hexdigest().upper()
        auth[clientID]['encryptionStage'] = 1
        print auth[clientID]['key'] + "          public key"
        return auth[clientID]['key']
    clientID = receivedMessage[:32]
    body = receivedMessage[32:]
    if auth[clientID]['encryptionStage'] == 1:
        if auth[clientID]['key'] == body:
            #generate first private key
            auth[clientID]['key'] = hashlib.md5(''.join(random.sample(char_set*6, 15))).hexdigest().upper()
            print auth[clientID]['key'] + "    first private key"
            encryptedFirstPrivateKey = AES.new(body, AES.MODE_CBC, IV).encrypt(auth[clientID]['key'])
        auth[clientID]['encryptionStage'] = 2
        return encryptedFirstPrivateKey
    if auth[clientID]['encryptionStage'] == 2:
        if auth[clientID]['key'] == body:
            print 'second private key'
            #generate second private key
            auth[clientID]['key'] = hashlib.md5(''.join(random.sample(char_set*6, 15))).hexdigest().upper()
            print auth[clientID]['key'] + '  second private key'
            encryptedSecondPrivateKey = AES.new(body, AES.MODE_CBC, IV).encrypt(auth[clientID]['key'])
            auth[clientID]['encryptionStage'] = 3
            pring
            return encryptedSecondPrivateKey





configArray=parseConfig('/usr/local/etc/bhyvemc/bhyvemc.conf')
#print encryption('hello')
listenPort(configArray["listenPort"],configArray["listenIP"])
