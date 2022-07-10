#tkmenus.py
'''Library that holds all the Tkinter GUI menus'''

import pickle
from modules.fileHandling import findInFile
from tkinter import *
import modules.accountManagement as accountManagement

#Functions
def firstMenu():
    '''Initial Log in/Sign up menu'''

    #Window configuration    
    frame = Frame(window, background = bgBlue)
    frame.pack()
    window.title("Welcome to Eclipse")

    header = Label(frame, text = "Welcome to Eclipse", font = "Comfortaa 24", bg = bgBlue, fg = "#eee")
    header.pack(anchor="center", pady = (48, 0))

    loginButton = Button(frame, text = "Log In", font = "Montserrat", bg = bgBlueLight, fg = "#eee", width = 16, relief = "groove", activebackground = bgBlue, activeforeground = "#FF4800", command = lambda:[frame.destroy(), login()])
    loginButton.pack(after = header, pady = (48, 0))
    signupButton = Button(frame, text = "Sign Up", font = "Montserrat", bg = bgBlueLight, fg = "#eee", width = 16, relief = "groove", activebackground = bgBlue, activeforeground = "#FF4800")
    signupButton.pack(after = loginButton, pady = (8, 0))

    window.mainloop()

#Login Menu
def login():
    '''Employee login menu'''
    global currentEmp

    #Window configuration
    window.title("Log In")
    navFrame = Frame(window, bg = bgBlue)
    navFrame.pack(anchor = "nw")
    frame = Frame(window, bg = bgBlue)
    frame.pack()

    def showError(error):
        errorLabel.config(text = error)

    def validateEntries():
        with open(r"data/accounts_emp.dat", "rb") as accountsFile:
            email = emailEntry.get()
            password = passwordEntry.get()
            fifEmail = findInFile(email, accountsFile)
            
            #Checks if fields are blank
            if not email or not password:
                showError("Please fill out the fields")
                return
            elif "@" not in email:
                showError("Invalid Email")
                return
            elif not fifEmail["found"]:
                showError("Email not found")
                return

            if password != fifEmail["rec"]["password"]:
                showError("Invalid Password")
            else:
                currentEmp = fifEmail["rec"]
                accountManagement.setCurrentEmp(currentEmp)
                showError("Logged in")

            
        #    fif = findInFile(email, accountsFile)
        #    if not fif["found"]:            #Search for account in file
        #        ch = input("Account not found, create new? (y/n) ").lower()
        #        while ch != "y":
        #            login()                 #Never thought I'd be using recursion, but alas
        #            return                  #Returns in login come back here, so another return is needed to exit the recursion
        #        else:
        #            createEmpAccount()
        #            return
        #    else:
        #        password = input("Enter password (< to exit): ")
        #        if password == "<":
        #            return
        #
        #        while password != fif["rec"]["password"]:   #Check if password matches the one in the rec that belongs to the given email
        #            password = input(
        #                "Invalid password.\n"
        #                "Enter password (< to exit):")
        #            if password == "<":
        #                return
        #        
        #        currentEmp = fif["rec"]
        #        accountManagement.setCurrentEmp(currentEmp)
        #        print(f"Logged in as {currentEmp['email']} ({currentEmp['role']})\n")   #A little messy, the second f-string gets the employee type from the rec value returned by fif
        #

    #Back button
    backButton = Button(navFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = bgBlue, fg = "#eee", relief = "flat", command = lambda:[frame.destroy(), firstMenu()])
    backButton.pack(anchor = "nw")

    #Header
    header = Label(frame, text = "Log In", font = "Comfortaa 24", bg = bgBlue, fg = "#eee")
    header.pack(anchor="center")

    #Email ID:
    emailLabel = Label(frame, bg = bgBlue, fg = "#eee", font = "Montserrat 12", text = "Email ID:")
    emailLabel.pack(after = header, anchor = "w", pady = (8, 0))
    #Email entry
    emailEntry = Entry(frame, bg = bgBlueLight, fg = "#eee", width = 48)
    emailEntry.pack(after = emailLabel)

    #Password:
    passwordLabel = Label(frame, bg = bgBlue, fg = "#eee", font = "Montserrat 12", text = "Password:")
    passwordLabel.pack(after = emailEntry, anchor = "w", pady = (8, 0))
    #Password entry
    passwordEntry = Entry(frame, bg = bgBlueLight, fg = "#eee", width = 48, show = "•")
    passwordEntry.pack(after = passwordLabel)

    #Login button
    loginButton = Button(frame, bg = bgBlue, activebackground = bgBlueLight, fg = "#eee", activeforeground = bgBlue, text = "Login", command = validateEntries)
    loginButton.pack(after = passwordEntry, pady = (12, 0))

    #Error
    errorLabel = Label(frame, bg = bgBlue, fg = "#f00", font = "Montserrat 12")
    errorLabel.pack(before = emailLabel, pady = (8, 0))

    

#Constants
bgBlue = "#222831"
bgBlueLight = "#2D4059"
window = Tk()
window.configure(bg = bgBlue, padx = 8, pady = 8)
window.geometry("640x360")
bg = PhotoImage(file = r"resources/bg.png")