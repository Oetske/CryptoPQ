import falcon
import hashlib
from ecdsa import SigningKey, NIST256p


class Wallet_PQ:
    def __init__(self, n, name, amount=0):
        self.private_key = falcon.SecretKey(n)
        self.public_key = falcon.PublicKey(self.private_key)
        self.adress = self.generate_adress()
        self.name = name
        self.amount = amount

    def generate_adress(self):
        pk_h = self.public_key.h
        pk_h = map(str, pk_h)
        pk_string = ''.join(pk_h)
        s = hashlib.new('sha256', pk_string.encode()).digest()
        r = hashlib.new('ripemd160', s).hexdigest()
        return r

    @staticmethod
    def signature(sk, msg):
        return sk.sign(msg)

    @staticmethod
    def verification(pk, msg, sig):
        return pk.verify(msg, sig)



class Wallet:
    def __init__(self, name, amount=0):
        self.private_key, self.private_key_str = self.generate_sk()
        self.public_key, self.public_key_str = self.generate_pk()
        self.adress = self.generate_adress()
        self.name = name
        self.amount = amount

    def generate_sk(self):
        sk = SigningKey.generate(curve=NIST256p)
        sk_string = sk.to_string()
        return sk, sk_string.hex()

    def generate_pk(self):
        pk = self.private_key.verifying_key
        pk_string = pk.to_string()
        return pk, pk_string.hex()

    def generate_adress(self):
        s = hashlib.new('sha256', self.public_key_str.encode()).digest()
        r = hashlib.new('ripemd160', s).hexdigest()
        return r

    def signature_ecdsa(self, msg):
        return self.private_key.sign(msg)

    @staticmethod
    def verification_ecdsa(pk, msg, sign):
        return pk.verify(sign, msg)










