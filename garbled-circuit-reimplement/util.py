from cryptography.fernet import Fernet

def gen_key():
    return Fernet.generate_key()

