from OT2 import *
PORT = 6999
from random import randint

def Alice_OT2():
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, PORT))
    s.listen(5)
    while True:
        client,addr = s.accept()
        OT_Sender([b"This is secret 0",b"This is secret 1"],client)
    
if __name__ == '__main__':
    Alice_OT2()