import util
from OT import OblivousTransfer as ot

socket_b = util.EvaluatorSocket()
ot_b = ot(socket_b, enabled=True)


def send_evaluation(entry):
    """Evaluate yao circuit for all Bob and Alice's inputs and
    send back the results.

    Args:
        entry: A dict representing the circuit to evaluate.
    """
    circuit, pbits_out = entry["circuit"], entry["pbits_out"]
    garbled_tables = entry["garbled_tables"]
    a_wires = circuit.get("alice", [])  # list of Alice's wires
    b_wires = circuit.get("bob", [])  # list of Bob's wires
    N = len(a_wires) + len(b_wires)
    #print("circuit:", circuit)
    #print("Received:", circuit['id'])

    # Generate all possible inputs for both Alice and Bob
    #for bits in [format(n, 'b').zfill(N) for n in range(2**N)]:
        #bits_b = [int(b) for b in bits[N - len(b_wires):]]  # Bob's inputs

        # Create dict mapping each wire of Bob to Bob's input
    bits_b = input("Bob input (format: 0 0):")
    bits_b = [int(x) for x in bits_b.split()]
    #print("bits_b:", bits_b)
    b_inputs_clear = {
        b_wires[i]: bits_b[i]
        for i in range(len(b_wires))
    }
    #print("b_inputs_clear:", b_inputs_clear, bits_b)

    # Evaluate and send result to Alice
    ot_b.send_result(circuit, garbled_tables, pbits_out,
                        b_inputs_clear)

while True:
    try:
        entry = socket_b.receive()
        socket_b.send(True)
        send_evaluation(entry)
    except KeyboardInterrupt:
        break

