#fileHandling.py
'''Library that holds some essential file handling functions to make the program efficient'''

import pickle

#Functions

#Check if query exists in file
def findInFile(query, fobj):
    '''Looks for a specific term in a file and returns whether it exists, and the record it belongs to'''

    fobj.seek(0)    #Sets pointer to the start of file
    found = 0
    rec = {}        #Need this to scan empty files, since rec will never be defined otherwise
    try:
        while not found:
            pos = fobj.tell()
            rec = pickle.load(fobj)
            if query in rec.values():
                found = 1
    except EOFError:
        pass

    return {"found": found, "rec": rec, "pos": pos}     #Returns the found record too if needed for a function

#Display File
def displayFile(fobj):
    '''Displays all contents of a flie'''

    fobj.seek(0)
    try:
        while True:
            print(pickle.load(fobj))
    except EOFError:
        pass

#Modify File
def modifyFile(fobj, query, newRec):
    '''Modifies a record in a file'''
    
    foundRec = findInFile(query, fobj)
    if foundRec["found"]:
        fobj.seek(foundRec["pos"])
        pickle.dump(newRec, fobj)
    else:
        print("Query not found")