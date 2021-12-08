# 1-4 OT in GMW according http://people.eecs.berkeley.edu/~sanjamg/classes/cs276-fall14/scribe/lec16.pdf
# n132
import utils

def OT2():
# 1-2 OT is reconstructed from the OT I build several days ago-

# ALICE
import socket
PORT = 6999
from random import randint
from utils import *
def otEncrypt(g,p,pk,s):
    r=randint(1,p-1)
    tmp= n2b(pow(g,r,p))
    tmp2 = bytes_to_long(hash( n2b( pow(pk,r,p) ) )) ^ bytes_to_long(s)
    return tmp+b'-'+n2b(tmp2)
def OT_Alice(message,client):
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
    assert(c== (pks[0] * pks[1])% p)
    sec = message
    data=b""
    data+= otEncrypt(g,p,pks[0],sec[0])
    data+=b'-'
    data+= otEncrypt(g,p,pks[1],sec[1])
    client.send(data)
    client.close()
def Alice():
    s = socket.socket()
    host = socket.gethostname()
    s.bind((host, PORT))
    s.listen(5)
    while True:
        client,addr = s.accept()
        OT_Alice([b"This is secret 0",b"This is secret 1"],client)
    

if __name__ == '__main__':
    Alice()