import hashlib
import random
import math
from math import gcd as bltin_gcd

# '.' separates units of signature
# '_' separates elements of keys
# '-' separates transaction items
# '=' separates block items

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
    p = int(random.randrange(1000000000000000,2000000000000000)) #generate p,q,n
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
    
    public_key = str(n) + "_" + str(e)
    private_key = str(n)+ "_" + str(d)
    print("Public Key: " + public_key)
    print("Private Key: " + private_key)
    return public_key, private_key
    
def convertToNumber (s):
    return int.from_bytes(s.encode('utf-8'), 'little')
def convertFromNumber (n):
    return n.to_bytes(math.ceil(n.bit_length()/8), 'little').decode('utf-8')

#TODO Fix
def encrypt(m, pub_key):
    m = convertToNumber(m) 
    #m = int(m)
    n = int(pub_key.split('_')[0])
    e = int(pub_key.split('_')[1])
    md = pow(m,e,n)
    return md
        
def decrypt(md, priv_key):
    md = int(md)
    n = int(priv_key.split('_')[0])
    d = int(priv_key.split('_')[1])
    m = pow(md,d,n)
    m = convertFromNumber(m)
    return m
def transact(current_coin,pub_key,priv_key):
    message = str(current_coin) + "-" + str(pub_key)
    signature = sign(message,priv_key)
    coin = message + "-" + str(signature)
    return coin
def sign(m,priv_key): #Sign a message using RSA private key
    md = hashlib.sha256(m.encode('utf-8')).hexdigest()
    signature = [0] * 6
    for i in range(6):
        begin = i * 12
        end = (i+1) * 12
        if i == 6:
            end = 64
        signature[i] = encrypt(md[begin:end],priv_key)
    return '.'.join(map(str, signature))
def verify(m,signature,pub_key): #Verify a message using RSA public ke;y
    signature = signature.split('.')
    md = hashlib.sha256(m.encode('utf-8')).hexdigest()
    origin = ""
    for i in range(6):
        origin += decrypt(signature[i],pub_key)
    if md == origin:
        return True
    return False
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
        self.block_data = previous_hash + "=" + transactions + "=" + hex(nonce) + "=" + hash

def verifyKeys(pub_key, priv_key):
    testMessage = "hi12"
    out = encrypt(testMessage,pub_key)
    out = decrypt(out,priv_key)
    return out == testMessage

def main():
    exit = 0
    pub_key = 0
    priv_key = 0
    
    while (1): #login/registration
        print("Type in the number of the action you want to take:")
        print("0 - Exit")
        print("1 - Login")
        print("2 - Register")
        action = input("Enter: ")
        if action == "0":
            return
        elif action == "1":
            pub_key = input("Public Key: ")
            priv_key = input("Private Key: ")
            if not verifyKeys(pub_key,priv_key):
                print("Invalid Login")
                pub_key = 0
                priv_key = 0
            else:
                exit = 1
        elif action == "2":
            pub_key, priv_key = generate_key_pair()
            exit = 1
        if exit:
            break  
    exit = 0
    
    while (1): #account actions   
        print("Type in the number of the action you want to take:")
        print("0 - Exit")
        print("1 - Transact")
        print("2 - Create Block")
        print("3 - Generate key-pair")
        print("4 - Encrypt/decrypt a message")
        print("5 - Sign a Message")
        print("6 - Validate Message")
        action = input("Enter: ")
        if action.lower() == "1":
            current_coin = input("Current Coin: ")
            transact_key = input("Recipient's Public Key: ")
            print("Coin: " + transact(current_coin,transact_key,priv_key))
        elif action.lower() == "0" or exit:
            break
        elif action.lower() == "2":
            transactions_count  = int(input("# of transactions: "))
            transactions = ""
            for i in range(transactions_count):
                transactions += input("transaction " + str(i + 1) + ": ")
                if i != transactions_count-1:
                    transactions += "="
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
                    #rec_key = input("Recipient's Public Key: ")
                    print("Encypted Message: ",encrypt(m,pub_key))
                elif action.lower() == "2":
                    md = input("Encrypted Message: ")
                    #priv_key = input("Private Key: ")
                    print("Message: ",decrypt(md,priv_key))
                elif action.lower() == "0":
                    exit = 1
                    break
                elif action.lower() == "3":
                    break      
        elif action.lower() == "5":
            m = input("Message: ")
            print("Signed Message: " + m + "-" + sign(m,priv_key))
        elif action.lower() == "6":
            m = input("Message: ")
            s = input("Signature: ")
            #TODO Add Public Key Functionality
            if verify(m,s,pub_key):
                print("Valid")
            else:
                print("Invalid")
        else:
            print("Invalid Input")
        if exit:
            break


if __name__ == "__main__":
    main()

