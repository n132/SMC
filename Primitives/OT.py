# n132
import logging
from utils import *
import gmpy2
from Crypto.Random  import random

def getRamdom(length):
    return gmpy2.mpz_urandomb(gmpy2.random_state(),1024)

# class Ot(object):
#     # Bellare-Micali Protocal
#     def __init__(self,id) -> None:
#         super().__init__()
#         if(id=='Alice'):
#             self.id=0
#         elif(id=='Bob'):
#             self.id=1
#         else:
#             exit(0)
#     def Alice(self):
#         self.connect()
#         c=self.getRandom()
#         self.send(c)
        
#         pks = self.recv()
#         #pk=[]
#         pk= getPkublicKeys(pks)
#         assert(pk[0]*pk[1]==c)
#         r0 = random.getrandbits()
#         r1 = random.getrandbits()
#         secret = self.getSec()
#         self.send(((pow(g,r0,p),hash(pow(pk[0],r0,p)) ^ secret[0] )),(pow(g,r1,p),hash(pow(pk[1],r1,p)) ^ secret[0] ) ))


#     def Bob(self):
#         self.connect()
#         c = self.recv()

#         k= self.getRandom()
#         print("Which secret do you like to get?")
#         b = input()
#         if(b not in [0,1]):
#             exit(0)
#         pk=[0,0]
#         pk[b] = pow(g,k,p)
#         pk[1-b] = c/pk[b]

#         self.send((pk[0],pk[1]))
#         data = self.recv()
#         data = data[b]
#         res = data[1] ^ hash(pow(data[0],k,p))
#         print("I get the secret:", res)
#         exit(1)
class Alice(object):
    def __init__(self, s) -> None:
        self.socket = s
    def get_g(self):
        g = int(self.socket.recv())
        print(g)
        return g
    def getSec(self):
        return ["This is secret 1","This is secret 2"]
    
    
class Bob(object):
    pass
