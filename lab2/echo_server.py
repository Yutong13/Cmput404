#!/usr/bin/env python3
import socket
import time
from multiprocessing import Process

#define address & buffer size
HOST = "127.0.0.1"
PORT = 8001
BUFFER_SIZE = 1024

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
        #QUESTION 3
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        #bind socket to address
        s.bind((HOST, PORT))
        #set to listening mode
        s.listen(2)

        #continuously listen for connections
        while True:
            conn, addr = s.accept()
            print("Connected by", addr)
            p = Process(target=handle_client, args=(conn,))
            p.start()
            conn.close()

def handle_client(client_socket):
    #receive data, wait a bit, then send it back
    full_data = client_socket.recv(BUFFER_SIZE) 
    time.sleep(0.5)
    client_socket.sendall(full_data)
    
    client_socket.shutdown(socket.SHUT_RD)

if __name__ == "__main__":
    main()
