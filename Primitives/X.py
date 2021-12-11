from OT4 import *
PORT = 6999
from random import randint
from GMW import *
def X():#Xiang's solution
    while True:
        try:
            GMW_X()
        except:
            pass
def XxX():
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, 1025))
    s.listen(5)
    while True:
        client,addr = s.accept()
        GMW_X(client)
        client.close()
if __name__ == "__main__":
    XxX()