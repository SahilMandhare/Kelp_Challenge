from pymongo import MongoClient

import sys

client = MongoClient("mongodb://127.0.0.1:27017")
print("Connection Successfull")

db = client["clientDB"]

collection = db["user"]

def create():
    acc = sys.argv[2]
    name = sys.argv[3]

    dictionary = {'accno' : acc, 'name' : name, 'balance' : 0}
    collection.insert_one(dictionary)

    return "Your " + str(acc) + " Account Created\n"

def deposit():
    acc = sys.argv[2]

    bal = collection.find_one({'accno' : acc}, {'_id' : 0, 'accno' : 1})

    if(bal == None):
        return "Wrong Account\n"
    else:
        depBalance = int(sys.argv[3])
        collection.update_one({'accno' : acc}, {'$inc' : {'balance' : depBalance}})
        return "Successfully Deposit\n"

def withdraw():
    acc = sys.argv[2]

    bal = collection.find_one({'accno' : acc}, {'_id' : 0, 'accno' : 1, 'balance' : 1})

    if(bal == None):
        return "Wrong Account\n"
    else:
        withdrawBalance = int(sys.argv[3])
        if(bal.get('balance') >= withdrawBalance):
            collection.update_one({'accno' : acc}, {'$inc' : {'balance' : -withdrawBalance}})
            return "Successfully Withdraw\n"
        else:
            return "High Amount!!\n"

def balance():
    acc = sys.argv[2]
    bal = collection.find_one({'accno' : acc}, {'_id' : 0,'name' : 1, 'balance' : 1})

    return bal.get('name') + " " + str(bal.get('balance'))

def option():
    a = sys.argv[1]
    print(a)

    if(a == 'CREATE'):
        print(create())
    elif(a == 'DEPOSIT'):
        print(deposit())
    elif(a == 'WITHDRAW'):
        print(withdraw())
    elif(a == 'BALANCE'):
        print(balance())
    else:
        print("Wrong Statement!!")

option()
exit()

client.close()