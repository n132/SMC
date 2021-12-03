import math
import gmpy2
from gmpy2 import mpz
import hashlib
import os
from random import randint
import socket
from Crypto.Util.number import *
import sympy

L = 256
PORT = 6999
ADDR = "127.0.0.1"
def n2b(n):#avoiding bad split
    return str(n).encode("utf8")
def pack(s,spliter=b'-'):#pack numbers
    res= b''
    for x in s:
        res += n2b(x)+spliter
    if(res==b''):
        return res
    return res[:-1]
def hash(t):
    #Test Passed
    h = hashlib.new('sha512_256')
    h.update(t)
    return h.hexdigest().encode('utf8')
def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((ADDR, PORT))
    return s
def listen():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((socket.gethostname(), PORT))
    serversocket.listen(5)
def nbit_prime(l = L):
    bstr = os.urandom(l//8)# 2048-bit-random
    rnum = bytes_to_long(bstr)# convert the bytes to long
    return gmpy2.next_prime(rnum)# get the next prime              
def ext(s):
    print("[!]",s)
    exit(0)
class CyclicGroup:# Cyclic group
    # test passed
    def __init__(self, p=None, g=None):
        self.p = p or nbit_prime() # get prime
        self.generator = g or self.find_generator()
    def mul(self, num1, num2):
        return (num1 * num2) % self.p
    def div(self,a,b):
        return self.mul(a,pow(b,self.p-2,self.p))
    def pow(self, base, exponent):
        return pow(base, exponent, self.p)
    def rand_int(self):
        return randint(1, self.p - 1)
    def find_generator(self):
        factors = sympy.primefactors(self.p-1)

        while True:
            candidate = self.rand_int()
            for factor in factors:
                if 1 == self.pow(candidate, (self.p -1) // factor):
                    break
            else:
                return candidate
        # fac = factor(self.p-1)
        # while True:
        #     t = self.rand_int()
        #     for i in fac:
        #         if pow(t, (self.p -1)//i):
        #             break
        #     else:
        #         return t
        # s = set(range(1, self.p))
        # for a in s:
        #     print(a)
        #     g = set()
        #     for x in s:
        #         g.add(pow(a,x,self.p))
        #     if g == s:
        #         return a
        # ext("find_generator.")

if __name__ == "__main__":
    print(hash(b"12222222222"))
    #print(factor(4776913109852041418248056622882488319))
    # p = 4776913109852041418248056622882488319
    # a =  CyclicGroup(p)
    # print("init finished")
    # k = a.rand_int()#get k
    # g = a.generator
    # h = a.pow(g,k)
    
    # r = a.rand_int()
    # u = a.pow(g,r)
    # m = bytes_to_long(b"n132")
    # print("g:",g)
    # print("k:",k)
    # print("h",a.pow(g,k))
    # v = a.mul(m,a.pow(h,r))
    # print(long_to_bytes(a.div(v,pow(u,k,p))))
