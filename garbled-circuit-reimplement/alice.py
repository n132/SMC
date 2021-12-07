import zmq

socket = zmq.Context().socket(zmq.REQ)
socket.connect("tcp://localhost:5555")

socket.send(b"Hello")

message = socket.recv()
print("alice received reply [ %s ]" % (message))