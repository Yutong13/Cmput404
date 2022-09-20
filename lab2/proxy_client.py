import socket

BufferSize = 1024

def main():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        print("Success: Socket")

        lan_ip = socket.gethostbyname("localhost")
        s.connect((lan_ip, 8001))

        print("Success: Connect")
        # input("$").encode()
        s.sendall(f'GET / HTTP/1.0\r\nHost: www.google.com\r\n\r\n'.encode())
        print("Success: Payload")

        s.shutdown(socket.SHUT_WR)

        full_str = b""
        while 1:
            recv = s.recv(BufferSize)
            if not recv:
                break
            full_str+=recv
        
        print(full_str)

    except Exception as e:
        print(e)
    
    finally:
        s.close()

main()