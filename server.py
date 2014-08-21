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
            print 'client ID='+clientID
            return "hello;"+clientID
    elif receivedMessage[:5] == 'hello':
        clientID = receivedMessage[6:]
        #generate puplic key
        auth[clientID]['key'] = hashlib.md5(''.join(random.sample(char_set*6, 15))).hexdigest().upper()
        auth[clientID]['encryptionStage'] = 1
        print auth[clientID]['key'] + "          public key"
        return auth[clientID]['key']
    if auth[receivedMessage[:32]]['encryptionStage'] == 1:
        if auth[receivedMessage[:32]]['key'] == receivedMessage[32:]:
            #generate first private key
            auth[receivedMessage[:32]]['key'] = hashlib.md5(''.join(random.sample(char_set*6, 15))).hexdigest().upper()
            encryptedFirstPrivateKey = AES.new(receivedMessage[32:], AES.MODE_CBC, IV).encrypt(hashlib.md5(''.join(random.sample(char_set*6, 15))).hexdigest().upper())
            print auth[receivedMessage[:32]]['key'] + "           firstPrivateKey"
            auth[receivedMessage[:32]]['encryptionStage'] = 2
            auth[receivedMessage[:32]]['key'] = encryptedFirstPrivateKey
            return encryptedFirstPrivateKey
    if auth[receivedMessage[:32]]['encryptionStage'] == 2:
        if auth[receivedMessage[:32]]['key'] == receivedMessage[32:]:
            #generate second private key
            encryptedSecondPrivateKey = AES.new(receivedMessage[32:], AES.MODE_CBC, IV).encrypt(hashlib.md5(''.join(random.sample(char_set*6, 15))).hexdigest().upper())
            auth[receivedMessage[:32]]['key'] = hashlib.md5(''.join(random.sample(char_set*6, 15))).hexdigest().upper()
            print auth[receivedMessage[:32]]['key'] + "           second Private Key"
            auth[receivedMessage[:32]]['key'] = encryptedSecondPrivateKey
            auth[receivedMessage[:32]]['encryptionStage'] = 3
            return auth[receivedMessage[:32]]['key']
    if auth[receivedMessage[:32]]['encryptionStage'] == 3:
        print AES.new(auth[receivedMessage[:32]]['key'], AES.MODE_CBC, IV).decrypt(receivedMessage[32:])






configArray=parseConfig('/usr/local/etc/bhyvemc/bhyvemc.conf')
print encryption('hello')
listenPort(configArray["listenPort"],configArray["listenIP"])
