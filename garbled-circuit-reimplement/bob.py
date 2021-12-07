import zmq
import time

socket = zmq.Context().socket(zmq.REP)
socket.bind("tcp://*:5555")


while True:
    message = socket.recv()

    print("bob received request: %s" % message)

    time.sleep(1)

    socket.send(b"World")