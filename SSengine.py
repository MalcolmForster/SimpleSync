from genericpath import isfile
import os
import sys
import shutil
import datetime
import hashlib

def sync(dir, bUpDir):

    if(os.path.exists(bUpDir + "\\_OBS\\") == False):
        os.mkdir(bUpDir + "\\_OBS\\")

    #Initally will leave in folder where backup is wanted to end up, making all paths relative.

    toBUp = []
    curBUpFiles = []

    # Creates list of all folders in both directory and backupdirectory

    for folders, childfolders, files in os.walk(dir):
        toBUp.append(folders.removeprefix(dir))


    for folders, childfolders, files in os.walk(bUpDir):
        if folders.__contains__("_OBS") == False:
            curBUpFiles.append(folders.removeprefix(bUpDir))

    def dateMethod():
        return datetime.datetime.isoformat(datetime.datetime.now(), timespec= 'hours')

    # If no path in _OBS to desired folder this will make it
    def obsPathChk(originalFilePath):
        if os.path.isfile(bUpDir + originalFilePath):
            originalPath = originalFilePath.replace(os.path.basename(bUpDir + originalFilePath), '')
        else:
            originalPath = originalFilePath

        pathObs = "\\_OBS" + originalPath

        if os.path.exists(pathObs) == False:
            splitPath = pathObs.split('\\')
            splitPath.remove('')

            if os.path.isfile(bUpDir + pathObs):
                splitPath.pop()

            checked = []
            for folder in splitPath:
                checked.append(folder)
                check = bUpDir + "\\" + '\\'.join(checked)
                if os.path.exists(check) == False:
                    print("Making Directory " + check)
                    os.mkdir(check)

    def moveToObs(file):
        obsPathChk(file)
        shutil.move(bUpDir + file, bUpDir + "\\_OBS" + file + dateMethod())
        #print("Moved \"" + file +"\" to _OBS")


    #_______________________SECTION TO REMOVE DELETED FOLDERS__________________________________________

    # Checks if directory structure is the same, not if files are updated:

    if toBUp == curBUpFiles:
        print("Folder Structure is the same")
    else:
        print("Difference in file structure detected")

        # Will check if all folders in directory exist in backupdirectory and copy new ones over

        for folder in toBUp:
            if (curBUpFiles.__contains__(folder) == False):# and folder != "\_OBS"):
                os.mkdir(bUpDir + folder)
                print("Added \"" + folder +"\" to backup")

        # Will check if all folders backupdirectory has any extra folders and moving them to _OBS folder

        folders2Move = []

        for folder in curBUpFiles:
            #Adding all parent folders to the folder2Move array so program doesnt try to move children afterwards        

            if toBUp.__contains__(folder) == False:

                # Add parent folders to the folders2Move array
                parentFound = False
                for parent in folders2Move:                
                    if folder.find(parent) == 0:
                        parentFound = True
                
                if parentFound == False:
                    folders2Move.append(folder)   
                        
                #Adds date to file names
                contents = os.listdir(bUpDir + folder)
                
                for file in contents:
                    fileLoc = bUpDir + folder + "\\" + file
                    
                    # Need to make a way to deal with shutil.Error of folder already existing
                    # if error, find which desitination already exists, try move contents?
                    # this could lead to more errors where contents also contains existing folder

                    if os.path.isfile(fileLoc):
                        shutil.move(fileLoc, fileLoc + dateMethod())

        def shutilErr(wherefrom, whereto):
            try:
                shutil.move
            except shutil.Error:
                shutilErr(wherefrom,whereto)
                
        for parent in folders2Move:
            try:
                shutil.move(bUpDir + "\\" +  parent, bUpDir + "\\_OBS" +  parent)
            except shutil.Error:
                print("Shutil Error with moving folders to _OBS that were deleted")
                #shutilErr(bUpDir + "\\" +  parent, bUpDir + "\\_OBS" +  parent)

    #_______________________SECTION TO COPY COMPLETELY NEW FILES OVER________________________________________

    # Could walk through entire file system and compare differences

    toBUp = []
    curBUpFiles = []

    # Creates list of all folders in both directory and backupdirectory
    for folders in os.walk(dir):
        for file in folders[2]:
            fileLoc = folders[0] + "\\" + file
            toBUp.append(fileLoc.removeprefix(dir))

    for folders in os.walk(bUpDir):
        if folders[0].__contains__("_OBS") == False:
            for file in folders[2]:
                fileLoc = folders[0] + "\\" + file
                curBUpFiles.append(fileLoc.removeprefix(bUpDir))

    if toBUp == curBUpFiles:
        print("File naming is the same")
    else:
        print("Difference in files detected")

        # if a file is deleted in working folder move to _OBS

        for file in toBUp:
            if curBUpFiles.__contains__(file) == False:            
                shutil.copy(dir + file, bUpDir + file)
                print("Added \"" + file +"\" to backup")

        # Will check if all folders backupdirectory has any extra folders and moving them to _OBS folder
        
        for file in curBUpFiles:
            if toBUp.__contains__(file) == False:
                moveToObs(file)  



    #_______________________SECTION TO CHECK FILES ARE THE SAME AND COPY NEW FILES OVER________________________________________



    toBUp = []
    curBUpFiles = []
    isntEditable = ['.pdf', '.PDF','.epub', '.png', '.jpeg']

    # Creates list of all folders in both directory and backupdirectory
    for folders in os.walk(dir):
        for file in folders[2]:
            edit = True
            for ext in isntEditable:
                if file.endswith(ext):
                    edit = False
            if edit == True:
                fileLoc = folders[0] + "\\" + file
                toBUp.append(fileLoc.removeprefix(dir))

    for folders in os.walk(bUpDir):
        if folders[0].__contains__("_OBS") == False:
            for file in folders[2]:
                edit = True
                for ext in isntEditable:               
                    if file.endswith(ext):
                        edit = False
                if edit == True:
                    fileLoc = folders[0] + "\\" + file
                    curBUpFiles.append(fileLoc.removeprefix(bUpDir))


    # Run md5 hashing on editable files
    def md5sum(file):
        m = hashlib.md5()
        b = bytearray(128*1024)
        mv = memoryview(b)
        with open(file, 'rb', buffering=0) as f:
            while n:=f.readinto(mv):
                m.update(mv[:n])
        return m.hexdigest()


    def binaryComp(file1, file2):
        file1Len = len(open(file1,"rb").read())
        file2Len = len(open(file2,"rb").read())
        # print(str(file1Len) +" and " + str(file2Len))

        if(file1Len == file2Len):
        # Compare file length, if same continue, if dif return false
            with open(file1, "rb") as one:
                with open(file2, "rb") as two:
                    chunk = other = True
                    while chunk or other:
                        chunk = one.read(100)
                        other = two.read(100)
                        if chunk != other:
                            return True
                    return False
        else:
            return True
        
        # Compare bytes of files, if same return true, if dif return false
        # Stop immediatly when difference is found
        

    if toBUp == curBUpFiles:        
        toUpdate = []
        #type of compare
        compType = 'binary'
        if compType == 'binary':            
            for i in range(len(toBUp)):
            #if (i <20):
                percentage = str(round((i/len(toBUp)) * 100, 1))
                print(percentage +"% checked", end = '    \r')
                if binaryComp(dir+toBUp[i],bUpDir+curBUpFiles[i]):
                    toUpdate.append(toBUp[i])

        elif compType == 'hash':
            for i in range(len(toBUp)):
                percentage = str(round((i/len(toBUp)) * 100, 1))
                print(percentage +"% checked", end = '    \r')

                toBHash = md5sum(dir + toBUp[i])
                curHash = md5sum(bUpDir + curBUpFiles[i])
                
                if toBHash != curHash:
                    toUpdate.append(toBUp[i])

        if len(toUpdate) > 0:
            for file in toUpdate:
                moveToObs(file)
                shutil.copy(dir + file, bUpDir + file)
                print("Updated " + file)
            print("All files updated")
        else:
            print("No file updates required")
