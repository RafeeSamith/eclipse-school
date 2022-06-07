#fileHandling.py
'''Library that holds some essential file handling functions to make the program efficient'''

import pickle

#Functions

#Check if query exists in file
def findInFile(query, fobj):
    fobj.seek(0)    #Sets pointer to the start of file
    found = 0
    rec = {}        #Need this to scan empty files, since rec will never be defined otherwise
    try:
        while not found:
            rec = pickle.load(fobj)
            if query in rec.values():
                found = 1
    except EOFError:
        pass

    return {"found": found, "rec": rec}     #Returns the found record too if needed for a function

#Display File
def displayFile(fobj):
    try:
        while True:
            print(pickle.load(fobj))
    except EOFError:
        pass
        
