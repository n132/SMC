import socket
from utils import *
PORT = 6999
BigPrime = 4776913109852041418248056622882488319
def OT_Bob(cmd,s):
    m= s.recv(2)
    if(m==b'Hi'):
        GC = CyclicGroup(BigPrime)
        g = GC.generator
        data = n2b(BigPrime)+b"-"+n2b(g)
        s.send(data)
        c = int(s.recv(1024))
        k = GC.rand_int()
        pks=[0,0]
        b = cmd
        pks[b] = GC.pow(g,k)
        pks[b-1] = GC.div(c,pks[b])
        
        s.send(pack(pks))
        data = s.recv(1024).split(b"-")
        b = b*2
        u = data[b]
        v = data[b+1]
        u = int(u)
        v = int(v)
        res=long_to_bytes( bytes_to_long(hash(n2b(GC.pow(u,k))))  ^ v )
        s.close()
        return int(res[-1:])
    else:
        s.close()
        return 2

def Bob(cmd):
    s = socket.socket()
    host = socket.gethostname()
    s.connect((host, PORT))
    return OT_Bob(cmd,s)

if __name__ == "__main__":
    ct = 0 
    for x in range(1000):
        exp = randint(0,1)
        if(exp != Bob(exp)):
            ct +=1
    print((1000-ct)/1000)