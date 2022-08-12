#accountManagement.py
'''Extension file that holds all the functions for account management, of both employees and users.'''

import pickle
import os
from modules.fileHandling import displayFile, findInFile

#Functions

def setCurrentEmp(emp):
    global currentEmp
    currentEmp = emp

### Universal ###

#Display All Accounts
def displayAccounts(type):
    '''Display all recorded accounts'''

    print("------------------------------\n"
    "Accounts:\n")
    with open(f"data/accounts_{type}.dat", "rb") as accountsFile:
        displayFile(accountsFile)
    print("------------------------------")

#Search Account
def searchAccount(type):
    global currentEmp
    selector = {"emp": "", "user": "username or "}                 #Used this to dynamically change how the function behaves, reusing it for two purposes
    currentSelect = selector[type]

    term = input(f"Enter {currentSelect}email: ").lower()
    with open(f"data/accounts_{type}.dat", "rb") as accountsFile:
        fif = findInFile(term, accountsFile)

        if not fif["found"]:
            print("Account not found.")
        else:
            print(f"Account found, details are given below\n    {fif['rec']}")

#Modify Account
def modifyAccount(type):
    global currentEmp
    selector = {"emp": "empno", "user": "username"}
    currentSelect = selector[type]
    
    with open(f"data/accounts_{type}.dat", "rb+") as accountsFile:
        found = 0
        try:
            if type == "user":
                term = input(f"Enter {currentSelect} or email: ").lower()
                while not found:
                    pos = accountsFile.tell()
                    rec = pickle.load(accountsFile)
                    if rec["user"] == term or rec["email"] == term:
                        found = 1
                
                else:
                    print("Account found, enter new details below", rec)

                    #Type
                    type = input("Enter type (Regular, VIP): ").lower()
                    if type != "vip":
                        type = "regular"

                    #New balance
                    balance += float(input("Enter balance to add: "))
                    

                    accountsFile.seek(pos)
                    rec["type"] = type
                    rec["balance"] = balance
                    pickle.dump(rec, accountsFile)
            else:
                term = input(f"Enter {currentSelect} or email: ").lower()
                while term == currentEmp["email"] or term == str(currentEmp["empno"]):    #Checks if employee is trying to change their own position
                    print("Cannot change your own position.")
                    term = input(f"Enter {currentSelect} or email: ").lower()
                
                else:
                    while not found:
                        pos = accountsFile.tell()
                        rec = pickle.load(accountsFile)
                        if str(rec["empno"]) == term or rec["email"] == term:
                            found = 1
                    else:
                        if roleHier.index(currentEmp["role"]) < roleHier.index(rec["role"]):
                            print("Cannot modify role of higher employee.")
                            return
                        
                        role = input(f"Account found, enter new role below \n{rec}\n")
                        while role not in roleHier: #Makes sure role is valid
                            role = input("Invalid role, enter new role: ")
                        
                        while roleHier.index(role) >= roleHier.index(currentEmp["role"]):    #Makes sure employee isn't allowed to promote someone to their position or higher 
                            print("Cannot promote employee higher than your own position.")
                            role = input("Enter new role: ")

                        accountsFile.seek(pos)
                        rec["role"] = role
                        pickle.dump(rec, accountsFile)
        except EOFError:
                print("Account not found.")

#Delete Account
def deleteAccount(type):
    global currentEmp
    selector = {"emp": "empno", "user": "user"}                 #Used this to dynamically change how the function behaves, reusing it for two purposes
    currentSelect = selector[type]

    term = input(f"Enter {currentSelect} or email: ").lower()

    if type == "emp":
        while term == currentEmp["email"] or term == str(currentEmp["empno"]):
            print("Cannot delete your own account.")
            term = input(f"Enter {currentSelect} or email: ").lower()

    oldAccountsFile = open(f"data/accounts_{type}.dat", "rb")
    newAccountsFile = open("data/temp.dat", "wb")

    found = 0
    try:
        while True:
            rec = pickle.load(oldAccountsFile)
            if rec["email"] != term and str(rec[currentSelect]) != term:
                pickle.dump(rec, newAccountsFile)
            else:
                selectedRec = rec   
                found = 1
    except EOFError:
        oldAccountsFile.close()
        newAccountsFile.close()
        if not found:
            print("Account was not found.")
            os.remove("temp.dat")
        else:
            if type == "emp" and roleHier.index(selectedRec["role"]) > roleHier.index(currentEmp["role"]):
                print("Cannot delete employee account higher than you.")
                return

            confirm = input(f"Account found, confirm delete? (y/n)\n    {selectedRec}\n")
            if confirm != "y":
                os.remove("temp.dat")
            else:
                os.remove(f"accounts_{type}.dat")
                os.rename("temp.dat", f"accounts_{type}.dat")

### Universal End ###

### User ###

#New Account
def newAccount_user():
    with open("data/accounts_user.dat", "ab+") as accountsFile:
        #Username
        user = input("Enter username: ").lower()
        while findInFile(user, accountsFile)["found"]:    #Repeat input until unique
            print("User already exists.")
            user = input("Enter username: ").lower()

        #Email ID
        email = input("Enter email ID: ").lower()
        while findInFile(email, accountsFile)["found"]:    #Repeat input until unique
            print("User already exists.")
            user = input("Enter username: ").lower()

        #Type
        type = input("Enter type (Regular, VIP): ").lower()
        if type != "vip":
            type = "regular"

        #Initial balance
        balance = float(input("Enter initial balance: "))
        while balance < 0:
            balance = float(input("Balance cannot be negative. \nEnter initial balance: "))

        rec = {"user" : user, "email" : email, "type" : type, "balance" : balance}
        pickle.dump(rec, accountsFile)

### User End ###

#Constants
currentEmp = {}
roleHier = ("guest", "cashier", "manager", "admin")    #Role hierarchy