#Client code
from socket import *
import sys, os

#Check if the correct number of command-line arguments is provided
if(len(sys.argv) != 3):
    print("Usage: python cli.py <<port>")
    sys.exit(1)

#Name and port of the server to connect to
serverName = str(sys.argv[1])
serverPort = int(sys.argv[2]) #Port number should be passed as a command-line argument (int is used for typecasting)

#Create a TCP client socket
clientSocket = socket(AF_INET,SOCK_STREAM)

#Connect to the server
clientSocket.connect((serverName, serverPort))

def validFile(input):
    return len(input.split(".")) == 2

def put(fileName):
    # Reads file
    fileObj = open(fileName, "r")
    fileData = fileObj.read(65536)

    # Executes until all data from file has been sent
    while fileData:
        dataSizeStr = str(len(fileData))

        # Prepends data with length of data
        while len(dataSizeStr) < 10:
            dataSizeStr = "0" + dataSizeStr
        
        fileData = dataSizeStr + fileData

        numSent = 0

        while len(fileData) > numSent:
            numSent += clientSocket.send(fileData[numSent:])

        fileData = fileObj.read(65536)

    print("Sent " + fileName)


while True:
    #Get line from user input
    client_line = input("ftp> ")
    cmd = client_line.split()

    #Check if the user wants to quit
    if cmd[0] == "quit":
        print("Exiting the client.")
        break
    elif cmd[0] == "ls":
        print("Listing files on the server...")
        ls = os.listdir(os.getcwd())
        res = ""
        for i in ls:
            res += i + "  "
        print(res)
        # This should be the logic to send a request to the server to list files and receive the response   
    elif cmd[0] == "get":
        if len(cmd) == 1:
            print("Please provide a file name...")
        else:
            if not validFile(cmd[1]):
                print("Please provide a valid file...")
            else:
                ls = os.listdir(os.getcwd())
                if cmd[1] not in ls:
                    print("File not found in the server...")
                else:
                    print("Getting file from the server...")
                    put(cmd[1])
        # This should be the logic to send a request to the server to get a file and receive the response   
    elif cmd[0] == "put":
        if len(cmd) == 1:
            print("Please provide a file name...")
        else:
            if not validFile(cmd[1]):
                print("Please provide a valid file...")
            else:
                ls = os.listdir(os.getcwd())
                if cmd[1] in ls:
                    print("File already in the server...")
                else:
                    print("Putting file in the server...")
        # This should be the logic to send a request to the server to put a file and receive the response
    else:
        print("Invalid command. Please enter 'ls', 'get', 'put', or 'quit'.")

