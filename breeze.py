import hashlib

class Breeze_block:
    def __init__(self, transactions, previous_hash):
        self.transactions = transactions
        self.previous_hash = previous_hash

    def raw_hash(transactions, previous_hash):
        raw = transactions + "-" + previous_hash
        return hashlib.sha256(raw)

    def nonce_hash(transactions, previous_hash, zeros_count):
        return TODO

