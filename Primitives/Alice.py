import socket
PORT = 6999
from random import randint
from utils import *
def otEncrypt(g,p,pk,s):
    r=randint(1,p-1)
    tmp= n2b(pow(g,r,p))
    tmp2 = bytes_to_long(hash( n2b( pow(pk,r,p) ) )) ^ bytes_to_long(s)
    return tmp+b'-'+n2b(tmp2)
def getSec():
        return [b"This is secret 0",b"This is secret 1"]
if __name__ == '__main__':
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, PORT))
    s.listen(5)
    while True:
        client,addr = s.accept()
        client.send(b"Hi")
        data= client.recv(1024)

        p, g=data.split(b"-")
        p = int(p)
        g = int(g)
        c = randint(1,p-1)
        client.send(n2b(c))
        data = client.recv(1024)
        pks = data.split(b"-")
        pks[0] = int(pks[0])
        pks[1] = int(pks[1])
        print(c,pks)
        print((pks[0] * pks[1])% p)
        assert(c== (pks[0] * pks[1])% p)
        sec = getSec()
        data=b""
        data+= otEncrypt(g,p,pks[0],sec[0])
        data+=b'-'
        data+= otEncrypt(g,p,pks[1],sec[1])
        #print(data)
        client.send(data)
        client.close()