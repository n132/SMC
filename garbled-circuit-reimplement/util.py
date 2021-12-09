from cryptography.fernet import Fernet
import random

def gen_key():
    return Fernet.generate_key()

def gen_pbits(num):
    pbits = [0]
    for i in range(num):
        pbits.append(random.randrange(0, 2))
    #print("pbits:", pbits)
    return pbits

