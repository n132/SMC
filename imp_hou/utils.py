import json
import os
import zmq
import gmpy2
import sympy
import socket
import hashlib
from random import randint

LOCAL_PORT = 4080
SERVER_HOST = "127.0.0.1"
SERVER_PORT = 4080

L = 256

"""
# ---ZMQ utilities---

class Socket:
    def __init__(self, socket_type):
        self.socket = zmq.Context().socket(socket_type)

    def send(self, msg):
        self.socket.send_pyobj(msg)

    def receive(self):
        return self.socket.recv_pyobj()
    
    def send_wait(self, msg):
        self.send(msg)
        return self.receive()


# Socket for evaluating side
class BSocket(Socket):
    def __init__(self, endpoint=f"tcp://*:{LOCAL_PORT}"):
        super().__init__(zmq.REP)
        self.socket.bind(endpoint)

# Socket for garbling side
class ASocket(Socket):
    def __init__(self, endpoint=f"tcp://{SERVER_HOST}:{SERVER_PORT}"):
        super().__init__(zmq.REQ)
        self.socket.connect(endpoint)
"""

def pack(s, splitter=b'-'): # pack numbers
    res = b''
    for x in s:
        res += n2b(x)+splitter
    if(res==b''):
        return res
    return res[:-1]

def hash(t):
    #Test Passed
    h = hashlib.new('sha512_256')
    h.update(t)
    return h.hexdigest().encode('utf8')

def n2b(n):
    return str(n).encode("utf8")

def nbit_prime(l = L):
    bstr = os.urandom(l//8) # 2048-bit-random
    rnum = int.from_bytes(bstr, "big") # convert the bytes to long
    return gmpy2.next_prime(rnum) # get the next prime  

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


# socket utilities

def connect():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((SERVER_HOST, LOCAL_PORT))
    return s

def listen():
    serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    serversocket.bind((SERVER_HOST, LOCAL_PORT))
    serversocket.listen(5)
    return serversocket