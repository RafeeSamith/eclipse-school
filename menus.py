#menus.py
'''Library that (temporarily) holds all the menus of the program'''

import pickle
import accountManagement
from fileHandling import findInFile
from accountManagement import setCurrentEmp

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

    with open("accounts_emp.dat", "rb") as accountsFile:
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
            accountManagement.setCurrentEmp(currentEmp)
            print(f"Logged in as {currentEmp['email']} ({currentEmp['role']})\n")   #A little messy, the second f-string gets the employee type from the rec value returned by fif

    mainMenu()

#Create Account Menu
def createEmpAccount():
    with open("accounts_emp.dat", "ab+") as empAccountsFile:
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
    while ch != 5:
        ch = int(input(
            "----------------------------\n"
            "1. Account Management\n"
            "2.\n"
            "3. Log Out\n"
            "----------------------------\n"
            "Enter choice: "))

        if ch == 1:
            manageAccountMenu_pre()
        elif ch == 2:
            pass
        elif ch == 3:
            about()
        else:
            print("Invalid choice")

#About
def about():
    print("""
    Eclipse
    
    This is a project for a computer lounge management software by Rafee for Gulf Indian School. This program z""")

#Pre-Account Management Menu
def manageAccountMenu_pre():
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
def manageAccountMenu_emp():
    if roleHier.index(currentEmp["role"]) < 1:  #Checks if employee's role is below 1 (Manager) in the hierarchy
        print("Access Denied.")
        return
    else:
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
                accountManagement.displayAccounts("emp")
            elif ch == 2:
                accountManagement.searchAccount("emp")
            elif ch == 3:
                accountManagement.modifyAccount("emp")
            elif ch == 4:
                accountManagement.deleteAccount("emp")    #TODO: Make sure employee can't delete their own account

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
            accountManagement.displayAccounts("user")
        elif ch == 2:
            accountManagement.newAccount_user()
        elif ch == 3:
            accountManagement.searchAccount("user")
        elif ch == 4:
            accountManagement.modifyAccount_user("user")
        elif ch == 5:
            accountManagement.deleteAccount("user")

#Constants

roleHier = ("guest", "manager", "admin")    #Role hierarchy