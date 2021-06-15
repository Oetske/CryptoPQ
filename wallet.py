import falcon
import hashlib
from ecdsa import SigningKey


class Wallet_PQ:
    def __init__(self, n, name):
        self.private_key = falcon.SecretKey(n)
        self.public_key = falcon.PublicKey(self.private_key)
        self.adress = self.generate_adress(self.public_key.h)
        self.name = name

    def generate_adress(self, pk):
        str = "".format(pk)
        s = hashlib.new('sha256', str.encode()).digest()
        r = hashlib.new('ripemd160', s).hexdigest()
        return r


class Wallet:
    def __init__(self, name):
        self.private_key, self.private_key_str = self.generate_sk()
        self.public_key = self.generate_pk(self.private_key)
        self.adress = self.generate_adress(self.public_key)
        self.name = name

    def generate_sk(self):
        sk = SigningKey.generate()
        sk_string = sk.to_string()
        return sk, sk_string.hex()

    def generate_pk(self, sk):
        pk = sk.verifying_key
        pk_string = pk.to_string()
        return pk_string.hex()

    def generate_adress(self, pk):
        s = hashlib.new('sha256', pk.encode()).digest()
        r = hashlib.new('ripemd160', s).hexdigest()
        return r


if __name__ == '__main__':
    wallet_alice = Wallet_PQ(64, 'Alice')

    wallet_bob = Wallet('Bob')
    pk = wallet_bob.public_key
    print(pk)

    sk = wallet_bob.private_key_str
    print(sk)

    ad = wallet_bob.adress
    print(ad)









