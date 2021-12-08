from OT2 import *
PORT = 6999
def Bob_OT2(cmd):
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, PORT))
    res= OT_Receiver(cmd,s)
    s.close()
    return res
if __name__ == "__main__":
    ct = 0 
    for x in range(1000):
        exp = randint(0,1)
        if(exp != int(Bob_OT2(exp)[-1:])):
            ct +=1
    print((1000-ct)/1000)