import zmq
import util
from garble import *

socket = zmq.Context().socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

# need keys

circuit = Circuit()
keys = circuit.all_key()

#print(circuit.all_key())



socket.send(b"Hello")

message = socket.recv()
print("alice received reply [ %s ]" % (message))

