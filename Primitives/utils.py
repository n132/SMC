import gmpy2
import hashlib
import binascii
PORT = 6999
ADDR = "127.0.0.1"
def powm(m,e,n):
    #pow + mod
    return gmpy2.powmod(m,e,n)
def hash(t):
    #Test Passed
    h = hashlib.new('sha512_256')
    h.update(t)
    return h.hexdigest()
import socket
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADDR, PORT))
    return s
def listen():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), PORT))
    serversocket.listen(5)

if __name__ == "__main__":
    cmd = input()
    if("1" in cmd):
        connect()
    else:
