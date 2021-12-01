# n132
#
# 
from Crypto.PublicKey import ECC
from Crypto.Random  import random
key = ECC.generate(curve='P-256')
f = open('myprivatekey.pem','wt')
f.write(key.export_key(format='PEM'))
f.close()

f = open('myprivatekey.pem','rt')
key = ECC.import_key(f.read())


def keyGen(self):
    if(self.id==0):
        return
        else:
            

class Ot(object):
    # Bellare-Micali Protocal
    def __init__(self,id) -> None:
        super().__init__()
        
        if(id=='S'):#Reciever
            self.id=0
        elif(id=='R'):#Sender
            self.id=1
        else:
            exit(0)

    def connect():
        pass 
    def send():
        pass
    def hash():
        pass        
    def getRandom():
        return random.getrandbits(2048)

    def Alice(self):
        self.connect()
        c=self.getRandom()
        self.send(c)
        pks = self.recv()
        #pk=[]
        pk= getPkublicKeys(pks)
        assert(pk[0]*pk[1]==c)
        c=[]
        c.append(hash(pk[0]))
        c.append(hash(pk[1]))

    def Bob(self):
        
        self.connect()
        c = self.recv()
        k= self.getRandom()
        pk1 = pow(g,k)
        pk2 = c/pk1
        self.send((pk1,pk2))
        self.recv()
        