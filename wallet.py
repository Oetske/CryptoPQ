import numpy as np


class Wallet:
    def __init__(self):
        self.private_key = LWE.gen_privateKey()
        self.public_key = LWE.gen_publicKey()


class LWE:
    def __init__(self, n, m, l, r, q):
        self.n = n
        self.m = m
        self.l = l
        self.r = r
        self.q = q
        self.public_key = self.gen_publicKey()
        self.private_key = self.gen_privateKey()

    def gen_privateKey(self):
        S = np.empty([self.n, self.l], dtype=int)
        for i in range(self.n):
            S[i] = np.random.randint(0, self.n * self.l, self.l) % self.q
        print('S')
        print(S)
        return S

    def gen_publicKey(self):
        A = np.empty([self.m, self.n], dtype=int)
        for i in range(self.m):
            A[i] = np.random.randint(0, self.m * self.n, self.n) % self.q
        print('A')
        print(A)

        E = np.empty([self.m, self.l], dtype=int)
        for i in range(self.m):
            E[i] = np.random.randint(0, self.m * self.l, self.l) % self.q #manque psi

        print('E')
        print(E)

        P = np.dot(A, self.gen_privateKey()) + E
        print('P')
        print(P)

        return A, P

    def gen_alpha(self):
        pass #je sais pas
        #return alpha

    def psi(self):
        z_q = np.arange(self.q)
        sigma = self.gen_alpha() * self.q / np.sqrt(2*np.pi)
        mean = 0
        psi = sigma * np.random.randn(z_q) + mean
        psi = round(psi) % self.q
        return psi

    def gen_u(self):
        u = self.gen_publicKey()[0].T * self.gen_alpha()
        return u

    def gen_v(self):
        v = self.gen_publicKey()[1].T * self.gen_alpha()
        return v


if __name__ == "__main__":
    a = LWE(3 ,4 , 2, 1, 7)
    LWE.gen_privateKey(a)
    LWE.gen_publicKey(a)



