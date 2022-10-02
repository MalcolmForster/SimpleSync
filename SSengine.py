from genericpath import isfile
import os
import sys
import shutil
import datetime
import hashlib

def sync(dir, bUpDir,compType):

    if(os.path.exists(bUpDir + "\\_OBS\\") == False):
        os.mkdir(bUpDir + "\\_OBS\\")

    #Initally will leave in folder where backup is wanted to end up, making all paths relative.

    toBUp = []
    curBUpFiles = []

    # Creates list of all folders in both directory and backupdirectory


    toBackUpFolders = os.walk(dir)
    theBackUpFolders = os.walk(bUpDir)


    # print(toBackUpFolders.__sizeof__()) 
    # print(theBackUpFolders.__sizeof__()) 

    for folders, childfolders, files in toBackUpFolders:
        toBUp.append(folders.removeprefix(dir))


    for folders, childfolders, files in theBackUpFolders:
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
        print("Moved \"" + file +"\" to _OBS")


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
                foldersChanged = True                
                print("Added \"" + folder +"\" to backup")

        # Will check if all folders backupdirectory has any extra folders and moving them to _OBS folder

        folders2Move = []

        for folder in curBUpFiles:
            #Adding all parent folders to the folder2Move array so program doesnt try to move children afterwards        

            if toBUp.__contains__(folder) == False:
                foldersChanged = True
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
                foldersChanged = True
                shutil.move(bUpDir + "\\" +  parent, bUpDir + "\\_OBS" +  parent)
            except shutil.Error:
                print("Shutil Error with moving folders to _OBS that were deleted")
                #shutilErr(bUpDir + "\\" +  parent, bUpDir + "\\_OBS" +  parent)
        #theBackUpFolders = os.walk(bUpDir)

    #_______________________SECTION TO COPY COMPLETELY NEW FILES OVER________________________________________

    # Could walk through entire file system and compare differences

    toBUp = []
    curBUpFiles = []
    
    # Run md5 hashing on editable files
    def md5sum(file):
        m = hashlib.md5()
        b = bytearray(128*1024)
        mv = memoryview(b)
        with open(file, 'rb', buffering=0) as f:
            while n:=f.readinto(mv):
                m.update(mv[:n])
        return m.hexdigest()

    # Creates list of all folders in both directory and backupdirectory

    toBackUpFolders = os.walk(dir)        
    theBackUpFolders = os.walk(bUpDir)

    for folders in toBackUpFolders:        
        for file in folders[2]:
            if file.__contains__('md5hashMap.txt') == False:
                fileLoc = folders[0] + "\\" + file
                toBUp.append(fileLoc.removeprefix(dir))

    for folders in theBackUpFolders:            
        if folders[0].__contains__("_OBS") == False:            
            for file in folders[2]:
                if file.__contains__('md5hashMap.txt') == False:
                    fileLoc = folders[0] + "\\" + file
                    curBUpFiles.append(fileLoc.removeprefix(bUpDir))

    # print(toBackUpFolders.__sizeof__()) 
    # print(theBackUpFolders.__sizeof__())
    # print(list(set(toBUp) - set(curBUpFiles))) #should probably use this method of finding difference in list sets

    if toBUp == curBUpFiles:
        print("File naming is the same")
    else:
        print("Difference in files detected")
        addToHashTable = False
        # if a file is deleted in working folder move to _OBS
        if compType == 'md5 hashMap' and os.path.exists(bUpDir+"\\md5hashMap.txt"):
            bUpMap = open(bUpDir+"\\md5hashMap.txt",'a')
            addToHashTable = True
        for file in toBUp:
            if curBUpFiles.__contains__(file) == False:            
                shutil.copy(dir + file, bUpDir + file)
                if addToHashTable:
                    curHash = md5sum(dir + file)
                    bUpMap.write(file+"|*|"+curHash+"\n")
                print("Added \"" + file +"\" to backup")

        if addToHashTable:
            bUpMap.close()

        # if addToHashTable and len(curBUpFiles) > 0:
        #     with open(bUpDir+"\\md5hashMap.txt", "r") as f:
        #         lines = f.readlines()
        #     with open(bUpDir+"\\md5hashMap.txt", "w") as f:
        #         for line in lines:
        #             addLine = True
        #             for file in curBUpFiles:
        #                 if toBUp.__contains__(file) == False and line.__contains__(file+"|*|"):
        #                     print("Removed "+ file+" from hashmap")
        #                     addLine = False
        #                     break
        #             if addLine:
        #                 f.write(line)
        # Will check if all folders backupdirectory has any extra folders and moving them to _OBS folder

        # print(list(set(toBUp) - set(curBUpFiles)))

        for file in curBUpFiles:                    
            if toBUp.__contains__(file) == False:
                print(file + " to be moved to obs")
                moveToObs(file)
        theBackUpFolders = os.walk(bUpDir)


    #_______________________SECTION TO CHECK FILES ARE THE SAME AND COPY NEW FILES OVER________________________________________



    toBUp = []
    curBUpFiles = []
    isntEditable = ['.pdf', '.PDF','.epub', '.png', '.jpeg']

    # Creates list of all folders in both directory and backupdirectory
    for folders in os.walk(dir):
        for file in folders[2]:
            if file.__contains__('md5hashMap.txt') == False:
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
                if file.__contains__('md5hashMap.txt') == False:
                    edit = True
                    for ext in isntEditable:               
                        if file.endswith(ext):
                            edit = False
                    if edit == True:
                        fileLoc = folders[0] + "\\" + file
                        curBUpFiles.append(fileLoc.removeprefix(bUpDir))

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
        # Stop immediately when difference is found

    # for i in range(len(curBUpFiles)):

    # print(len(toBUp))
    # print(len(curBUpFiles))

    if toBUp == curBUpFiles:
        toUpdate = []
        #type of compare
        if compType == 'Binary Compare':   

            for i in range(len(toBUp)):
            #if (i <20):
                percentage = str(round((i/len(toBUp)) * 100, 1))                
                if binaryComp(dir+toBUp[i],bUpDir+curBUpFiles[i]):
                    toUpdate.append(toBUp[i])
                print(percentage +"% checked, " + str(len(toUpdate))+ " files to be updated.", end = '    \r')

        elif compType == 'md5 hashing':
            for i in range(len(toBUp)):
                percentage = str(round((i/len(toBUp)) * 100, 1))
                print(percentage +"% checked", end = '    \r')

                toBHash = md5sum(dir + toBUp[i])
                curHash = md5sum(bUpDir + curBUpFiles[i])
                
                if toBHash != curHash:
                    toUpdate.append(toBUp[i])

        elif compType == 'md5 hashMap':
            if os.path.exists(dir+"\\md5hashMap.txt"):
                os.remove(dir+"\\md5hashMap.txt")
            
            toBUpMap = open(dir+"\\md5hashMap.txt",'w')
            for i in range(len(toBUp)):
                percentage = str(round((i/len(toBUp)) * 100, 1))
                print(percentage +"% checked", end = '    \r')
                toBHash = md5sum(dir + toBUp[i])
                toBUpMap.write(toBUp[i]+"|*|"+toBHash+"\n")
            toBUpMap.close()

            if os.path.exists(bUpDir+"\\md5hashMap.txt"):                
                bUpMap = open(bUpDir+"\\md5hashMap.txt")
                content=bUpMap.read()
                bUpMap.close()
            else:                
                bUpMap = open(bUpDir+"\\md5hashMap.txt",'w')
                for i in range(len(toBUp)):
                    percentage = str(round((i/len(toBUp)) * 100, 1))
                    print(percentage +"% checked", end = '    \r')
                    curHash = md5sum(bUpDir + toBUp[i])
                    bUpMap.write(toBUp[i]+"|*|"+curHash+"\n")
                bUpMap.close()

            if binaryComp(dir+"\\md5hashMap.txt",bUpDir+"\\md5hashMap.txt"):
                bUpMapOpen = open(bUpDir+"\\md5hashMap.txt")
                toBUpMapOpen = open(dir+"\\md5hashMap.txt")

                bUpMap = bUpMapOpen.read().split("\n")
                toBUpMap = toBUpMapOpen.read().split("\n")

                bUpMapOpen.close()
                toBUpMapOpen.close()

                for file in toBUpMap:
                    fileFound = False
                    count = 0
                    for bUpFile in bUpMap:
                        if bUpFile == file:
                            fileFound = True
                            count += 1
                            break
                    if fileFound == False:
                        # print(file.split("|*|")[0])
                        toUpdate.append(file.split("|*|")[0])
            else:
                print("Hash Tables are the same")           

        if len(toUpdate) > 0:
            for file in toUpdate:
                #print(file + " to be moved to obs and new version copied")
                moveToObs(file)
                shutil.copy(dir + file, bUpDir + file)
                print("Updated " + file)
            print("All files updated")
            if compType == 'md5 hashMap':
                print("Hashmap copied")
                os.remove(bUpDir+"\\md5hashMap.txt")
                shutil.copy(dir+"\\md5hashMap.txt", bUpDir+"\\md5hashMap.txt")
        else:
            print("No file updates required")
