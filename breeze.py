import hashlib
import random
import math
from math import gcd as bltin_gcd

def coprime(a, b):
    return bltin_gcd(a, b) == 1
def isPrime(n):
  if n == 2 or n == 3: return True
  if n < 2 or n%2 == 0: return False
  if n < 9: return True
  if n%3 == 0: return False
  r = int(n**0.5)
  f = 5
  while f <= r:
    if n % f == 0: return False
    if n % (f+2) == 0: return False
    f += 6
  return True
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
        raise Exception('modular inverse does not exist')
    else:
        return x % m
    
def generate_key_pair():
    p = int(random.randrange(1000000,2000000)) #generate p,q,n
    while not isPrime(p):
        p = p +1
    q = p+1
    while not isPrime(q):
        q += 1
    n = p*q
    
    totient_n = (q -1) * (p-1) #calculate totient(n)
    
    e = random.randrange(50,100) #generate e coprime to n
    while not coprime(totient_n,e):
        e += 1
        
    d = modinv(e,totient_n) #calculate modular inverse of e with respect to totient(n)
    
    public_key = str(n) + "-" + str(e)
    private_key = str(n)+ "-" + str(d)
    print("Public Key: " + public_key)
    print("Private Key: " + private_key)
    return public_key, private_key
    
def convertToNumber (s):
    return int.from_bytes(s.encode(), 'big')

def convertFromNumber (n):
    return n.to_bytes(math.ceil(n.bit_length()/8), 'big').decode()

#TODO Fix
def encrypt(m, pub_key):
    m = convertToNumber(m) 
    #m = int(m)
    n = int(pub_key.split('-')[0])
    e = int(pub_key.split('-')[1])
    md = pow(m,e,n)
    return md
        
def decrypt(md, priv_key):
    md = int(md)
    n = int(priv_key.split('-')[0])
    d = int(priv_key.split('-')[1])
    m = pow(md,d,n)
    m = convertFromNumber(m)
    return m

def transact(current_coin,public_key,private_key):
        message = str(current_coin) + "-" + str(public_key)
        md = hashlib.sha256(message.encode('utf-8')).hexdigest()
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


#Todo
def verifyKeys(pub_key, priv_key):
    return True

def main():
    exit = 0
    pub_key = 0
    priv_key = 0
    
    while 1:
        print("Type in the number of the action you want to take:")
        print("0 - Exit")
        print("1 - Login")
        print("2 - Register")
        action = input("Enter: ")
        if action == "0" or exit:
            break
        elif action == "1":
            pub_key = input("Public Key: ")
            priv_key = input("Private Key: ")
            if not verifyKeys(pub_key,priv_key):
                print("Invalid Login")
                pub_key = 0
                priv_key = 0
                break
            exit = 1
        elif action == "2":
            pub_key, priv_key = generate_key_pair()
            exit = 1
        if exit:
            break     
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
            #priv_key = input("Private Key: ")
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
                    rec_key = input("Recipient's Public Key: ")
                    print("Encypted Message: ",encrypt(m,rec_key))
                elif action.lower() == "2":
                    md = input("Encrypted Message: ")
                    #priv_key = input("Private Key: ")
                    print("Message: ",decrypt(md,priv_key))
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

