import socket
from utils import *
BigPrime = 4776913109852041418248056622882488319

def OT_Encrypt(g,p,pk,s):
    r=randint(1,p-1)
    tmp= n2b(pow(g,r,p))
    tmp2 = bytes_to_long(hash( n2b( pow(pk,r,p) ) )) ^ bytes_to_long(s)
    return tmp+b'-'+n2b(tmp2)

def OT_Receiver(choice,s):
    m= s.recv(8)
    if(m==b'n132-OT2'):
        GC = CyclicGroup(BigPrime)
        g = GC.generator
        data = n2b(BigPrime)+b"-"+n2b(g)
        s.send(data)
        c = int(s.recv(1024))
        k = GC.rand_int()
        pks=[0,0]
        b = choice
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
        return res
    else:
        s.close()
        return -1

def OT_Sender(message,client):
    client.send(b"n132-OT2")
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
    data+= OT_Encrypt(g,p,pks[0],sec[0])
    data+=b'-'
    data+= OT_Encrypt(g,p,pks[1],sec[1])
    client.send(data)
    client.close()