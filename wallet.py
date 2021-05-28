from lwe import *


class Wallet:
    def __init__(self):
        self.private_key = LWE.gen_privateKey()
        self.public_key = LWE.gen_publicKey()




