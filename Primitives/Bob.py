import socket
PORT = 6999
if __name__ == '__main__':
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, PORT))
    print(s.recv(1024))
    s.close()