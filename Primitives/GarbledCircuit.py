#n132
def AND(a,b):
    return a and b
def OR(a,b):
    return a or b
def XOR(a,b):
    return a^b
    

from utils import *
class GarbledGates(object):
    def __init__(self,wire_a,wire_b,logic) -> None:
        super().__init__()
        if(logic==b"AND" or logic == b"and"):
            self.gate = AND
        elif(logic==b"OR" or logic == b"or"):
            self.gate = OR
        elif(logic==b"XOR" or logic == b"xor"):
            self.gate = XOR
        else:
            exit(1)
        self.a =wire_a
        self.b =wire_b
        self.k =None
        self.c =None
        self.keys = [[0,0],[0,0],[0,0]]
    def GetKeys(self):
        for x in range(3):
            for y in range(2):
                self.keys[x][y] = kengen()
        return self.keys
    def encCircuit(self):
        #-----------------------------------
        self.k = []
        for x in range(3):
            for y in range(2):
                self.k[x][y] = encrypt(self.keys[x][y],str(y).encode('utf8'))
        #-----------------------------------
        ptr = self.keys
        self.c=[]
        for x in range(2):
            tmp = []
            for y in range(2):
                content  = self.k[2][self.gate(x,y)]
                tmp.append( encrypt(ptr[0][x],encrypt(ptr[1][y],content)) )
            self.c.append(tmp)
        #-----------------------------------
        
        #---------------------------------------------
        #---------------------------------------------
        #---------------------------------------------
        #---------------------------------------------
        #---------------------------------------------
        #---------------------------------------------
    def genGC(self):
        encCircuit()
        
if __name__ == "__main__":
    a= GarbledGates(1,2,3)
    for x in a.GetKeys():
        print(x) 