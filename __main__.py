from blockchain import *
from wallet import *
import time


            ## Blockchain PQ ##

print("---- FALCON && Ajtai Hash Function ----\n")

# -- Création de la Blockchain -- #
blockchain = Blockchain()

# -- Création de 2 wallet -- #
start_alice_pq = time.process_time_ns()
wallet_alice = Wallet_PQ(256, 'Alice', 50)
end_alice_pq = time.process_time_ns()
print('FALCON wallet before: ',  wallet_alice.name, wallet_alice.adress, 'Amount: ', wallet_alice.amount, '\n')

start_bob_pq = time.process_time_ns()
wallet_bob = Wallet_PQ(256, 'Bob')
end_bob_pq = time.process_time_ns()
print('FALCON wallet before: ', wallet_bob.name, wallet_bob.adress, 'Amount: ', wallet_bob.amount, '\n')

# -- Création d'une transaction -- #
new_transaction, valid = blockchain.create_transaction(wallet_alice.adress, wallet_bob.adress, 20, wallet_alice.private_key)

# -- Vérification de la transaction ( signature ) et minage -- #
if Wallet_PQ.verification(wallet_alice.public_key, new_transaction.transaction_format.encode(), new_transaction.signature):

    start_pq = time.process_time_ns()
    blockchain.mine(2, 'pq')
    end_pq = time.process_time_ns()
    # --  Time for hash   -- #
    print('Ajtai time: ', (end_pq - start_pq) * 10 ** -9, '\n')

    print('Hash Ajtai: ', blockchain.chain[1].hash, 'Nonce: ', blockchain.chain[1].nonce, '\n')
    wallet_bob.amount += new_transaction.amount
    wallet_alice.amount -= new_transaction.amount
else:
    print('Transaction not verified\n')

print('FALCON wallet after: ', wallet_alice.name, wallet_alice.adress, 'Amount: ', wallet_alice.amount, '\n')
print('FALCON wallet after: ', wallet_bob.name, wallet_bob.adress, 'Amount: ', wallet_bob.amount, '\n')

# --  Time for digital signature -- #
print('FACLON wallet (Alice) genereate key and adress time: ', (end_alice_pq - start_alice_pq) * 10 ** -9, '\n')
print('FACLON wallet (Bob) genereate key and adress time: ', (end_bob_pq - start_bob_pq) * 10 ** -9, '\n')


            ## Blockchain ECDSA ##

print("---- ECDSA && SHA256 ----\n")

# -- Création de 2 wallet -- #
start_alice_ecdsa = time.process_time_ns()
wallet_alice_ecdsa = Wallet('AliceECDSA', 40)
end_alice_ecdsa = time.process_time_ns()
print('ECDSA wallet: ', wallet_alice_ecdsa.name, wallet_alice_ecdsa.adress, 'Amount: ', wallet_alice_ecdsa.amount, '\n')

start_bob_ecdsa = time.process_time_ns()
wallet_bob_ecdsa = Wallet('BobECDSA', 10)
end_bob_ecdsa = time.process_time_ns()
print('ECDSA wallet: ', wallet_bob_ecdsa.name, wallet_bob_ecdsa.adress, 'Amount: ', wallet_bob_ecdsa.amount, '\n')

# -- Création d'une transaction -- #
new_transaction_ecdsa, valid = blockchain.create_transaction(wallet_bob_ecdsa.adress, wallet_alice_ecdsa.adress, 10, wallet_bob_ecdsa.private_key)

# -- Vérification de la transaction ( signature ) et minage -- #
if Wallet.verification_ecdsa(wallet_bob_ecdsa.public_key, new_transaction_ecdsa.transaction_format.encode(), new_transaction_ecdsa.signature):

    start_sha = time.process_time_ns()
    blockchain.mine(2, 'sha')
    end_sha = time.process_time_ns()
    #--  Time for SHA --#
    print('SHA256 time:', (end_sha - start_sha) * 10 ** -9, '\n')


    print('Hahs SHA256: ', blockchain.chain[2].hash, 'Nonce: ', blockchain.chain[2].nonce, '\n')
    wallet_alice_ecdsa.amount += new_transaction_ecdsa.amount
    wallet_alice_ecdsa.amount -= new_transaction_ecdsa.amount
else:
    print('Transaction not verified\n')

print('ECDSA wallet: ', wallet_alice_ecdsa.name, wallet_alice_ecdsa.adress, 'Amount: ',  wallet_alice_ecdsa.amount, '\n')
print('ECDSA wallet: ', wallet_bob_ecdsa.name, wallet_bob_ecdsa.adress, 'Amount: ', wallet_bob_ecdsa.amount, '\n')

# --  Time for digital signature -- #
print('ECDSA wallet (Alice) genereate key and adress time: ', (end_alice_ecdsa - start_alice_ecdsa) * 10 ** -9, '\n')
print('ECDSA wallet (Bob) genereate key and adress time: ', (end_bob_ecdsa - start_bob_ecdsa) * 10 ** -9, '\n')


            ##   Benchmark  ##


def display_blockchain(blockchain):
    l = len(blockchain.chain)
    for i in range(l):
        print(i, ' : ', blockchain.chain[i].hash, '\n')


def display_time_hash(start, end, type, difficulty):
    t = (end - start) * 10 ** -9
    #print(type, ' : ', t, ' seconds with difficulty ', difficulty)
    return t


def test(type):
    test_time = []
    for i in range(4):
        new_transaction_test, valid_test = blockchain.create_transaction(wallet_alice.adress, wallet_bob.adress, 20,
                                                               wallet_alice.private_key)
        Wallet_PQ.verification(wallet_alice.public_key, new_transaction.transaction_format.encode(),
                                  new_transaction_test.signature)

        start = time.process_time_ns()
        blockchain.mine(i, type)
        end = time.process_time_ns()
        if type == 'pq':
            pq_time = display_time_hash(start, end, 'Ajtai', i)
            test_time.append(pq_time)
        elif type == 'sha':
            c_time = display_time_hash(start, end, 'SHA256', i)
            test_time.append(c_time)

    return test_time


def moyenne(a, iter=100):
    for i in range(len(a) - 1):
        result = map(lambda a, b: a + b, a[0], a[1])
        a.remove(a[1])
        a[0] = result
    r = list(result)
    for i in range(len(r)):
        r[i] = r[i] / iter
    return r


print(' -- Benchmark Ajtai && SHA256 -- \n')

# -- Average time for Ajtai -- #
total_pq = []
for i in range(50):
    total_pq.append(test('pq'))

print('Moyenne Ajtai', moyenne(total_pq, 50))

# -- Average time for SHA256 -- #
total_c = []
for i in range(50):
    total_c.append(test('sha'))

print('Moyenne SHA', moyenne(total_c, 50))







