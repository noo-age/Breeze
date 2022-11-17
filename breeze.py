import hashlib
import random
from math import gcd as bltin_gcd

def coprime(a, b):
    return bltin_gcd(a, b) == 1

def generate_key_pair():
    p = int(random.randrange(1000,2000)) 
    q = p+1
    while 1:
        if coprime(p,q):
            break
        q += 1
    n = p*q
    totient_n = n * (1-1/p) * (1-1/q)
    e = random.randrange(50,100)
    while 1:
        if coprime(n,e):
            break
        e += 1
    d = 0
    k = 1
    while 1:
        d = (k * totient_n+1)/e
        if int(d) == d:
            break
        k += 1
    public_key = str(n) + "-" + str(e)
    private_key = str(n)+ "-" + str(int(d))
    print("Public Key: " + public_key)
    print("Private Key: " + private_key)
    print("Store key-pairs in a safe, easily accessible location. They are your Breeze identity\n")
    
    
#TODO Fix
def encrypt():
    #m = input("Message: ").encode('ASCII')
    m = int.from_bytes(input("Message: ").encode('ASCII'), byteorder='big')
    pub_key = input("Public key: ")
    n = int(pub_key.split('-')[0])
    e = int(pub_key.split('-')[1])
    md = 1
    for i in range(e):
        md = (md * m) % n
    print(md)
        
def decrypt():
    md = int.from_bytes(input("Message: ").encode('ASCII'), byteorder='big')
    priv_key = input("Private key: ")
    n = int(priv_key.split('-')[0])
    d = int(priv_key.split('-')[1])
    m = 1
    for i in range(d):
        m = (m * md) % n
    print(m.decode('ASCII'))
    

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
            hash_result = hashlib.sha256((str(transactions)+"-"+str(previous_hash)+"-"+str(nonce)).encode('utf-8')).hexdigest()
            if (str(hash_result))[0:int(difficulty)] == a.zfill(int(difficulty)):
                final_nonce = nonce
                break
        return final_nonce, hash_result

    def generate_block(self,transactions, previous_hash, difficulty):
        nonce, hash = self.proof_of_work(transactions, previous_hash, difficulty)
        block = str(transactions) + "-" + str(previous_hash)+ "-" + str(nonce) + "-" + str(hash)
        print(block)
    
    def transact():
        current_coin = input("Enter current coin: ")
        public_key = input("Enter the public key of the user you wish to transact to: ")
        private_key = input("Enter your private key: ")

        message = str(current_coin) + "-" + str(public_key)
        md = hashlib.sha256(message).hexdigest()

def main():
    exit = 0
    while (1):
        print("Type in the number of the action you want to take:")
        print("0 - Exit")
        print("1 - Transact")
        print("2 - Create Block")
        print("3 - Generate key-pair")
        print("4 - Encrypt/decrypt a message")
        action = input("Enter: ")
        if action.lower() == "1":
            print("Transaction complete")
        elif action.lower() == "0" or exit:
            break
        elif action.lower() == "2":
            transactions  = input("transactions: ")
            previous_hash = input("previous_hash: ")
            difficulty = input("difficulty: ")
            block = Breeze_block(transactions,previous_hash,difficulty)
            block.generate_block(transactions,previous_hash,difficulty)
        elif action.lower() == "3":
            generate_key_pair()
        elif action.lower() == "4":
            while (1):
                print("Type in the number of the action you want to take:")
                print("0 - Exit")
                print("1 - Encrypt a message")
                print("2 - Decrypt a message")
                print("3 - Back")
                action = input("Enter: ")
                if action.lower() == "1":
                    encrypt()
                elif action.lower() == "2":
                    decrypt()
                elif action.lower() == "0":
                    exit = 1
                    break
                elif action.lower() == "3":
                    break       
        else:
            print("Invalid Input")


if __name__ == "__main__":
    main()

