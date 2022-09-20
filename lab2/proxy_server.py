import socket
import time
import multiprocessing as mtp

HOST = "127.0.0.1"
PORT = 8001
BUFFER_SIZE = 4096
Google = "www.google.com"

def main():
    
    # try:
    #     sgoogle = socket.socket(socket.AN_INET, socket.SOCK_STREAM)
    
    # except (msg):
    #     print(f'Socket to google failed. Error: {"".join(msg)}')

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sclient:
        sclient.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        sclient.bind((HOST, PORT))

        sclient.listen(2)

        while True:
            connection, address = sclient.accept()

            p = mtp.Process(target=handle_client, args=(connection, address))
            # p.daemon = True
            p.start()
            print("Process starts")

def handle_client(connection, address):
    message = b""
    # listen to client
    while 1:
        data = connection.recv(BUFFER_SIZE)
        # print(data)
        if not data:
            break
        message+=data
    # print(message)

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        s.settimeout(1)
        # connect to google
        google_ip = socket.gethostbyname(Google)
        s.connect((google_ip, 80))
        
        
        s.sendall(message)

        # waiting for google
        message = b""
        
        while 1:
            try:
                mesage = s.recv(BUFFER_SIZE)
                if not mesage:
                    break
                message+=mesage
            except TimeoutError as e:
                print(e)
                break

        s.shutdown(socket.SHUT_RDWR)

        # send reply to client
        connection.sendall(message)
        connection.shutdown(socket.SHUT_RDWR)
        connection.close()

if __name__ == "__main__":
    main()
