import yaml
import tkinter as tk
from tkinter import ttk

import tkinter.filedialog as fd
import SSengine

# This program will compare two sets of file lists and copy the difference over to the backup folder
# Will then compare hashes of files which are the same in both lists to see if anything has changed recently
# If difference detected it will move the old version to an obsolete folder and copy the new verison over

# Tkinter GUI initilisation

txtP = 5 #padding for text used in tkinter
frameP = 5 #padding for framing in tkinter
pairH = 100

windowSS = tk.Tk()


windowSS.title("SimplySync")

label = tk.Label(master=windowSS, text = "Welcome to SimpleSync", font=("Times New Roman", 20))
label.pack(padx=txtP,pady=txtP)

framePair = tk.Frame(windowSS, height = pairH, highlightbackground="black", highlightthickness=2)
frameFrom = tk.Frame(framePair, height=pairH/2)
frameTo = tk.Frame(framePair, height=pairH/2)

framePair.pack(fill=tk.X,  ipadx=5, ipady=5, padx=frameP, pady=frameP)
frameFrom.pack(fill=tk.X,  ipadx=5, ipady=5, padx=frameP, pady=frameP)
frameTo.pack(fill=tk.X,  ipadx=5, ipady=5, padx=frameP, pady=frameP)

frameSettings = tk.Frame(windowSS, highlightbackground="black", highlightthickness=2)
frameSettings.pack(fill=tk.X,  ipadx=5, ipady=5, padx=frameP, pady=frameP)

frameSubmit = tk.Frame(windowSS, highlightbackground="black", highlightthickness=2)
frameSubmit.pack(fill=tk.X,  ipadx=5, ipady=5, padx=frameP, pady=frameP)

# Function used to open directory to sync
def findDir(entry):
    location = fd.askdirectory()
    entry.delete(0,tk.END)
    entry.insert(0,location)
    

# Add working folder location(s)
workLocLab = tk.Label(master=frameFrom,text = "Folder location to sync from:")
workLocLab.pack(padx=txtP,pady=txtP, side=tk.LEFT)

chWorkDir1 = tk.Button(frameFrom, text="Choose directory", command=lambda:findDir(workLocText)) # Choose work directory1 to sync FROM
chWorkDir1.pack(padx=txtP,pady=txtP,side = tk.RIGHT)

workLoc = tk.StringVar()
workLoc.set("C:\Projects")
workLocText = tk.Entry(master=frameFrom, textvariable = workLoc, width = 50)
workLocText.pack(padx=txtP,pady=txtP,side = tk.RIGHT)


# Add sync folder location(s)
recLocLab = tk.Label(master=frameTo,text = "Folder location to sync above folder to:") # receiving sync location
recLocLab.pack(padx=txtP,pady=txtP, side=tk.LEFT)

chrecDir1 = tk.Button(frameTo, text="Choose directory", command=lambda:findDir(recLocText)) # Choose rec directory1 to sync TO
chrecDir1.pack(padx=txtP,pady=txtP,side = tk.RIGHT)

recLoc = tk.StringVar()
recLoc.set("N:\Backup\BeastBackup")
recLocText = tk.Entry(master=frameTo, textvariable = recLoc, width = 50) # receiving sync location
recLocText.pack(padx=txtP,pady=txtP,side = tk.RIGHT)


def openJob():
    jobFile = fd.askopenfile(mode='r', title='Open a job file', filetypes=[('yaml', '*.yaml')])
    try:
        data = yaml.safe_load(jobFile)        
        syncFrom = data['SyncJob1']['From']
        syncTo = data['SyncJob1']['To']
        workLocText.delete(0,tk.END)
        workLocText.insert(0,syncFrom)
        recLocText.delete(0,tk.END)
        recLocText.insert(0,syncTo)
             
        
    except yaml.YAMLError as exc:
        print(exc)

# Buttons for Frame Submit to start, stop, open, alter and save jobs and other options

n = tk.StringVar()
fileComp = ttk.Combobox(frameSettings, width = 27, state="readonly", textvariable = n) #<-----------Needs to be activated--------------
fileComp['values'] = ('Binary Compare (Default)', 'Time last edited', 'md5 hashing')
fileComp.current(0)

fileTypeButton = tk.Button(frameSettings, text="File types to compare") #<----------Add seperate window to be opened where file extensions can be added, add choice to allow for date only checking for certain files

addButton = tk.Button(frameSettings, text="Add folder pair")
clearButton = tk.Button(frameSettings, text="Clear folder pairs")

syncButton = tk.Button(frameSubmit, text="Sync Start", command= lambda:SSengine.sync(workLocText.get(), recLocText.get()))
stopButton = tk.Button(frameSubmit, text="Sync Stop")
openButton = tk.Button(frameSubmit, text="Load sync job", command=lambda:openJob())
saveButton = tk.Button(frameSubmit, text="Save sync job")

addButton.pack(padx=txtP,pady=txtP, side=tk.LEFT)
clearButton.pack(padx=txtP,pady=txtP, side=tk.LEFT)

syncButton.pack(padx=txtP,pady=txtP, side=tk.LEFT)
stopButton.pack(padx=txtP,pady=txtP, side=tk.LEFT)
openButton.pack(padx=txtP,pady=txtP, side=tk.LEFT)
saveButton.pack(padx=txtP,pady=txtP, side=tk.LEFT)
fileComp.pack(padx=txtP,pady=txtP, side=tk.LEFT)
fileTypeButton.pack(padx=txtP,pady=txtP, side=tk.LEFT)

#set dir [tk_chooseDirectory %appData% ~ -title "Choose a directory"] #opens up directory choice dialog box

windowSS.mainloop()

#quit() #<--------enable to allow testing of just GUI without running remaining script