# 1-4 OT in GMW according http://people.eecs.berkeley.edu/~sanjamg/classes/cs276-fall14/scribe/lec16.pdf
# n132
import utils
from OT2 import *
from random import randint

def SGnenerator():
    S = []
    for _ in range(6):
        S.append(randint(0,1))
    return S
def OT4_Encrypt(S,m):
    assert(len(S)==6 and len(m)==4)
    res=[]
    res.append(
        S[0] ^ S[2] ^ m[0]
    )
    res.append(
        S[0] ^ S[3] ^ m[1]
    )
    res.append(
        S[1] ^ S[4] ^ m[2]
    )
    res.append(
        S[1] ^ S[5] ^ m[3]
    )
    return res

def OT4_Sender():
    pass
def OT4_Receiver():
    pass
# 1-2 OT is reconstructed from the OT I build several days ago-


if __name__ == '__main__':
    OT4_Sender()