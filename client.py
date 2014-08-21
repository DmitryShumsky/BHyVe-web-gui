__author__ = 'DmitryShumsky'
from Crypto.Cipher import AES
import select
import socket
import csv
import StringIO
global auth
import random
import hashlib
def connectToServer(serverIP, serverPort, message):
    sock = socket.socket()
    sock.connect((serverIP, serverPort))
    sock.send(message)
    data = sock.recv(2048)
    sock.close()
    return data
def decrypt():
#send hello to server
    IV = 16 * '\x00'
    receivedData = connectToServer('localhost',9001,'hello')
    print receivedData+"   - data after hello (client ID)"
        #for contentString in receivedData:
    clientID = receivedData[6:]
    print clientID + "     - client ID"
    publicKey = connectToServer('localhost',9001,"hello;"+clientID)
    print publicKey+'   - public key'
    firstPrivateKey = connectToServer('localhost',9001,clientID+publicKey)
    #print firstPrivateKey
    privateKey = AES.new(publicKey, AES.MODE_CBC, IV).decrypt(firstPrivateKey)
    print privateKey + '         firstPrivateKey'
    secondPrivateKey = connectToServer('localhost',9001,clientID+firstPrivateKey)
    print(secondPrivateKey)
    secondPrivateKeyDecr = AES.new(privateKey, AES.MODE_CBC, IV).decrypt(secondPrivateKey)
    print secondPrivateKeyDecr+'        - second private key'

    #if auth == 0:
    #receivedData =
        #return configArray;

decrypt()
