import hashlib
import random
import math
from math import gcd as bltin_gcd

'''
'.' separates units of signature
'_' separates elements of keys
'-' separates transaction items
'=' separates block items
'''

# math helper functions
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
  
  
#encoding helper functions
def convertToNumber (s):
    return int.from_bytes(s.encode('utf-8'), 'little')
def convertFromNumber (n):
    return n.to_bytes(math.ceil(n.bit_length()/8), 'little').decode('utf-8')


#RSA implementation
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

def encrypt(m, pub_key): #RSA encrypt
    m = convertToNumber(m) 
    #m = int(m)
    n = int(pub_key.split('_')[0])
    e = int(pub_key.split('_')[1])
    md = pow(m,e,n)
    return md
        
def decrypt(md, priv_key): #RSA decrypt
    md = int(md)
    n = int(priv_key.split('_')[0])
    d = int(priv_key.split('_')[1])
    m = pow(md,d,n)import hashlib
import random
import math
from math import gcd as bltin_gcd

'''
'.' separates units of signature
'_' separates elements of keys
'-' separates transaction items
'=' separates block items
'''

# math helper functions
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
  
  
#encoding helper functions
def convertToNumber (s):
    return int.from_bytes(s.encode('utf-8'), 'little')
def convertFromNumber (n):
    return n.to_bytes(math.ceil(n.bit_length()/8), 'little').decode('utf-8')


#RSA implementation
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

def encrypt(m, pub_key): #RSA encrypt
    m = convertToNumber(m) 
    #m = int(m)
    n = int(pub_key.split('_')[0])
    e = int(pub_key.split('_')[1])
    md = pow(m,e,n)
    return md
        
def decrypt(md, priv_key): #RSA decrypt
    md = int(md)
    n = int(priv_key.split('_')[0])
    d = int(priv_key.split('_')[1])
    m = pow(md,d,n)
    m = convertFromNumber(m)
    return m

def transact(current_coin,pub_key,priv_key): #returns new coin given from priv_key owner to pub_key owner
    message = str(current_coin) + "-" + str(pub_key)
    signature = sign(message,priv_key)
    coin = message + "-" + str(signature)
    return coin

def sign(m,priv_key): #sign a message using RSA private key
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

def proof_of_work(transactions,previous_hash,difficulty): #adds proof-of-work to block
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
    
#class definition
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

    m = convertFromNumber(m)
    return m

def transact(current_coin,pub_key,priv_key): #returns new coin given from priv_key owner to pub_key owner
    message = str(current_coin) + "-" + str(pub_key)
    signature = sign(message,priv_key)
    coin = message + "-" + str(signature)
    return coin

def sign(m,priv_key): #sign a message using RSA private key
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

def proof_of_work(transactions,previous_hash,difficulty): #adds proof-of-work to block
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
    
#class definition
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
