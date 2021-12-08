from OT2 import *
PORT = 6999
def Bob(cmd):
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, PORT))
    return OT_Receiver(cmd,s)

if __name__ == "__main__":
    ct = 0 
    for x in range(1000):
        exp = randint(0,1)
        if(exp != Bob(exp)):
            ct +=1
    print((1000-ct)/1000)