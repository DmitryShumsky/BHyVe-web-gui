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
    print firstPrivateKey + '         received first private key'
    privateKey = AES.new(publicKey, AES.MODE_CBC, IV).decrypt(firstPrivateKey)
    print privateKey+'     first private key'
    serverAnswer = connectToServer('localhost',9001,clientID+firstPrivateKey)
    secondPrivateKey = AES.new(privateKey, AES.MODE_CBC, IV).decrypt(serverAnswer)
    print secondPrivateKey + '           second private key'
    command = AES.new(secondPrivateKey, AES.MODE_CBC, IV).encrypt('first encrypted command')
    serverAnswer = connectToServer('localhost',9001,clientID+command)
    print serverAnswer
    #if auth == 0:
    #receivedData =
        #return configArray;

decrypt()
