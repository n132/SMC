import gmpy2
import hashlib
def powm(m,e,n):
    #pow + mod
    return gmpy2.powmod(m,e,n)
def hash(t):
    h = hashlib.new('sha512_256')
    h.update(t)
    return h.hexdigest()
if __name__ == "__main__":
    print(hash(b"1231"))