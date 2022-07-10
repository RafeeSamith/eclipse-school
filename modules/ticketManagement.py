#ticketManagement.py
'''Extension file that holds all the functions for ticket management'''

import pickle
from re import L
from fileHandling import displayFile, findInFile, modifyFile
import time

#Functions

#Creat Ticket
def createTicket():
    '''Create a new ticket'''

    discountDict = {"regular": 1, "vip": 1.05}               #5% discount for VIP

    with open("tickets.dat", "ab+") as ticketsFile, open("accounts_user.dat", "rb+") as accountsFile:
        user = input("Enter user: ")
        foundUser = findInFile(user, accountsFile)
        while not foundUser["found"]:                       #Finds user in account database
            user = input("User not found. Enter user: ")
            foundUser = findInFile(user, accountsFile)

        if foundUser["rec"]["balance"] == 0:                #Checks if user has no balance
            print("User has no balance in their account.")   
            return         
        
        #Paid
        paid = float(input("Enter amount paid ($1/hr): "))
        while foundUser["rec"]["balance"] < paid:           #Checks if user has sufficient balance
            paid = float(input("Insufficient balance, please try again: ")) 

        #Time
        timeBought = 0.01*(round(100*(paid * discountDict[foundUser["rec"]["type"]])))    #Multiplies by 100, then rounds, then divides by 100

        #Discounts applied
        discount = discountDict[foundUser["rec"]["type"]]

        #Time ticket was created
        timeCreated = time.ctime()

        #Ticket record
        ticket = {"user": user, "paid": paid, "time bought": f"{timeBought} hours", "discount": f"{round((discount-1)*100)}%", "time created": timeCreated}

        foundUser["rec"]["balance"] -= paid                 #Removed paid amount from user's balance

        modifyFile(accountsFile, user, foundUser["rec"])    #Modifies user's information in file

        pickle.dump(ticket, ticketsFile)
        displayFile(ticketsFile)
        displayFile(accountsFile)

#Display Tickets
def displayTickets():
    '''Display all recorded tickets'''
    print("------------------------------\n"
    "Tickets:\n")
    with open("tickets.dat", "rb") as ticketsFile:
        displayFile(ticketsFile)
    print("------------------------------")


#Constants