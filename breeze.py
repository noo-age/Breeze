import hashlib

class Breeze_block:

    def __init__(self, transactions, previous_hash, difficulty):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.difficulty = difficulty
    
    

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

    def generate_block(self,transactions, previous_hash, difficulty):
        nonce, hash = self.proof_of_work(transactions, previous_hash, difficulty)
        block = str(transactions) + "-" + str(previous_hash)+ "-" + str(nonce) + "-" + str(hash)
        print(block)




def main():
    print("Type in which action you want to take: \n")
    print("- Transact\n")
    print("- Create Block\n")
    action = input("Enter: ")
    if action.lower() == "transact":
        print("Transaction complete")
    elif action.lower() == "create block":
        transactions  = input("transactions")
        previous_hash = input("previous_hash")
        difficulty = input("difficulty")
        block = Breeze_block(transactions,previous_hash,difficulty)
        block.generate_block(transactions,previous_hash,difficulty)
    else:
        print("Invalid Input")


if __name__ == "__main__":
    main()

