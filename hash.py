import random
import numpy as np
import binascii
from operator import add

def key(n, m):
    q = n ** 2
    A = np.empty([n, m], dtype=int)

    for i in range(n):
        A[i] = np.random.randint(0, n * m, m) % q

    return A


def fA(A, y, n):
    q = n ** 2
    return (A * y) % q


def hash_fct(msg):
    str_list = list(msg)
    m = len(str_list)
    y = np.empty([m], dtype=int)
    for i in range(m):
        y[i] = ord(str_list[i])
    k = key(64, m)
    hash_int = fA(k, y, 64)
    hash_list = hash_int.tolist()
    for i in range(len(hash_list)):
        hash_list[i] = sum(hash_list[i])
    for i in range(len(hash_list)):
        hash_list[i] = hash_list[i] % 16
        hash_list[i] = hex(hash_list[i]).split('x')[-1]
    hash = ''
    hash = hash + ''.join(hash_list)
    return hash









