# MPC/SMC

## Module Intro

This repo contains our implemenation of two protocols in SMC/MPC(Secure Multi-Party Communication).

1. Yao's Garbled Circuit
- Garbled Circuit
    - iLabel: Lable input wires
    - cGarble: Generate garbled circuits
    - gcEval: Evaluate the garbled circuits
- Oblivious Transfer
    - Cyclic Group
    - 1 in 2 OT based on Bellare-Micali protocol
2. GMW
- Secret Sharing
    - n-1 random bits
    - XOR the secret and random bits to get the last bit 
- Oblivious Transfer
    - Expand 1 in 2 OT to 1 in 4 OT
## Usage

Wrapper (to be added)

## Communication Procedure Intro

1. Yao's Garbled Circuit
- Alice sends Bob the circuit, garbled table, and Alice's inputs
- Bob gets his own inputs through OT
- Bob evaluates the circuit and sends back the result

2. GMW
- Alice, Bob and Dealer build socket connect with each other
- Alice and Bob perform Secret Sharing to share their inputs with each other
- 

## Details

Function used to test the protocols: Equality function

Encryption library: Fernet from Python Cryptography


## Reference

- Lecture 10 slides 

- Secure Multiparty Computation and Secret Sharing (https://www.cambridge.org/core/books/secure-multiparty-computation-and-secret-sharing/4C2480B202905CE5370B2609F0C2A67A)

- Yao’s Garbled Circuits: Recent Directions and Implementations (https://www.peteresnyder.com/static/papers/Peter_Snyder_-_Garbled_Circuits_WCP_2_column.pdf)

- Secure multi-party computation (http://people.eecs.berkeley.edu/~sanjamg/classes/cs276-fall14/scribe/lec16.pdf)

- GMW Protocol (https://www.cs.purdue.edu/homes/hmaji/teaching/Fall%202017/lectures/39.pdf)

- APragmatic Introduction to Secure Multi-Party Computation (https://www.cs.virginia.edu/~evans/pragmaticmpc/pragmaticmpc.pdf)

- Financial Cryptographyand Data Security (https://link.springer.com/content/pdf/10.1007%2F978-3-642-39884-1.pdf)

- Cyclic Group (https://github.com/ojroques/garbled-circuit)