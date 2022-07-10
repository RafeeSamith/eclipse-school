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

    header = Label(frame, text = "Welcome to Eclipse", font = "Comfortaa 24", bg = bgBlue, fg = "#eee")
    header.pack(anchor="center", pady = (48, 0))

    loginButton = Button(frame, text = "Log In", font = "Montserrat", bg = bgBlueLight, fg = "#eee", width = 16, relief = "groove", activebackground = bgBlue, activeforeground = "#FF4800", command = lambda:[frame.destroy(), login()])
    loginButton.pack(after = header, pady = (48, 0))
    signupButton = Button(frame, text = "Sign Up", font = "Montserrat", bg = bgBlueLight, fg = "#eee", width = 16, relief = "groove", activebackground = bgBlue, activeforeground = "#FF4800", command = lambda:[frame.destroy(), signUp()])
    signupButton.pack(after = loginButton, pady = (8, 0))

    window.mainloop()

#Login Menu
def login():
    '''Employee login menu'''
    global currentEmp

    #Create Frames
    navFrame = Frame(window, bg = bgBlue)
    navFrame.pack(anchor = "nw")
    frame = Frame(window, bg = bgBlue)
    frame.pack()

    #Show error function
    def showError(error):
        errorLabel.config(text = error)

    #Entry checker
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

                navFrame.destroy()
                frame.destroy()
                mainMenu()

    #Back button
    backButton = Button(navFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = bgBlue, activebackground = bgBlueLight, activeforeground = "#FF4800", fg = "#eee", relief = "flat", command = lambda:[navFrame.destroy(), frame.destroy(), firstMenu()])
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
    loginButton = Button(frame, bg = bgBlue, activebackground = bgBlueLight, fg = "#eee", activeforeground = "#FF4800", text = "Log In", command = validateEntries, relief = "groove", padx = 8, pady = 2)
    loginButton.pack(after = passwordEntry, pady = (12, 0))

    #Error
    errorLabel = Label(frame, bg = bgBlue, fg = "#f00", font = "Montserrat 12")
    errorLabel.pack(before = emailLabel, pady = (8, 0))

#Sign Up menu
def signUp():

    #Create frames
    navFrame = Frame(window, bg = bgBlue)
    navFrame.pack(anchor = "nw")
    frame = Frame(window, bg = bgBlue)
    frame.pack()
    
    #Show error function
    def showError(error):
        errorLabel.config(text = error)

    #Entry checker
    def validateEntries():
        with open(r"data/accounts_emp.dat", "ab+") as accountsFile:
            empno = 0

            email = emailEntry.get()
            password = passwordEntry.get()
            fifEmail = findInFile(email, accountsFile)

            #Email checks
            if fifEmail["found"]:
                showError("Email already exists")
                return

            #Password checks
            if len(password) < 8:
                showError("Password must be > 8 characters")
                return

            try:
                while findInFile(empno, accountsFile)["found"]:
                    empno += 1
            except KeyError:        #Empty file
                pass

            rec = {"empno": empno, "email": email, "password": password, "role": "guest"}
            pickle.dump(rec, accountsFile)

            navFrame.destroy()
            frame.destroy()
            mainMenu()


    #Back button
    backButton = Button(navFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = bgBlue, activebackground = bgBlueLight, fg = "#eee", activeforeground = "#FF4800", relief = "flat", command = lambda:[navFrame.destroy(), frame.destroy(), firstMenu()])
    backButton.pack(anchor = "nw")

    #Header
    header = Label(frame, text = "Sign Up", font = "Comfortaa 24", bg = bgBlue, fg = "#eee")
    header.pack(anchor="center")

    #Email ID:
    emailLabel = Label(frame, bg = bgBlue, fg = "#eee", font = "Montserrat 12", text = "Email ID:")
    emailLabel.pack(after = header, anchor = "w", pady = (8, 0))
    #Email entry
    emailEntry = Entry(frame, bg = bgBlueLight, fg = "#eee", width = 48)
    emailEntry.pack(after = emailLabel)

    #Password:
    passwordLabel = Label(frame, bg = bgBlue, fg = "#eee", font = "Montserrat 12", text = "Password (Minimum 8 Characters):")
    passwordLabel.pack(after = emailEntry, anchor = "w", pady = (8, 0))
    #Password entry
    passwordEntry = Entry(frame, bg = bgBlueLight, fg = "#eee", width = 48, show = "•")
    passwordEntry.pack(after = passwordLabel)

    #Sign Up button
    createButton = Button(frame, bg = bgBlue, activebackground = bgBlueLight, fg = "#eee", activeforeground = "#FF4800", text = "Create Account", command = validateEntries, relief = "groove", padx = 8, pady = 2)
    createButton.pack(after = passwordEntry, pady = (12, 0))

    #Error
    errorLabel = Label(frame, bg = bgBlue, fg = "#f00", font = "Montserrat 12")
    errorLabel.pack(before = emailLabel, pady = (8, 0))

#Main menu
def mainMenu():

    #Create frames
    navFrame = Frame(window, bg = bgBlue)
    navFrame.pack(anchor = "nw")
    frame = Frame(window, bg = bgBlue)
    frame.pack()

    #Back button
    backButton = Button(navFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = bgBlue, activebackground = bgBlueLight, fg = "#eee", activeforeground = "#FF4800", relief = "flat", command = lambda:[navFrame.destroy(), frame.destroy(), firstMenu()])
    backButton.pack(anchor = "nw")

    #Header
    header = Label(frame, text = "Main Menu", font = "Comfortaa 24", bg = bgBlue, fg = "#eee")
    header.pack(anchor="center")

                #Github
    githubButton = Button(image = github, bg = bgBlue)
    githubButton.pack()





##Main Menu
#def mainMenu():
#    ch = 0  
#    while ch != 4:
#        ch = int(input(
#            "----------------------------\n"
#            "1. Account Management\n"
#            "2. Ticket Management\n"
#            "3. About\n"
#            "4. Log Out\n"
#            "----------------------------\n"
#            "Enter choice: "))
#
#        if ch == 1:
#            manageAccountMenu_pre()
#        elif ch == 2:
#            manageTickets()
#        elif ch == 3:
#            about()
#        else:
#            print("Invalid choice")
#

#Constants
currentEmp = {}
#Colors I'm too lazy to remember
bgBlue = "#222831"
bgBlueLight = "#2D4059"
#Window
window = Tk()
window.configure(bg = bgBlue, padx = 8, pady = 8)
window.geometry("640x360")
window.title("Eclipse")
#
github = PhotoImage(file = r"resources/github.png")