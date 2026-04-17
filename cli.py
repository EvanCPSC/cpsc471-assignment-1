#Client code
from socket import *
import sys

#Check if the correct number of command-line arguments is provided
if(len(sys.argv) != 2):
    print("Usage: python cli.py <port>")
    sys.exit(1)

#Name and port of the server to connect to
serverName = 'localhost'
serverPort = int(sys.argv[1]) #Port number should be passed as a command-line argument (int is used for typecasting)

#Create a TCP client socket
clientSocket = socket(AF_INET,SOCK_STREAM)

#Connect to the server
clientSocket.connect((serverName, serverPort))

while True:
    #Get line from user input
    client_line = input("ftp> ")

    #Check if the user wants to quit
    if client_line == "quit":
        print("Exiting the client.")
        break
    elif client_line == "ls":
        print("Listing files on the server...")
        # This should be the logic to send a request to the server to list files and receive the response   
    elif client_line == "get":
        print("Getting file from the server...")
        # This should be the logic to send a request to the server to get a file and receive the response   
    elif client_line == "put":
        print("Putting file on the server...")
        # This should be the logic to send a request to the server to put a file and receive the response
    else:
        print("Invalid command. Please enter 'ls', 'get', 'put', or 'quit'.")


