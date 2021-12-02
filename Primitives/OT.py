# n132
#
# 
from utils import *
import gmpy2
from Crypto.PublicKey import ECC,XOR
from Crypto.Random  import random
key = ECC.generate(curve='P-256')
f = open('myprivatekey.pem','wt')
f.write(key.export_key(format='PEM'))
f.close()

f = open('myprivatekey.pem','rt')
key = ECC.import_key(f.read())
def getRamdom(length):
    return gmpy2.mpz_urandomb(gmpy2.random_state(),1024)


            

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
    
    def getRandom():
        return random.getrandbits(2048)
    def getSec():
        res=[]
        print("Give me two sec:")
        res.append(input())
        res.append(input())
    def Alice(self):

        self.connect()
        c=self.getRandom()
        self.send(c)
        
        pks = self.recv()
        #pk=[]
        pk= getPkublicKeys(pks)
        assert(pk[0]*pk[1]==c)
        r0 = random.getrandbits()
        r1 = random.getrandbits()
        secret = self.getSec()
        self.send(( (powm(g,r0,p),hash(powm(pk[0],r0,p)) ^ secret[0] )),(powm(g,r1,p),hash(powm(pk[1],r1,p)) ^ secret[0] ) ))


    def Bob(self):
        self.connect()
        c = self.recv()

        k= self.getRandom()
        print("Which secret do you like to get?")
        b = input()
        if(b not in [0,1]):
            exit(0)
        pk=[0,0]
        pk[b] = powm(g,k,p)
        pk[1-b] = c/pk[b]

        self.send((pk[0],pk[1]))
        data = self.recv()
        data = data[b]
        res = data[1] ^ hash(powm(data[0],k,p))
        print("I get the secret:", res)
        exit(1)
