import socket
PORT = 6999
if __name__ == '__main__':
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, PORT))
    s.listen(5)
    while True:
        c,addr = s.accept()
        c.send(b'Hi Bob, I am Alice\n')
        c.close()
        exit(1)