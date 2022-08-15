#tkmenus.py
'''Library that holds all the Tkinter GUI menus'''

from cmath import exp
from email.base64mime import header_encode
import pickle
import time
from tkinter.font import Font
from modules.fileHandling import findInFile, displayFile, modifyFile
from tkinter import *
import modules.accountManagement as accountManagement
import webbrowser


#Functions
def firstMenu():
    '''Initial Log in/Sign up menu'''
    global currentEmp
    currentEmp = {} #Resets currentEmp if logged out

    #Window configuration    
    frame = Frame(window, background = primaryColor)
    frame.pack()

    header = Label(frame, text = "Welcome to Eclipse", font = "Comfortaa 24", bg = primaryColor, fg = "#eee")
    header.pack(anchor="center", pady = (48, 0))

    loginButton = Button(frame, text = "Log In", font = "Montserrat", bg = secondaryColor, fg = "#eee", width = 16, relief = "groove", activebackground = primaryColor, activeforeground = "#FF4800", command = lambda:[frame.destroy(), login()])
    loginButton.pack(after = header, pady = (48, 0))
    signupButton = Button(frame, text = "Sign Up", font = "Montserrat", bg = secondaryColor, fg = "#eee", width = 16, relief = "groove", activebackground = primaryColor, activeforeground = "#FF4800", command = lambda:[frame.destroy(), signUp()])
    signupButton.pack(after = loginButton, pady = (8, 0))

    window.mainloop()

#Login Menu
def login():
    '''Employee login menu'''
    global currentEmp

    #Create Frames
    outerFrame = Frame(window, bg = primaryColor)
    outerFrame.pack(expand = True, fill = "both")
    frame = Frame(outerFrame, bg = primaryColor)
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

                outerFrame.destroy()
                frame.destroy()
                mainMenu(currentEmp)

    #Back button
    backButton = Button(outerFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = "#FF4800", fg = "#eee", relief = "flat", borderwidth = 0, command = lambda:[outerFrame.destroy(), frame.destroy(), firstMenu()])
    backButton.pack(before = frame, anchor = "nw")

    #Header
    header = Label(frame, text = "Log In", font = "Comfortaa 24", bg = primaryColor, fg = "#eee")
    header.pack(anchor="center")

    #Email ID:
    emailLabel = Label(frame, bg = primaryColor, fg = "#eee", font = "Montserrat 12", text = "Email ID:")
    emailLabel.pack(after = header, anchor = "w", pady = (8, 0))
    #Email entry
    emailEntry = Entry(frame, bg = secondaryColor, fg = "#eee", width = 48)
    emailEntry.pack(after = emailLabel)

    #Password:
    passwordLabel = Label(frame, bg = primaryColor, fg = "#eee", font = "Montserrat 12", text = "Password:")
    passwordLabel.pack(after = emailEntry, anchor = "w", pady = (8, 0))
    #Password entry
    passwordEntry = Entry(frame, bg = secondaryColor, fg = "#eee", width = 48, show = "•")
    passwordEntry.pack(after = passwordLabel)

    #Login button
    loginButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", text = "Log In", command = validateEntries, relief = "groove", padx = 8, pady = 2)
    loginButton.pack(after = passwordEntry, pady = (12, 0))

    #Error
    errorLabel = Label(frame, bg = primaryColor, fg = "#f00", font = "Montserrat 12")
    errorLabel.pack(before = emailLabel, pady = (8, 0))

#Sign Up menu
def signUp():

    #Create frames
    outerFrame = Frame(window, bg = primaryColor)
    outerFrame.pack(expand = True, fill = "both")
    frame = Frame(outerFrame, bg = primaryColor)
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

            outerFrame.destroy()
            frame.destroy()
            mainMenu()


    #Back button
    backButton = Button(outerFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "flat", borderwidth = 0, command = lambda:[outerFrame.destroy(), frame.destroy(), firstMenu()])
    backButton.pack(before = frame, anchor = "nw")

    #Header
    header = Label(frame, text = "Sign Up", font = "Comfortaa 24", bg = primaryColor, fg = "#eee")
    header.pack(anchor="center")

    #Email ID:
    emailLabel = Label(frame, bg = primaryColor, fg = "#eee", font = "Montserrat 12", text = "Email ID:")
    emailLabel.pack(after = header, anchor = "w", pady = (8, 0))
    #Email entry
    emailEntry = Entry(frame, bg = secondaryColor, fg = "#eee", width = 48)
    emailEntry.pack(after = emailLabel)

    #Password:
    passwordLabel = Label(frame, bg = primaryColor, fg = "#eee", font = "Montserrat 12", text = "Password (Minimum 8 Characters):")
    passwordLabel.pack(after = emailEntry, anchor = "w", pady = (8, 0))
    #Password entry
    passwordEntry = Entry(frame, bg = secondaryColor, fg = "#eee", width = 48, show = "•")
    passwordEntry.pack(after = passwordLabel)

    #Sign Up button
    createButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", text = "Create Account", command = validateEntries, relief = "groove", padx = 8, pady = 2)
    createButton.pack(after = passwordEntry, pady = (12, 0))

    #Error
    errorLabel = Label(frame, bg = primaryColor, fg = "#f00", font = "Montserrat 12")
    errorLabel.pack(before = emailLabel, pady = (8, 0))

#Main menu
def mainMenu(emp):
    global currentEmp
    currentEmp = emp

    role = currentEmp["role"]

    def logout():
        outerFrame.destroy()
        frame.destroy()
        firstMenu()

    #Create frames
    outerFrame = Frame(window, bg = primaryColor)
    outerFrame.pack(expand = True, fill = "both")
    frame = Frame(outerFrame, bg = primaryColor)
    frame.pack()

    #Logged in user
    email = currentEmp["email"]
    loggedIn = Label(outerFrame, text = f"Logged in as {email} ({role})", bg = primaryColor, fg = "#FF4C29", font = "Montserrat 8 bold")
    loggedIn.pack(before = frame, anchor = "ne", side = "top")

    #Header
    header = Label(frame, text = "Main Menu", font = "Comfortaa 24", bg = primaryColor, fg = "#eee")
    header.pack(anchor="center", pady = (32, 0))
    
    #Buttons
    accButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "Account Management")
    accButton.pack(pady = (16, 2))
    ticketButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "Ticket Management")
    ticketButton.pack(pady = 2)
    aboutButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "About")
    aboutButton.pack(pady = 2)
    logoutButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "Log Out", command = logout)
    logoutButton.pack(pady = 2)

    if roleHier.index(role) < 1:  #Below cashier
        ticketButton.configure(state = "disabled")
    if roleHier.index(role) < 2:  #Below manager
        accButton.configure(state = "disabled")

    #Github
    githubButton = Button(outerFrame, image = github, bg = primaryColor, relief = "flat", command = lambda:webbrowser.open_new_tab("https://github.com/rafeesamith"))
    githubButton.pack(anchor = "se", side = "bottom")

    window.mainloop()

#Ticket Management
def ticketManagement(emp):
    global currentEmp
    currentEmp = emp
    #currentEmp = emp

    role = currentEmp["role"]

    #Create frames
    frame = Frame(window, bg = primaryColor)
    frame.pack(anchor = "n", side = "top")
    navFrame = Frame(window, bg = primaryColor)
    navFrame.pack(fill = "x", before = frame, anchor = "n")

    #Logged in user
    email = currentEmp["email"]
    loggedIn = Label(navFrame, text = f"Logged in as {email} ({role})", bg = primaryColor, fg = "#FF4C29", font = "Montserrat 8 bold")
    loggedIn.pack(anchor = "ne", side = "right")
    
    #Back button
    backButton = Button(navFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = "#FF4800", fg = "#eee", relief = "flat", borderwidth = 0, command = lambda:[navFrame.destroy(), frame.destroy(), mainMenu(currentEmp)])
    backButton.pack(anchor = "nw", side = "left")

    #Header
    header = Label(frame, text = "Ticket Management", font = "Comfortaa 24", bg = primaryColor, fg = "#eee")
    header.pack(anchor = "n")
    
    #Buttons
    createButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "Create Ticket")
    createButton.pack(pady = (16, 2))
    refundButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "Refund Ticket")
    refundButton.pack(pady = 2)
    displayButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "Display Tickets")
    displayButton.pack(pady = 2)

    window.mainloop()

#Display Tickets
def displayTickets(emp):

    frame = Frame(window, bg = primaryColor)
    frame.pack(anchor = "n", side = "top")
    navFrame = Frame(frame, bg = primaryColor)
    navFrame.grid(row = 0, column = 0, sticky = "nw")

    #Back button
    backButton = Button(navFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = accentColor, fg = "#eee", relief = "flat", borderwidth = 0, command = lambda:[navFrame.destroy(), frame.destroy(), mainMenu(currentEmp)])
    backButton.pack(anchor = "nw", side = "left")

    #Header
    header = Label(frame, text = "Tickets", font = "Comfortaa 24", bg = primaryColor, fg = "#eee")
    header.grid(row = 1, column = 0, sticky = "nsew")
    header.grid_configure(columnspan = 10)

    ticketList = []

    with open("data/tickets.dat", "rb") as ticketsFile:
        try:
            while True:
                rec = pickle.load(ticketsFile)
                reclist = []
                for v in rec.values():
                    reclist.append(v)
                ticketList.append(reclist)
        except EOFError:
            pass
    
    #Ticket Headers
    headerList = ["User", "Paid", "Time", "Discount", "Time Created"]

    #Next Page button
    nextPageButton = Button(frame, text = "▶", font = "Comfortaa 18", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = accentColor, fg = "#eee", relief = "flat", borderwidth = 0)
    nextPageButton.grid(row = 99, column = 99)

    #Next Page button
    prevPageButton = Button(frame, text = "▶", font = "Comfortaa 18", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = accentColor, fg = "#eee", relief = "flat", borderwidth = 0)
    prevPageButton.grid(row = 99, column = 98)

    for i in range(5):
        headerStr = StringVar()
        headerStr.set(headerList[i])
        Entry(frame, readonlybackground = primaryColor, fg = accentColor, font = "Montserrat 10 bold", state = "readonly", textvariable = headerStr).grid(row = 2, column = i)
    
    def pages(page):
        x = (page*12)
        for i in range(x, x+12):
            entr = Entry(frame, font = "Montserrat 10")
            entr.grid(row = i+3)
            entr.insert(0, i)


    pages(1)
    

    #Ticket Details Loop
    #for i in range(len(ticketList)):
    #    for j in range(5):
    #        
    #        ticketStr = StringVar()
    #        ticketStr.set(ticketList[i][j])
    #        Entry(frame, readonlybackground = secondaryColor, fg = "#eee", font = "Montserrat 10", state = "readonly", textvariable = ticketStr).grid(row = i+2, column = j)
    
    window.geometry("960x480")
    window.mainloop()

#Create Ticket
def createTicket(emp):

    accType = "regular"
    discountDict = {"regular": 1, "vip": 1.05}               #5% discount for VIP

    constUser = ""
    constBal = 0.0
    constTime = 0.0
    

    def validateUser():
        global accType
        global constUser
        with open("data/accounts_user.dat", "rb") as accountsFile:
            userInput = userEntry.get()
            foundUser = findInFile(userInput, accountsFile)
            if foundUser["found"]:
                userCheckLabel.configure(text = "✅", fg = "#0f0")
                updateButton.configure(state = "normal")
                balStr = StringVar()
                balStr.set(foundUser["rec"]["balance"])
                curBalEntry.configure(textvariable = balStr)
                accType = foundUser["rec"]["type"]
                constUser = userInput
            else:
                userCheckLabel.configure(text = "❎", fg = "#f00")
                updateButton.configure(state = "disabled")
                balStr = StringVar()
                balStr.set(0)
                curBalEntry.configure(textvariable = balStr)
                accType = "regular"
                constUser = ""

    def updateBal():
        global accType
        global constBal
        global constTime

        curBal = float(curBalEntry.get())
        paid = float(paidEntry.get())

        newBal = curBal - paid
        
        if newBal >= 0:
            balStr = StringVar()
            timeStr = StringVar()

            balStr.set(newBal)
            newBalEntry.configure(textvariable = balStr)

            timeCount = 0.01*(round(100*(paid*discountDict[accType])))

            timeStr.set(timeCount)       #Multiplies by 100, then rounds, then divides by 100)
            timeEntry.configure(textvariable = timeStr)

            confirmButton.configure(state = "normal")

            constBal = newBal
            constTime = timeCount

        else:
            errorLabel.configure(text = "Insuficient Balance")
            confirmButton.configure(state = "disabled")
    
    def confirm():
        global accType
        global constBal
        global constTime
        global constUser
        discountDict = {"regular": 1, "vip": 1.05}
        discount = discountDict[accType]
        with open("data/accounts_user.dat", "rb+") as accountsFile, open("data/tickets.dat", "ab") as ticketsFile:
            #Time ticket was created
            timeCreated = time.ctime()
            #Ticket record
            ticket = {"user": constUser, "paid": paidEntry.get(), "time bought": f"{constTime} hours", "discount": f"{round((discount-1)*100)}%", "time created": timeCreated}
            pickle.dump(ticket, ticketsFile)
            
            foundUser = findInFile(constUser, accountsFile)
            userRec = foundUser["rec"]
            userRec["balance"] = constBal
            modifyFile(accountsFile, constUser, userRec)

            
                

    frame = Frame(window, bg = primaryColor)
    frame.pack(anchor = "n", side = "top")
    navFrame = Frame(window, bg = primaryColor)
    navFrame.pack(fill = "x", before = frame, anchor = "n")

    #Back button
    backButton = Button(navFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = accentColor, fg = "#eee", relief = "flat", borderwidth = 0, command = lambda:[navFrame.destroy(), frame.destroy(), mainMenu(currentEmp)])
    backButton.pack(anchor = "nw", side = "left")

    header = Label(frame, text = "Create Ticket", font = "Comfortaa 24", bg = primaryColor, fg = "#eee")
    header.pack(pady = (0, 0))

    errorLabel = Label(frame, text = "", bg = primaryColor, fg = accentColor, font = "Montserrat 12")
    errorLabel.pack(pady=4)


    userFrame = Frame(frame, bg = primaryColor)
    userFrame.pack()

    userEntry = Entry(userFrame, bg = secondaryColor, fg = "#eee", font = "Montserrat 8")
    userEntry.insert(0, "Enter user")
    userEntry.pack(side="left", pady=8)

    userCheckButton = Button(userFrame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", text = "Check", font = "Montserrat 8", relief = "groove", width = 7, command = validateUser)
    userCheckButton.pack(side="left", pady=8)

    userCheckLabel = Label(userFrame, bg = primaryColor, fg = "#eee", font = "Montserrat", text = "⭕")
    userCheckLabel.pack(pady=8)


    paidFrame = Frame(frame, bg = primaryColor)
    paidFrame.pack(pady = 8)
    
    paidEntry = Entry(paidFrame, bg = secondaryColor, fg = "#eee", font = "Montserrat 8")
    paidEntry.insert(0, "Enter paid amount")
    paidEntry.pack(side = "left")

    updateButton = Button(paidFrame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", text = "Update", font = "Montserrat 8", relief = "groove", width = 8, state = "disabled", command = updateBal)
    updateButton.pack(side = "left")

    balanceFrame = Frame(frame, bg = primaryColor)
    balanceFrame.pack()

    curBalFrame = Frame(balanceFrame, bg = primaryColor)
    curBalFrame.pack(side = "left")

    curBalLabel = Label(curBalFrame, bg = primaryColor, fg = "#eee", text = "Current", font = "Montserrat 8")
    curBalLabel.pack()

    curBalEntry = Entry(curBalFrame, readonlybackground = secondaryColor, fg = "#eee", font = "Montserrat 8", state = "readonly", justify = "center")
    curBalEntry.pack()

    newBalFrame = Frame(balanceFrame, bg = primaryColor)
    newBalFrame.pack(side = "left")

    newBalLabel = Label(newBalFrame, bg = primaryColor, fg = "#eee", text = "New", font = "Montserrat 8")
    newBalLabel.pack()

    newBalEntry = Entry(newBalFrame, readonlybackground = secondaryColor, fg = "#eee", font = "Montserrat 8", state = "readonly", justify = "center")
    newBalEntry.pack()



    timeFrame = Frame(frame, bg = primaryColor)
    timeFrame.pack(pady = (16, 0))

    timeLabel = Label(timeFrame, bg = primaryColor, fg = "#eee", text = "Time:")
    timeLabel.pack(side = "left")

    timeEntry = Entry(timeFrame, readonlybackground = secondaryColor, fg = "#eee", text = "Time:", state = "readonly")
    timeEntry.pack(side = "left")
    

    confirmButton = Button(timeFrame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", text = "Confirm", font = "Montserrat 8", width = 9, relief = "groove", state = "disabled", command = confirm)
    confirmButton.pack(side = "left")

    #buttonFrame = Frame(frame)
    #buttonFrame.pack()
    #Button(buttonFrame).pack(side = "left")
    #Button(buttonFrame).pack(side = "left")



    window.mainloop()

#def createTicket():
#    '''Create a new ticket'''
#
#    discountDict = {"regular": 1, "vip": 1.05}               #5% discount for VIP
#
#    with open("tickets.dat", "ab+") as ticketsFile, open("accounts_user.dat", "rb+") as accountsFile:
#        user = input("Enter user: ")
#        foundUser = findInFile(user, accountsFile)
#        while not foundUser["found"]:                       #Finds user in account database
#            user = input("User not found. Enter user: ")
#            foundUser = findInFile(user, accountsFile)
#
#        if foundUser["rec"]["balance"] == 0:                #Checks if user has no balance
#            print("User has no balance in their account.")   
#            return         
#        
#        #Paid
#        paid = float(input("Enter amount paid ($1/hr): "))
#        while foundUser["rec"]["balance"] < paid:           #Checks if user has sufficient balance
#            paid = float(input("Insufficient balance, please try again: ")) 
#
#        #Time
#        timeBought = 0.01*(round(100*(paid * discountDict[foundUser["rec"]["type"]])))    #Multiplies by 100, then rounds, then divides by 100
#
#        #Discounts applied
#        discount = discountDict[foundUser["rec"]["type"]]
#
#        #Time ticket was created
#        timeCreated = time.ctime()
#
#        #Ticket record
#        ticket = {"user": user, "paid": paid, "time bought": f"{timeBought} hours", "discount": f"{round((discount-1)*100)}%", "time created": timeCreated}
#
#        foundUser["rec"]["balance"] -= paid                 #Removed paid amount from user's balance
#
#        modifyFile(accountsFile, user, foundUser["rec"])    #Modifies user's information in file
#
#        pickle.dump(ticket, ticketsFile)
#        displayFile(ticketsFile)
#        displayFile(accountsFile)


#Constants
currentEmp = {}
roleHier = ("guest", "cashier", "manager", "admin")    #Role hierarchy
#Colors I'm too lazy to remember
primaryColor = "#282838"
secondaryColor = "#37374d"
accentColor = "#FF4C29"
#Window
window = Tk()
window.configure(bg = primaryColor, padx = 8, pady = 8)
window.geometry("640x360")
window.title("Eclipse")
#
github = PhotoImage(file = r"resources/github.png")
