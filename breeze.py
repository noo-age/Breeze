import hashlib

class Breeze_block:

    def __init__(self, transactions, previous_hash, difficulty):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.difficulty = difficulty

    def proof_of_work(self,transactions,previous_hash,difficulty):
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

    def generate_block(self,transactions, previous_hash, difficulty):
        nonce, hash = self.proof_of_work(transactions, previous_hash, difficulty)

    def transact():
        current_coin = input("Enter current coin: ")
        public_key = input("Enter the public key of the user you wish to transact to: ")
        private_key = input("Enter your private key: ")





def main():
    print("Type in the number of the action you want to take: \n")
    print("1 - Transact\n")
    print("2 - Create Block\n")
    action = input("Enter: ")
    if action.lower() == "1":
        print("Transaction complete")
    elif action.lower() == "2":
        print("Block Created")
    else:
        print("Invalid Input")


if __name__ == "__main__":
    main()

