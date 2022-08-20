#tkmenus.py
'''Library that holds all the Tkinter GUI menus'''

import pickle
import time
from tkinter.font import Font
from modules.fileHandling import findInFile, displayFile, modifyFile
from tkinter import *
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
                showError("Please fill out all fields")
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
                #accountManagement.setCurrentEmp(currentEmp)

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
    loginButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", font = "Montserrat 8", text = "Log In", command = validateEntries, relief = "groove", padx = 8, pady = 2)
    loginButton.pack(after = passwordEntry, pady = (12, 0))

    #Error
    errorLabel = Label(frame, bg = primaryColor, fg = accentColor, font = "Montserrat 12")
    errorLabel.pack(before = emailLabel, pady = (8, 0))

#Sign Up menu
def signUp():
    global currentEmp

    #Create frames
    outerFrame = Frame(window, bg = primaryColor)
    outerFrame.pack(expand = True, fill = "both")
    frame = Frame(outerFrame, bg = primaryColor)
    frame.pack()
    
    #Show error function
    def showError(error):
        errorLabel.configure(text = error)

    #Entry checker
    def validateEntries():
        with open(r"data/accounts_emp.dat", "ab+") as accountsFile:
            empno = 0

            email = emailEntry.get()
            password = passwordEntry.get()
            fifEmail = findInFile(email, accountsFile)

            #Empty fields check
            if not email or not password:
                showError("Please fill out all fields") 

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

            rec = {"empno": empno, "email": email, "password": password, "role": 0}
            pickle.dump(rec, accountsFile)
            currentEmp = rec

            outerFrame.destroy()
            frame.destroy()

        mainMenu(currentEmp)

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
    createButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", font = "Montserrat 8", text = "Create Account", command = validateEntries, relief = "groove", padx = 8, pady = 2)
    createButton.pack(after = passwordEntry, pady = (12, 0))

    #Error
    errorLabel = Label(frame, bg = primaryColor, fg = accentColor, font = "Montserrat 12")
    errorLabel.pack(before = emailLabel, pady = (8, 0))

#Main menu
def mainMenu(emp):
    global currentEmp
    currentEmp = emp

    role = roleHier[currentEmp["role"]]

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
    accButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "Account Management", command = lambda: [outerFrame.destroy(), frame.destroy(), accountManagementSelect(currentEmp)])
    accButton.pack(pady = (16, 2))
    ticketButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "Ticket Management", command = lambda: [outerFrame.destroy(), frame.destroy(), ticketManagement(currentEmp)])
    ticketButton.pack(pady = 2)
    aboutButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "About")
    aboutButton.pack(pady = 2)
    logoutButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "Log Out", command = logout)
    logoutButton.pack(pady = 2)

    if roleHier.index(role) < 1:  #Below cashier
        ticketButton.configure(state = "disabled")
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

    role = roleHier[currentEmp["role"]]

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
    createButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "Create Ticket", command = lambda:[navFrame.destroy(), frame.destroy(), createTicket()])
    createButton.pack(pady = (16, 2))

    displayButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "Display Tickets", command = lambda:[navFrame.destroy(), frame.destroy(), displayFile("tickets", header = "Tickets")])
    displayButton.pack(pady = 2)

    window.mainloop()

#Create Ticket
def createTicket():

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
                userCheckLabel.configure(text = "❎", fg = accentColor)
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

            errorLabel.configure(text = "")

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

        #Reset Values
        emptyString = StringVar()
        updateButton.configure(state = "disabled")
        confirmButton.configure(state = "disabled")
        curBalEntry.configure(textvariable = emptyString)
        newBalEntry.configure(textvariable = emptyString)
        timeEntry.configure(textvariable = emptyString)

        #Success Popup
        confirmPopup = Toplevel(window, bg = primaryColor)
        confirmPopup.geometry("240x120")
        popupFrame = Frame(confirmPopup, bg = primaryColor)
        popupFrame.pack()
        Label(popupFrame, text = "Success!", font = "Comfortaa 14", bg = primaryColor, fg = "#eee").pack(pady = 24)
        Button(popupFrame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", text = "OK", font = "Montserrat 8", relief = "groove", width = 3, command = confirmPopup.destroy).pack()

    frame = Frame(window, bg = primaryColor)
    frame.pack(anchor = "n", side = "top")
    navFrame = Frame(window, bg = primaryColor)
    navFrame.pack(fill = "x", before = frame, anchor = "n")

    #Back button
    backButton = Button(navFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = accentColor, fg = "#eee", relief = "flat", borderwidth = 0, command = lambda:[navFrame.destroy(), frame.destroy(), ticketManagement(currentEmp)])
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

    window.mainloop()

currentPage = 0

#Display Tickets
def displayFile(filename, header):

    recNestList = []
    #Accounts Headers
    headerList = []

    types = {0: "Standard", 1: "VIP"}
    roles = {0: "Guest", 1: "Cashier", 2: "Manager", 3: "Admin"}

    with open(f"data/{filename}.dat", "rb") as fobj:
        rec = pickle.load(fobj)
        for k in rec.keys():
            headerList.append(k)
            fobj.seek(0)

        try:
            while True:
                rec = pickle.load(fobj)
                reclist = []
                for k, v in rec.items():
                    if k == "type":
                        reclist.append(types[v])
                    elif k == "role":
                        reclist.append(roles[v])
                    else:
                        reclist.append(v)
                recNestList.append(reclist)
        except EOFError:
            pass

    def pages(page):
        global currentPage
        totalPages = len(recNestList) // 12

        if page == "next" and currentPage < totalPages:
            currentPage += 1
        elif page == "prev" and currentPage > 0:
            currentPage -= 1
        elif page == "refresh":
            currentPage = 0

        x = (currentPage*12)
        for i in range(0, 12):
            for j in range(0, len(headerList)):
                try:
                    ticketStr = StringVar()
                    ticketStr.set(recNestList[i+x][j])
                    entry = Entry(frame, readonlybackground = secondaryColor, fg = "#eee", font = "Montserrat 10", state = "readonly", textvariable = ticketStr)
                    entry.grid(row = i+3, column = j)

                except IndexError:
                    entry.insert(0, "")

    frame = Frame(window, bg = primaryColor)
    frame.pack(anchor = "n", side = "top")
    navFrame = Frame(frame, bg = primaryColor)
    navFrame.grid(row = 0, column = 0, sticky = "nw")

    #Back button
    backButton = Button(navFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = accentColor, fg = "#eee", relief = "flat", borderwidth = 0, command = lambda:[navFrame.destroy(), frame.destroy(), window.geometry("640x360"), mainMenu(currentEmp)])
    backButton.pack(anchor = "nw", side = "left")

    #Header
    header = Label(frame, text = header, font = "Comfortaa 24", bg = primaryColor, fg = "#eee")
    header.grid(row = 1, column = 0, sticky = "nsew")
    header.grid_configure(columnspan = 10)

    pageButtonFrame = Frame(frame, bg = accentColor)
    pageButtonFrame.grid(row = 15, sticky = "e")
    pageButtonFrame.grid_configure(columnspan = 100)

    #Next Page button
    nextPageButton = Button(pageButtonFrame, text = "▶", font = "Comfortaa 14", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = accentColor, fg = "#eee", relief = "flat", borderwidth = 0, command = lambda:[pages("next")])
    nextPageButton.pack(side = "right")

    #Previous Page button
    prevPageButton = Button(pageButtonFrame, text = "◀", font = "Comfortaa 14", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = accentColor, fg = "#eee", relief = "flat", borderwidth = 0, command = lambda:[pages("prev")])
    prevPageButton.pack(side = "right")

    for i in range(len(headerList)):
        headerStr = StringVar()
        headerStr.set(headerList[i])
        Entry(frame, readonlybackground = primaryColor, fg = accentColor, font = "Montserrat 10 bold", state = "readonly", textvariable = headerStr).grid(row = 2, column = i)
        
    pages("refresh")

    window.geometry("960x480")
    window.mainloop()

#Account Management Selection
def accountManagementSelect(emp):
    global currentEmp
    currentEmp = emp

    role = roleHier[currentEmp["role"]]

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
    header = Label(frame, text = "Account Management", font = "Comfortaa 24", bg = primaryColor, fg = "#eee")
    header.pack(anchor = "n")
    
    #Buttons
    userButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "User Accounts", command = lambda:[navFrame.destroy(), frame.destroy(), accountManagement_user(currentEmp)])
    userButton.pack(pady = (16, 2))

    empButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "Employee Accounts", command = lambda:[navFrame.destroy(), frame.destroy(), accountManagement_emp(currentEmp)])
    empButton.pack(pady = 2)

    if roleHier.index(role) < 2:    #Manager
        empButton.configure(state = "disabled")

    window.mainloop()

#Account Management (User)
def accountManagement_user(emp):
    global currentEmp
    currentEmp = emp
  
    #Create frames
    frame = Frame(window, bg = primaryColor)
    frame.pack(anchor = "n", side = "top")
    navFrame = Frame(window, bg = primaryColor)
    navFrame.pack(fill = "x", before = frame, anchor = "n")
    
    #Back button
    backButton = Button(navFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = "#FF4800", fg = "#eee", relief = "flat", borderwidth = 0, command = lambda:[navFrame.destroy(), frame.destroy(), mainMenu(currentEmp)])
    backButton.pack(anchor = "nw", side = "left")

    #Header
    header = Label(frame, text = "Account Management", font = "Comfortaa 24", bg = primaryColor, fg = "#eee")
    header.pack(anchor = "n")
    
        #Buttons
    #Display Users Button
    displayButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = f"Display User Accounts", command = lambda:[navFrame.destroy(), frame.destroy(), displayFile("accounts_user", header = "User Accounts")])
    displayButton.pack(pady = (16, 2))
    #Create User Button
    createButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = f"Create User Accounts", command = lambda:[navFrame.destroy(), frame.destroy(), createAccount_user(currentEmp)])
    createButton.pack(pady = 2)
    #Update User Button
    updateButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = f"Create User Accounts", command = lambda:[navFrame.destroy(), frame.destroy(), updateAccount_user(currentEmp)])
    updateButton.pack(pady = 2)
    

    window.mainloop()

#Account Management (Employee)
def accountManagement_emp(emp):
    global currentEmp
    currentEmp = emp
  
    #Create frames
    frame = Frame(window, bg = primaryColor)
    frame.pack(anchor = "n", side = "top")
    navFrame = Frame(window, bg = primaryColor)
    navFrame.pack(fill = "x", before = frame, anchor = "n")
    
    #Back button
    backButton = Button(navFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = "#FF4800", fg = "#eee", relief = "flat", borderwidth = 0, command = lambda:[navFrame.destroy(), frame.destroy(), mainMenu(currentEmp)])
    backButton.pack(anchor = "nw", side = "left")

    #Header
    header = Label(frame, text = "Account Management", font = "Comfortaa 24", bg = primaryColor, fg = "#eee")
    header.pack(anchor = "n")
    
    #Buttons
    displayButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "Display Employee Accounts", command = lambda:[navFrame.destroy(), frame.destroy(), displayFile("accounts_emp", header = "Employee Accounts")])
    displayButton.pack(pady = (16, 2))

    createButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", relief = "groove", width = 30, font = "Montserrat 10", pady = 4, text = "Create Employee Accounts", command = lambda:[navFrame.destroy(), frame.destroy(), createAccount_emp(currentEmp)])
    createButton.pack(pady = 2)

    window.mainloop()

#Create Account (User)
def createAccount_user(emp):
    
    def userCheckPressed():
        user = userEntry.get()
        with open("data/accounts_user.dat", "rb") as accountsFile:
            foundUser = findInFile(user, accountsFile)

            def proceed():
                userCheckLabel.configure(text = "✅", fg = "#0f0")
                emailEntry.configure(state = "normal")
                emailCheckButton.configure(state = "normal")
                errorLabel.configure(text = "")

            def block():
                userCheckLabel.configure(text = "❎", fg = accentColor)
                emailEntry.configure(state = "readonly")
                emailCheckButton.configure(state = "disabled")
                balEntry.configure(state = "readonly")
                errorLabel.configure(text = "Username Taken")

            if not user:
                errorLabel.configure(text = "Please fill out all fields")
                return

            if not foundUser["found"]:
                proceed()
            else:
                block()

        return user
    
    def emailCheckPressed():
        user = userCheckPressed()
        email = emailEntry.get()

        with open("data/accounts_user.dat", "rb") as accountsFile:
            foundEmail = findInFile(email, accountsFile)

            def proceed():
                emailCheckLabel.configure(text = "✅", fg = "#0f0")
                balEntry.configure(state = "normal")
                errorLabel.configure(text = "")
                confirmButton.configure(state = "normal")
                
            def block():
                emailCheckLabel.configure(text = "❎", fg = accentColor)
                balEntry.configure(state = "readonly")
                errorLabel.configure(text = "Email Taken")
                confirmButton.configure(state = "disabled")


            if not user and email:
                errorLabel.configure(text = "Please fill out all fields")
                return
            elif "@" not in email:
                errorLabel.configure(text = "Invalid Email")
                return
           
            if not foundEmail["found"]:
                proceed()
            else:
                block()

        return email

    def confirmButtonPressed():
        user = userCheckPressed()
        email = emailCheckPressed()
        types = {"standard": 0, "vip": 1}
        type = types[typeVar.get()]
        try:
            bal = float(balEntry.get())
        except ValueError:
            bal = 0.0

        def returnState():
            userCheckLabel.configure(text = "⭕", fg = "#eee")
            emailCheckLabel.configure(text = "⭕", fg = "#eee")
            emailEntry.configure(state = "readonly")
            emailCheckButton.configure(state = "disabled")
            balEntry.configure(state = "readonly")
            errorLabel.configure(text = "")
            confirmButton.configure(state = "disabled")

        if type not in (0, 1):
            errorLabel.configure(text = "Please select a type")
            return

        with open("data/accounts_user.dat", "ab") as accountsFile:
            rec = {"user": user, "email": email, "type": type, "balance": bal}
            pickle.dump(rec, accountsFile)

        #Success Popup
        confirmPopup = Toplevel(window, bg = primaryColor)
        confirmPopup.geometry("240x120")
        popupFrame = Frame(confirmPopup, bg = primaryColor)
        popupFrame.pack()
        Label(popupFrame, text = "Success!", font = "Comfortaa 14", bg = primaryColor, fg = "#eee").pack(pady = 24)
        Button(popupFrame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", text = "OK", font = "Montserrat 8", relief = "groove", width = 3, command = confirmPopup.destroy).pack()

        returnState()

    #Create frames
    frame = Frame(window, bg = primaryColor)
    frame.pack(anchor = "n", side = "top")
    navFrame = Frame(window, bg = primaryColor)
    navFrame.pack(fill = "x", before = frame, anchor = "n")
    
    #Back button
    backButton = Button(navFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = "#FF4800", fg = "#eee", relief = "flat", borderwidth = 0, command = lambda:[navFrame.destroy(), frame.destroy(), mainMenu(currentEmp)])
    backButton.pack(anchor = "nw", side = "left")

    #Header
    header = Label(frame, text = "Create User Account", font = "Comfortaa 24", bg = primaryColor, fg = "#eee")
    header.pack(anchor = "n")

    #Error
    errorLabel = Label(frame, bg = primaryColor, fg = accentColor, font = "Montserrat 12", text = "")
    errorLabel.pack(pady = (8, 0))

    #Username Frame
    userFrame = Frame(frame, bg = primaryColor)
    userFrame.pack()
    #Username Label
    userLabel = Label(userFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 8", text = "Username:")
    userLabel.pack(side = "left", pady=8)
    #Username Entry
    userEntry = Entry(userFrame, bg = secondaryColor, fg = "#eee", font = "Montserrat 8")
    userEntry.pack(side="left", pady=8)
    #Username Check Button
    userCheckButton = Button(userFrame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", text = "Check", font = "Montserrat 8", relief = "groove", width = 7, command = userCheckPressed)
    userCheckButton.pack(side="left", pady=8)
    #Username Check Label
    userCheckLabel = Label(userFrame, bg = primaryColor, fg = "#eee", font = "Montserrat", text = "⭕")
    userCheckLabel.pack(pady=8)
    
    #Email Frame
    emailFrame = Frame(frame, bg = primaryColor)
    emailFrame.pack()
    #Email Label
    emailLabel = Label(emailFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 8", text = "Email:")
    emailLabel.pack(side = "left", pady=8)
    #Email Entry
    emailEntry = Entry(emailFrame, bg = secondaryColor, readonlybackground = secondaryColor, fg = "#eee", font = "Montserrat 8", state = "readonly")
    emailEntry.pack(side="left", pady=8)
    #Email Check Button
    emailCheckButton = Button(emailFrame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", text = "Check", font = "Montserrat 8", relief = "groove", width = 7, state = "disabled", command = emailCheckPressed)
    emailCheckButton.pack(side="left", pady=8)
    #Email Check Label
    emailCheckLabel = Label(emailFrame, bg = primaryColor, fg = "#eee", font = "Montserrat", text = "⭕")
    emailCheckLabel.pack(pady=8)

    #Type Frame
    typeFrame = Frame(frame, bg = primaryColor)
    typeFrame.pack()
    #Type Selectors
    typeVar = StringVar()

    #Standard Type Radio Button
    standardButton = Radiobutton(typeFrame, bg = primaryColor, activebackground = primaryColor, variable = typeVar, value = "standard")
    standardButton.pack(side = "left")
    #Standard Type Label
    standardLabel = Label(typeFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 9", text = "Standard")
    standardLabel.pack(side = "left")
    
    #VIP Type Radio Button
    vipButton = Radiobutton(typeFrame, bg = primaryColor, activebackground = primaryColor, variable = typeVar, value = "vip") 
    vipButton.pack(side = "left")
    #VIP Type Label
    vipLabel = Label(typeFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 9", text = "VIP")
    vipLabel.pack(side = "left")

    #Bal Frame
    balFrame = Frame(frame, bg = primaryColor)
    balFrame.pack()
    #Bal Label
    balLabel = Label(balFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 8", text = "Initial Balance:")
    balLabel.pack(side = "left", pady=8)
    #Bal Entry
    balEntry = Entry(balFrame, bg = secondaryColor, readonlybackground = secondaryColor, fg = "#eee", font = "Montserrat 8", state = "readonly")
    balEntry.pack(side="left", pady=8)

    #Confirm Button
    confirmButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", font = "Montserrat 8",  text = "Create Account", relief = "groove", state = "disabled", padx = 8, pady = 2, command = confirmButtonPressed)
    confirmButton.pack(pady = 4)

    window.mainloop()

#Update Account (User)
def updateAccount_user(emp):
    global currentEmp
    currentEmp = emp
    
    def userCheckPressed():
        user = userEntry.get()

        with open("data/accounts_user.dat", "rb") as accountsFile:
            foundUser = findInFile(user, accountsFile)
            curBal = foundUser["rec"]["balance"]

            def proceed():
                userCheckLabel.configure(text = "✅", fg = "#0f0")
                balEntry.configure(state = "normal")
                curBalLabel.configure(text = f"Current: {curBal}")
                errorLabel.configure(text = "")
                confirmButton.configure(state = "normal")
                
            def block():
                userCheckLabel.configure(text = "❎", fg = accentColor)
                balEntry.configure(state = "readonly")
                errorLabel.configure(text = "User Not Found")
                confirmButton.configure(state = "disabled")

            if not user:
                errorLabel.configure(text = "Please fill out all fields")
                return
        
            if not foundUser["found"]:
                block()
            else:
                proceed()
        
        return user

    def confirmButtonPressed():
        user = userCheckPressed()

        types = {"regular": 0, "vip": 1}
        type = types[typeVar.get()]
        bal = float(balEntry.get())

        def returnState():
            userCheckLabel.configure(text = "⭕", fg = "#eee")
            balEntry.configure(state = "readonly")
            errorLabel.configure(text = "")
            confirmButton.configure(state = "disabled")

        if type not in (0, 1):
            errorLabel.configure(text = "Please select a type")
            return
        if not bal:
            errorLabel.configure(text = "Please enter balance")
            return
        
        with open("data/accounts_user.dat", "rb+") as accountsFile:    

            foundUser = findInFile(user, accountsFile)
            userRec = foundUser["rec"]
            print(userRec)

            userRec["type"] = type
            userRec["balance"] = bal

            print(userRec)
    
            modifyFile(accountsFile, query = user, newRec = userRec)

        #Success Popup
        confirmPopup = Toplevel(window, bg = primaryColor)
        confirmPopup.geometry("240x120")
        popupFrame = Frame(confirmPopup, bg = primaryColor)
        popupFrame.pack()
        Label(popupFrame, text = "Success!", font = "Comfortaa 14", bg = primaryColor, fg = "#eee").pack(pady = 24)
        Button(popupFrame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", text = "OK", font = "Montserrat 8", relief = "groove", width = 3, command = confirmPopup.destroy).pack()

        returnState()
        return

    #Create frames
    frame = Frame(window, bg = primaryColor)
    frame.pack(anchor = "n", side = "top")
    navFrame = Frame(window, bg = primaryColor)
    navFrame.pack(fill = "x", before = frame, anchor = "n")
    
    #Back button
    backButton = Button(navFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = "#FF4800", fg = "#eee", relief = "flat", borderwidth = 0, command = lambda:[navFrame.destroy(), frame.destroy(), mainMenu(currentEmp)])
    backButton.pack(anchor = "nw", side = "left")

    #Header
    header = Label(frame, text = "Update User Account", font = "Comfortaa 24", bg = primaryColor, fg = "#eee")
    header.pack(anchor = "n")

    #Error
    errorLabel = Label(frame, bg = primaryColor, fg = accentColor, font = "Montserrat 12", text = "")
    errorLabel.pack(pady = (8, 0))


    #Username Frame
    userFrame = Frame(frame, bg = primaryColor)
    userFrame.pack()
    #Username Label
    userLabel = Label(userFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 8", text = "Username:")
    userLabel.pack(side = "left", pady=8)
    #Username Entry
    userEntry = Entry(userFrame, bg = secondaryColor, readonlybackground = secondaryColor, fg = "#eee", font = "Montserrat 8")
    userEntry.pack(side="left", pady=8)
    #Username Check Button
    userCheckButton = Button(userFrame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", text = "Check", font = "Montserrat 8", relief = "groove", width = 7, command = userCheckPressed)
    userCheckButton.pack(side="left", pady=8)
    #Username Check Label
    userCheckLabel = Label(userFrame, bg = primaryColor, fg = "#eee", font = "Montserrat", text = "⭕")
    userCheckLabel.pack(pady=8)

    #Type Frame
    typeFrame = Frame(frame, bg = primaryColor)
    typeFrame.pack()
    #Type Selectors
    typeVar = StringVar()

    #Regular Type Radio Button
    regularButton = Radiobutton(typeFrame, bg = primaryColor, activebackground = primaryColor, variable = typeVar, value = "regular")
    regularButton.pack(side = "left")
    #Regular Type Label
    regularLabel = Label(typeFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 9", text = "Regular")
    regularLabel.pack(side = "left")
    
    #VIP Type Radio Button
    vipButton = Radiobutton(typeFrame, bg = primaryColor, activebackground = primaryColor, variable = typeVar, value = "vip") 
    vipButton.pack(side = "left")
    #VIP Type Label
    vipLabel = Label(typeFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 9", text = "VIP")
    vipLabel.pack(side = "left")

    #Bal Frame
    balFrame = Frame(frame, bg = primaryColor)
    balFrame.pack()
    #Bal Label
    balLabel = Label(balFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 8", text = "New Balance:")
    balLabel.pack(side = "left", pady=8)
    #Bal Entry
    balEntry = Entry(balFrame, bg = secondaryColor, readonlybackground = secondaryColor, fg = "#eee", font = "Montserrat 8", state = "readonly")
    balEntry.pack(side="left", pady=8)
    #Current Balance Label
    curBalLabel = Label(balFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 8 italic", text = "Current:")
    curBalLabel.pack(side = "left", pady=8)

    #Confirm Button
    confirmButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", font = "Montserrat 8",  text = "Update Account", relief = "groove", state = "disabled", padx = 8, pady = 2, command = confirmButtonPressed)
    confirmButton.pack(pady = 4)

    window.mainloop()

#Update Account (Employee)
def updateAccount_emp(emp):
    global currentEmp
    currentEmp = emp
    
    def empCheckPressed():
        empIn = empEntry.get()

        if currentEmp["role"] < 3:
            managerButton.configure(state = "disabled")
            adminButton.configure(state = "disabled")

        with open("data/accounts_emp.dat", "rb") as accountsFile:
            foundEmp = findInFile(empIn, accountsFile)

            if foundEmp["rec"]["role"] >= currentEmp["role"]:
                errorLabel.configure(text = "Insufficient Permission")
                return

            def proceed():
                empCheckLabel.configure(text = "✅", fg = "#0f0")
                errorLabel.configure(text = "")
                confirmButton.configure(state = "normal")
                
            def block():
                empCheckLabel.configure(text = "❎", fg = accentColor)
                errorLabel.configure(text = "Employee Not Found")
                confirmButton.configure(state = "disabled")

            if not empIn:
                errorLabel.configure(text = "Please fill out all fields")
                return
        
            if not foundEmp["found"]:
                block()
            else:
                proceed()
        
        return empIn

    def confirmButtonPressed():
        emp = empCheckPressed()

        roles = {"guest": 0, "cashier": 1, "manager": 2, "admin": 3}
        role = roles[roleVar.get()]

        def returnState():
            empCheckLabel.configure(text = "⭕", fg = "#eee")
            errorLabel.configure(text = "")
            confirmButton.configure(state = "disabled")

        if role not in (0, 1):
            errorLabel.configure(text = "Please select a type")
            return
        
        with open("data/accounts_emp.dat", "rb+") as accountsFile:    

            foundEmp = findInFile(emp, accountsFile)
            empRec = foundEmp["rec"]

            empRec["role"] = role
    
            modifyFile(accountsFile, query = emp, newRec = empRec)

        #Success Popup
        confirmPopup = Toplevel(window, bg = primaryColor)
        confirmPopup.geometry("240x120")
        popupFrame = Frame(confirmPopup, bg = primaryColor)
        popupFrame.pack()
        Label(popupFrame, text = "Success!", font = "Comfortaa 14", bg = primaryColor, fg = "#eee").pack(pady = 24)
        Button(popupFrame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", text = "OK", font = "Montserrat 8", relief = "groove", width = 3, command = confirmPopup.destroy).pack()

        returnState()
        return

    #Create frames
    frame = Frame(window, bg = primaryColor)
    frame.pack(anchor = "n", side = "top")
    navFrame = Frame(window, bg = primaryColor)
    navFrame.pack(fill = "x", before = frame, anchor = "n")
    
    #Back button
    backButton = Button(navFrame, text = "◀", font = "Comfortaa 18", height = 0, width = 3, bg = primaryColor, activebackground = secondaryColor, activeforeground = "#FF4800", fg = "#eee", relief = "flat", borderwidth = 0, command = lambda:[navFrame.destroy(), frame.destroy(), mainMenu(currentEmp)])
    backButton.pack(anchor = "nw", side = "left")

    #Header
    header = Label(frame, text = "Update Employee Account", font = "Comfortaa 24", bg = primaryColor, fg = "#eee")
    header.pack(anchor = "n")

    #Error
    errorLabel = Label(frame, bg = primaryColor, fg = accentColor, font = "Montserrat 12", text = "")
    errorLabel.pack(pady = (8, 0))


    #Employee Frame
    empFrame = Frame(frame, bg = primaryColor)
    empFrame.pack()
    #Employee Label
    empLabel = Label(empFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 8", text = "Employee:")
    empLabel.pack(side = "left", pady=8)
    #Employee Entry
    empEntry = Entry(empFrame, bg = secondaryColor, readonlybackground = secondaryColor, fg = "#eee", font = "Montserrat 8")
    empEntry.pack(side="left", pady=8)
    #Employee Check Button
    empCheckButton = Button(empFrame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", text = "Check", font = "Montserrat 8", relief = "groove", width = 7, command = empCheckPressed)
    empCheckButton.pack(side="left", pady=8)
    #Employee Check Label
    empCheckLabel = Label(empFrame, bg = primaryColor, fg = "#eee", font = "Montserrat", text = "⭕")
    empCheckLabel.pack(pady=8)

    #Role Frame
    roleFrame = Frame(frame, bg = primaryColor)
    roleFrame.pack()
    #Role Selectors
    roleVar = StringVar()

    #Guest Type Radio Button
    guestButton = Radiobutton(roleFrame, bg = primaryColor, activebackground = primaryColor, variable = roleVar, value = "guest")
    guestButton.pack(side = "left")
    #Guest Type Label
    guestLabel = Label(roleFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 9", text = "Guest")
    guestLabel.pack(side = "left")
    
    #Cashier Type Radio Button
    cashierButton = Radiobutton(roleFrame, bg = primaryColor, activebackground = primaryColor, variable = roleVar, value = "cashier") 
    cashierButton.pack(side = "left")
    #Cashier Type Label
    cashierLabel = Label(roleFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 9", text = "Cashier")
    cashierLabel.pack(side = "left")

    #Manager Type Radio Button
    managerButton = Radiobutton(roleFrame, bg = primaryColor, activebackground = primaryColor, variable = roleVar, value = "manager")
    managerButton.pack(side = "left")
    #Manager Type Label
    managerLabel = Label(roleFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 9", text = "Manager")
    managerLabel.pack(side = "left")
    
    #Admin Type Radio Button
    adminButton = Radiobutton(roleFrame, bg = primaryColor, activebackground = primaryColor, variable = roleVar, value = "admin") 
    adminButton.pack(side = "left")
    #Admin Type Label
    adminLabel = Label(roleFrame, bg = primaryColor, fg = "#eee", font = "Montserrat 9", text = "Admin")
    adminLabel.pack(side = "left")

    #Confirm Button
    confirmButton = Button(frame, bg = primaryColor, activebackground = secondaryColor, fg = "#eee", activeforeground = "#FF4800", font = "Montserrat 8",  text = "Update Account", relief = "groove", state = "disabled", padx = 8, pady = 2, command = confirmButtonPressed)
    confirmButton.pack(pady = 4)

    window.mainloop()

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
