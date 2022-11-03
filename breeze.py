import hashlib

class Breeze_block:
    def __init__(self, transactions, previous_hash, difficulty):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.difficulty = difficulty

    def raw_hash(transactions, previous_hash):
        raw = str(transactions) + "-" + str(previous_hash)
        return hashlib.sha256(raw)

    def proof_of_work(transactions, previous_hash, difficulty):
        max_nonce = 2 ** 32
        a = ""
        hash_result = 0
        final_nonce = 0
        for nonce in range(max_nonce):
            hash_result = hashlib.sha256(str(transactions)+"-"+str(previous_hash)+"-"+str(nonce)).hexdigest()

            if str(hash_result)[0,difficulty] == a.zfill(difficulty):
                final_nonce = nonce
                break

        return final_nonce, hash_result

def main():
    return TODO

if __name__ == "__main__":
    main()

