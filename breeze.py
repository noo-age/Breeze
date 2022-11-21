import hashlib
import random
import math
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
    totient_n = (q -1) * (p-1)
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
    
def convertToNumber (s):
    return int.from_bytes(s.encode(), 'big')

def convertFromNumber (n):
    return n.to_bytes(math.ceil(n.bit_length()/8), 'big').decode('latin-1')

#TODO Fix
def encrypt(m, pub_key):
    #m = convertToNumber(input("Message: ")) fix input
    m = int(m)
    n = int(pub_key.split('-')[0])
    e = int(pub_key.split('-')[1])
    md = 1
    for i in range(e):
        md = (md * m) % n
    return md
        
def decrypt(md, priv_key):
    #fix input
    md = int(md)
    n = int(priv_key.split('-')[0])
    d = int(priv_key.split('-')[1])
    m = 1
    for i in range(d):
        m = (m * md) % n
    #print(convertFromNumber(m))
    return m

def transact(current_coin,public_key,private_key):
        message = str(current_coin) + "-" + str(public_key)
        md = hashlib.sha256(message).hexdigest()
        signature = encrypt(md,private_key)
        coin = message + "-" + signature
        return coin
        
def proof_of_work(transactions,previous_hash,difficulty):
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
    
class Breeze_block:        

    def __init__(self, transactions, previous_hash, difficulty):
        self.transactions = transactions
        self.previous_hash = previous_hash
        self.difficulty = difficulty
        
        nonce, hash = proof_of_work(transactions, previous_hash,difficulty)
        self.block_data = previous_hash + "-" + transactions + "-" + hex(nonce) + "-" + hash

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
            current_coin = input("Current Coin: ")
            pub_key = input("Recipient's Public Key: ")
            priv_key = input("Private Key: ")
            print("Coin: " + transact(current_coin,pub_key,priv_key))
        elif action.lower() == "0" or exit:
            break
        elif action.lower() == "2":
            transactions  = input("transactions: ")
            previous_hash = input("previous_hash: ")
            difficulty = input("difficulty: ")
            block = Breeze_block(transactions,previous_hash,difficulty)
            print(block.block_data)
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
                    m = input("Message: ")
                    pub_key = input("Public Key: ")
                    print(encrypt(m,pub_key))
                elif action.lower() == "2":
                    md = input("Encrypted Message: ")
                    priv_key = input("Private Key: ")
                    print(decrypt(md,priv_key))
                elif action.lower() == "0":
                    exit = 1
                    break
                elif action.lower() == "3":
                    break       
        else:
            print("Invalid Input")
        if exit:
            break


if __name__ == "__main__":
    main()

