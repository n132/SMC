from OT4 import *
from GMW import *
PORT =1025
def X():#Xiang's solution
    while True:
        try:
            GMW_X()
        except:
            pass
def XxX():
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host,PORT))
    s.listen(5)
    while True:
        client,addr = s.accept()
        GMW_X(client)
        client.close()
if __name__ == "__main__":
    XxX()