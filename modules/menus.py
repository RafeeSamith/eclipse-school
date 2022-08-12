#menus.py
'''Library that (temporarily) holds all the menus of the program'''

import modules
import pickle
from modules.fileHandling import findInFile
from modules.accountManagement import setCurrentEmp
from modules.ticketManagement import createTicket, displayTickets

#Functions


#First Menu
def firstMenu():
    ch = 0
    while ch != 3:
        try:
            ch = int(input(
                "==============================\n"
                "Login/Sign Up\n"
                "------------------------------\n"
                "1. Log in\n"
                "2. Create new account\n"
                "------------------------------\n"
                "Enter choice: "))
            print("\n")
            
            if ch == 1:
                login()
            elif ch == 2:
                createEmpAccount()
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid input.")
         
#Login Menu
def login():
    global currentEmp

    print(
        "==============================\n"
        "Employee Login\n"
        "------------------------------"
    )

    with open("data/accounts_emp.dat", "rb") as accountsFile:
        email = input("Enter email ID (< to exit): ")
        if email == "<":
            return

        while "@" not in email:         #Check for valid email format
            email = input("Enter valid email ID (< to exit): ")
            if email == "<":
                return

        fif = findInFile(email, accountsFile)
        if not fif["found"]:            #Search for account in file
            ch = input("Account not found, create new? (y/n) ").lower()
            while ch != "y":
                login()                 #Never thought I'd be using recursion, but alas
                return                  #Returns in login come back here, so another return is needed to exit the recursion
            else:
                createEmpAccount()
                return
        else:
            password = input("Enter password (< to exit): ")
            if password == "<":
                return

            while password != fif["rec"]["password"]:   #Check if password matches the one in the rec that belongs to the given email
                password = input(
                    "Invalid password.\n"
                    "Enter password (< to exit):")
                if password == "<":
                    return
            
            currentEmp = fif["rec"]
            modules.accountManagement.setCurrentEmp(currentEmp)
            print(f"Logged in as {currentEmp['email']} ({currentEmp['role']})\n")   #A little messy, the second f-string gets the employee type from the rec value returned by fif

    mainMenu()

#Create Account Menu
#def createEmpAccount():
    with open("data/accounts_emp.dat", "ab+") as empAccountsFile:
        empno = 0

        email = input("Enter email ID (< to exit): ")
        if email == "<":
            return

        while findInFile(email, empAccountsFile)["found"]:    #Check if email already exists
            print("Account already exists")
            email = input("Enter email ID (< to exit): ")
            if email == "<":
                return
            
        password = input("Enter password (Minimum 8 characters) (< to exit): ")
        if password == "<":
            return

        while len(password) < 8:
            print("Password must be at least 8 characters")
            password = input("Enter password (Minimum 8 characters) (< to exit): ")

        try:        
            while findInFile(empno, empAccountsFile)["found"]:
                empno += 1
        except KeyError:    #For an empty file
            pass

        rec = {"empno": empno, "email": email, "password": password, "role": "guest"}
        pickle.dump(rec, empAccountsFile)

#Main Menu
def mainMenu():
    ch = 0  
    while ch != 4:
        ch = int(input(
            "----------------------------\n"
            "1. Account Management\n"
            "2. Ticket Management\n"
            "3. About\n"
            "4. Log Out\n"
            "----------------------------\n"
            "Enter choice: "))

        if ch == 1:
            manageAccountMenu_pre()
        elif ch == 2:
            manageTickets()
        elif ch == 3:
            about()
        else:
            print("Invalid choice")

#About
#def about():
    print("""
    Eclipse
    
    This is a project for a computer lounge management software by me for my school (which will remain unnamed as this is a public repo). 
    
    This program features accounts for employees, customers and a management system for these accounts with necessary privileges """)

#Pre-Account Management Menu
def manageAccountMenu_pre():
    if roleHier.index(currentEmp["role"]) < roleHier.index("manager"):
        print("Access Denied. Only managers and above can access this section.")
        return 

    ch = 0
    while ch != 3:
        ch = int(input(
            "-------------------------\n"
            "1. Employee Accounts\n"
            "2. User Accounts\n"
            "3. Back\n"
            "-------------------------\n"
            "Enter choice: "
        ))

        if ch == 1:
            manageAccountMenu_emp()
        elif ch == 2:
            manageAccountMenu_user()

#Employee Account Management Menu
#def manageAccountMenu_emp():
    ch = 0
    while ch != 5:
        ch = int(input(
            "-------------------------\n"
            "1. Display Accounts\n"
            "2. Search Account\n"
            "3. Change Position\n"
            "4. Delete Account\n"
            "5. Back\n"
            "-------------------------\n"
            "Enter choice: "
        ))

        if ch == 1:
           modules.accountManagement.displayAccounts("emp")
        elif ch == 2:
           modules.accountManagement.searchAccount("emp")
        elif ch == 3:
           modules.accountManagement.modifyAccount("emp")
        elif ch == 4:
           modules.accountManagement.deleteAccount("emp")

#User Account Management Menu
def manageAccountMenu_user():
    ch = 0
    while ch != 6:
        ch = int(input(
            "-------------------------\n"
            "1. Display Accounts\n"
            "2. New Account\n"
            "3. Search Account\n"
            "4. Modify Account\n"
            "5. Delete Account\n"
            "6. Back\n"
            "-------------------------\n"
            "Enter choice: "
        ))
        
        if ch == 1:
           modules.accountManagement.displayAccounts("user")
        elif ch == 2:
           modules.accountManagement.newAccount_user()
        elif ch == 3:
           modules.accountManagement.searchAccount("user")
        elif ch == 4:
           modules.accountManagement.modifyAccount_user("user")
        elif ch == 5:
           modules.accountManagement.deleteAccount("user")

#Ticket Management Menu
#def manageTickets():
    if roleHier.index(currentEmp["role"]) < roleHier.index("cashier"):
        print("Access Denied. Only cashier or higher can access this section.")
        return

    ch = 0
    while ch != 4:
        ch = int(input(
            "1. Create Ticket\n"
            "2. Refund Ticket\n"
            "3. Display Tickets\n"
            "4. Exit\n"
            "Enter choice: "
        )) 
 
        if ch == 1:
            createTicket()
        elif ch == 3:
            displayTickets()

#Constants

roleHier = ("guest", "cashier", "manager", "admin")    #Role hierarchy