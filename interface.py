import breeze as b

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
            if not b.verifyKeys(pub_key,priv_key):
                print("Invalid Login")
                pub_key = 0
                priv_key = 0
            else:
                exit = 1
        elif action == "2":
            pub_key, priv_key = b.generate_key_pair()
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
            print("Coin: " + b.transact(current_coin,transact_key,priv_key))
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
            block = b.Breeze_block(transactions,previous_hash,difficulty)
            print(block.block_data)
        elif action.lower() == "3":
            b.generate_key_pair()
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
                    print("Encypted Message: ",b.encrypt(m,pub_key))
                elif action.lower() == "2":
                    md = input("Encrypted Message: ")
                    #priv_key = input("Private Key: ")
                    print("Message: ",b.decrypt(md,priv_key))
                elif action.lower() == "0":
                    exit = 1
                    break
                elif action.lower() == "3":
                    break      
        elif action.lower() == "5":
            m = input("Message: ")
            print("Signed Message: " + m + "-" + b.sign(m,priv_key))
        elif action.lower() == "6":
            m = input("Message: ")
            s = input("Signature: ")

            if b.verify(m,s,pub_key):
                print("Valid")
            else:
                print("Invalid")
        else:
            print("Invalid Input")
        if exit:
            break


if __name__ == "__main__":
    main()
