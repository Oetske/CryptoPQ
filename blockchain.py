import time
from hash import hash_fct


class Transaction:
    def __init__(self, sender, receiver, amount: float):
        self.sender = sender
        self.receiver = receiver
        self.amount = amount

    def valid_trans(self):
        if self.amount > 0:
            return True
        else:
            return False


class Block:
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp
        self.previous_hash = previous_hash
        self.nonce = nonce
        self.hash = 0

    def hashing(self):
        bloc_format = "{}{}{}{}{}".format(self.index, self.transactions, self.timestamp, self.previous_hash,
                                          self.nonce)
        return hash_fct(bloc_format)
        #hashlib.sha256(bloc_format.encode()).hexdigest()


class Blockchain:
    def __init__(self):
        self.chain = []
        self.create_genesis()
        self.unconfirmed_transactions = []

    @property
    def last_block(self):
        return self.chain[-1]

    def create_genesis(self):
        genesis_block = Block(0, [], time.time(), 0)
        genesis_block.hash = genesis_block.hashing()
        self.chain.append(genesis_block)

    def create_transaction(self, sender, receiver, amount):
        transaction = Transaction(sender, receiver, amount)
        if transaction.valid_trans():
            self.unconfirmed_transactions.append(transaction)
            return transaction, True
        else:
            return None, False

    def add_block(self, new_block):
        self.chain.append(new_block)

    @staticmethod
    def proof_of_work(block, difficulty):
        hash_block = block.hashing()
        while not hash_block[:difficulty] == difficulty * '0':
            block.nonce += 1
            hash_block = block.hashing()
        return hash_block

    def valid_block(self, current_block, previous_block):
        if current_block.index != previous_block.index + 1:
            return False
        if current_block.previous_hash != previous_block.hash:
            return False
        #à regarder avec merkletree

    def mine(self, difficulty):
        last_block = self.last_block
        index = last_block.index + 1
        previous_hash = last_block.hash
        new_block = Block(index, self.unconfirmed_transactions[0], time.time(), previous_hash)
        hash_new_block = self.proof_of_work(new_block, difficulty)
        new_block.hash = hash_new_block
        self.add_block(new_block)
        #valid = self.valid_block(new_block, last_block)
        self.unconfirmed_transactions.pop(0)



if __name__ == "__main__":
    blockchain = Blockchain()
    new_transaction, valid = blockchain.create_transaction('Alice', 'Bob', 100)

    blockchain.mine(2)
    print(blockchain.chain[1].hash, blockchain.chain[1].nonce)



















