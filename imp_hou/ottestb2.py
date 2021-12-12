import cgarbl2
import gcot
import pickle
from utils import *

import time

# server sends secrets to client
def ottestb():
    with listen() as s:
        while(True):
            conn, addr = s.accept()
            with conn: 
                print("connected by", addr)
                tmp = gcot.OT_Sender([b'aaaaaaaaaa', b'bbbbbbbbbb'], conn)
                conn.close()

def cgarbltestb():
    STARTFLAG = False
    STARTTIME = 0.0
    ENDTIME = 0.0

    with listen() as s:
        rounds = 0
        correct = 0
        while(rounds < 1000):
            conn, addr = s.accept()
            with conn:
                if(not STARTFLAG):
                    STARTTIME = time.time()
                    STARTFLAG = True
                
                # receive stuff from alice 
                a = conn.recv(256000)
                """
                {
                    "gc": {}
                    "cinfo": {}
                    "inputs": [b'xxx', b'xxx']
                    "rmap": {}
                }
                """
                amsg = pickle.loads(a)
                print("received:\n",amsg)

                # generate b inputs and ask for OT
                b_in_raw = [randint(0,1) for i in range(len(amsg["cinfo"]["b_inputs"]))]
                b_ins = [''] * len(amsg["cinfo"]["b_inputs"])
                conn.sendall(b'ready')
                ci=0
                while(b_ins[ci] == ""):
                    print("attempting ot",ci)
                    res = gcot.OT_Receiver(b_in_raw[ci], conn)
                    if(not res == -1):
                        b_ins[ci] = res
                    print("received secret:", b_ins[ci])
                    ci += 1
                    if(ci < len(b_in_raw)):
                        conn.sendall(b'continue')
                    else:
                        break

                conn.sendall(b'ins-done')
                print("b_ins", b_ins)

                # build inputs and eval circuit
                final_inputs = amsg["inputs"] + b_ins
                gc = amsg["gc"]
                cinfo = amsg["cinfo"]
                rmap = amsg["rmap"]

                eval_result = cgarbl2.gcEval(gc, final_inputs, cinfo, rmap)
                print("RESULT:",eval_result)

                conn.sendall(eval_result.to_bytes((eval_result.bit_length() + 7 ) // 8, 'big'))

                # correctness check
                a_raw_inputs = amsg["raw_ins"]
                b_raw_inputs = b_in_raw
                raw_inputs = a_raw_inputs + b_raw_inputs
                real = (not (a_raw_inputs == b_raw_inputs))
                print("correct:", (real==eval_result))
                if(real == eval_result):
                    correct += 1
                rounds += 1
        ENDTIME = time.time()
        print("ratio:", correct/rounds)
        print("Time Elapsed:", (ENDTIME - STARTTIME))

if(__name__ == "__main__"):
    #ottestb()
    cgarbltestb()
    #singletestb()