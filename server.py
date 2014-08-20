__author__ = 'DmitryShumsky'
#This is server side script. Wait for connect on specified port
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
    import select
    import socket
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
                data = s.recv(1024)
                if data:
                    dataWithoutSymbols = data.strip()
                    dataToWrite = encryption(dataWithoutSymbols)
                    client_socket.send(dataToWrite)
                else:
                    s.close()
                    read_list.remove(s)
def encryption(receivedMessage,clientIP):
#in this function we generate, encrypt and decrypt all messages
    from os import urandom
    from Crypto.Cipher import AES
    auth = {}
        if receivedMessage == 'hello':
            auth[clientIP] = 1
            return urandom(32)
        else:
            if auth[clientIP] == 1:
                









configArray=parseConfig('/usr/local/etc/bhyvemc/bhyvemc.conf')
print encryption('asdasdasd')
listenPort(configArray["listenPort"],configArray["listenIP"])
