import os
import tkinter as tk
from tkinter import messagebox
from tkinter import filedialog
import subprocess
import sys
import getpass as gp
from hashlib import sha256
######################################
#        [REDACTED] Launcher         #
# By James King (Github: JamesK2754) #
#            MIT Licence             #
######################################

version = "1.0.0"

def encryptpwd(pwd):
    pwd = str(pwd).encode("utf-8")
    for x in range(27):
        pwd = sha256(pwd).hexdigest()
        pwd = str(pwd).encode("utf-8")
    pwd = pwd.decode("utf-8")
    return pwd

if os.path.exists(".secure.txt") == False:
    print("Error, .secure.txt file was not found.")
    messagebox.showerror("Error", "The password storage file could not be found. Redacted Launcher has regenerated that file, please enter the command line terminal to reenter your password.")
    pwd = gp.getpass("Password: ")
    file = open(".secure.txt", "w")
    file.write(encryptpwd(pwd))
    file.close()
if os.path.exists(".secure_2.txt") == False:
    print("Error, .secure_2.txt was not found.")
    messagebox.showerror("Error", "The app location storage file was not found. Redacted launcher has regenerated the file, but the locations could not be loaded.")
    file = open(".secure_2.txt", "w")
    file.write("")
    file.close()

def outerloop():

    passwordfile = open(".secure.txt", "r")
    password = passwordfile.read()
    passwordfile.close()
    #START
    appwide = tk.Tk()
    appwide.title("[REDACTED] Launcher")
    appwide.resizable(False, False)

    def mainrun(sessionpwd):
        listfile = open(".secure_2.txt", "r")
        listfileconts = listfile.read()
        listfileconts = listfileconts.split("\n")
        appwide.title("[REDACTED] Launcher")
        mainscreenshell = tk.Frame(appwide)
        mainscreenshell.pack(fill="both", padx=5, pady=3)
        mainscreenright = tk.Frame(mainscreenshell)
        mainscreenright.pack(fill="both", side="right", padx=5, pady=3)
        mainscreenleft = tk.Frame(mainscreenshell)
        mainscreenleft.pack(fill="both", side="left", padx=5, pady=3)

        itemlist = tk.Listbox(mainscreenright)
        itemlist.grid(row=1, column=4, rowspan=8, columnspan=3)
        for x in range(len(listfileconts)):
            selectedtoinsertolist = listfileconts[x]
            selectedtoinsertolist = selectedtoinsertolist.split("|")
            selectedtoinsertolist = selectedtoinsertolist[0].replace("\"", "")
            itemlist.insert(0, selectedtoinsertolist)

        def openpressed():
            #try:
            selected_app_ = itemlist.get(itemlist.curselection())
            loc = [idx for idx, s in enumerate(listfileconts) if f"{selected_app_}" in s][0]
            selected_app = listfileconts[int(loc)]
            selected_app = selected_app.split("|")
            selected_app = selected_app[1]
            selected_app = selected_app.replace("\"", "")
            if sys.platform == "win32":
                os.startfile(selected_app)
            else:
                opener = "open" if sys.platform == "darwin" else "xdg-open"
                workdir = os.getcwd()
                workdir = workdir.split("/")
                #/{workdir[1]}/{workdir[2]}
                subprocess.call([opener, f"{selected_app}"])
        openbutt = tk.Button(mainscreenleft, text="Open", command=openpressed)
        openbutt.grid(row=1, column=1, rowspan=1, columnspan=2)

        def addpressed():
            pwdpop = tk.Tk()
            popframe = tk.Frame(pwdpop)
            pwdpop.title("[REDACTED] Launcher - Add application")
            popframe.pack(fill="both")
            appnametitle = tk.Label(popframe, text="Application name: ")
            locationname = tk.Label(popframe, text="Location: ")
            appnametitle.grid(row=1, column=1)
            locationname.grid(row=2, column=1)
            appnameentry = tk.Entry(popframe)
            def selectapplocation():
                locationentry = filedialog.askopenfilename(title="Select app location", initialdir="/", filetypes=[("All Files", "*.*")])
                locationholdlist = locationentry.split("/")
                locationhold = f".{locationholdlist[-1]}"
                locationholdlist.pop(-1)
                locationholdlist.append(locationhold)
                hiddenloc = ""
                for i in locationholdlist:
                    hiddenloc += str(i) + "/"
                os.rename(locationentry, hiddenloc)
                listfile = open(".secure_2.txt", "a+")
                appname = appnameentry.get()
                listfile.write(f"\n\"{appname}\"|\"{hiddenloc}\"")
                listfile.close()
                messagebox.showwarning("Heads up!", "The app will restart in order to refresh the app list.")
                pwdpop.destroy()
                appwide.destroy()
                outerloop()
            appnameentry.grid(row=1, column=2)
            locationentrybutton = tk.Button(popframe, text="Select app and save", command=selectapplocation)
            locationentrybutton.grid(row=2, column=2)
        addbutt = tk.Button(mainscreenleft, text="Add", command=addpressed)
        addbutt.grid(row=2, column=1, rowspan=1, columnspan=2)

        def deletepressed():
            selected_app_ = itemlist.get(itemlist.curselection())
            file = open(".secure_2.txt", "r")
            fileconts = file.read()
            file.close()
            fileconts = fileconts.split("\n")
            fileconts = list(filter(None, fileconts))
            loc = [idx for idx, s in enumerate(fileconts) if f"{selected_app_}" in s][0]
            #locinconts = fileconts.index(selected_app)
            fileconts.pop(loc)
            newfileconts = ""
            for i in fileconts:
                newfileconts += str(i) + "\n"
            file = open(".secure_2.txt", "w")
            file.write(newfileconts)
            file.close()
            messagebox.showwarning("Heads up!", "The app you requested was deleted from the list and storage file. [R]L will now restart in order to refresh the list.")
            appwide.destroy()
            outerloop()
        delbutt = tk.Button(mainscreenleft, text="Delete", command=deletepressed)
        delbutt.grid(row=3, column=1, rowspan=1, columnspan=2)

        def chngpwdpress():
            pwdpop = tk.Tk()
            pwdpop.title("[REDACTED] Launcher - Change launcher password")
            popframe = tk.Frame(pwdpop)
            popframe.pack(fill="both")
            orgpasstitle = tk.Label(popframe, text="Original password: ")
            newpass1title = tk.Label(popframe, text="New password: ")
            newpass2title = tk.Label(popframe, text="New password again: ")
            orgpass = tk.Entry(popframe)
            newpass1 = tk.Entry(popframe)
            newpass2 = tk.Entry(popframe)
            def enterpasschange():
                if encryptpwd(orgpass.get()) == password:
                    if newpass1.get() == newpass2.get():
                        newpassword = newpass1.get()
                        passwordfile = open(".secure.txt", "w")
                        newpassword = encryptpwd(newpassword)
                        passwordfile.write(newpassword)
                        passwordfile.close()
                        print("password changed")
                        pwdpop.destroy()
                        messagebox.showwarning("Alert", "Software will now close to update password cache.")
                        appwide.destroy()
                        outerloop()
                    else:
                        messagebox.showerror("Error", "The new passwords enter do not match.")
                else:
                    messagebox.showerror("Error", "The original password entered is invalid, please check it and try again.")
            enterbutt = tk.Button(popframe, text="Confirm", command=enterpasschange)
            def changepasswordcancel():
                pwdpop.destroy()
            cancbuttpwd = tk.Button(popframe, text="Cancel", command=changepasswordcancel)
            orgpass.grid(row=1, column=2, rowspan=1, columnspan=2)
            newpass1.grid(row=2,column=2, rowspan=1, columnspan=2)
            enterbutt.grid(row=4, column=2)
            cancbuttpwd.grid(row=4, column=1)
            newpass2.grid(row=3, column=2, rowspan=1, columnspan=2)
            orgpasstitle.grid(row=1, column=1)
            newpass1title.grid(row=2, column=1)
            newpass2title.grid(row=3, column=1)
        chngepwdbutt = tk.Button(mainscreenleft, text="Change password", command=chngpwdpress)
        chngepwdbutt.grid(row=4, column=1, rowspan=1, columnspan=2)

        def aboutpressed():
            aboutwin = tk.Tk()
            aboutwin.resizable(False, False)
            aboutwin.title("[REDACTED] Launcher - About")
            aboutshell = tk.Frame(aboutwin)
            aboutshell.pack(fill="both")
            aboutrightframe = tk.Frame(aboutshell)
            aboutleftframe = tk.Frame(aboutshell)
            aboutrightframe.pack(fill="both")
            aboutleftframe.pack(fill="both")

            abouttitle = tk.Label(aboutleftframe, text="[REDACTED] Launcher")
            authorlabel = tk.Label(aboutleftframe, text="Author: James King (Github: JamesK2754)")
            versionlabel = tk.Label(aboutleftframe, text=f"Version: {version}")
            licencelabel = tk.Label(aboutleftframe, text="Licence: MIT")
            abouttitle.grid(row=1, column=1)
            authorlabel.grid(row=2, column=1)
            versionlabel.grid(row=3, column=1)
            licencelabel.grid(row=4, column=1)
            advancedsettingslabel = tk.Label(aboutleftframe, text="Advanced settings\nThese will be helpful when updating to a new version of [R]L.")
            advancedsettingslabel.grid(row=5, column=1)
            def importpressed():
                filelocation = filedialog.askopenfilename(title="Select file location", initialdir="/", filetypes=[("Text Files", "*.txt")])
                try:
                    file = open(filelocation, "r")
                    fileconts = file.read()
                    file.close()
                    file = open(".secure_2.txt", "a+")
                    file.write(f"\n{fileconts}")
                    file.close()
                    messagebox.showwarning("Heads up!", "The app is going to restart in order to refresh the app list with the imported apps.")
                    aboutwin.destroy()
                    appwide.destroy()
                    outerloop()
                except:
                    messagebox.showerror("Error", "Something went wrong. Maybe check the location of the import file.")
            importbutton = tk.Button(aboutleftframe, text="Import app locations", command=importpressed)
            importbutton.grid(row=6, column=1)
            def exportpressed():
                messagebox.showwarning("Heads up!", "App locations will be exported to a plain text file, unencrypted. Keep this is mind when exporting. We reccomend deleting the file as soon as it is imported.")
                file = open(".secure_2.txt", "r")
                fileconts = file.read()
                file.close()
                filelocation = filedialog.askdirectory(title="Select export location", initialdir="/")
                file = open(f"{filelocation}/exported_locations.txt", "w")
                file.write(fileconts)
                file.close()
                messagebox.showwarning("Heads up!", "Export complete.")
            exportbutton = tk.Button(aboutleftframe, text="Export app locations", command=exportpressed)
            exportbutton.grid(row=7, column=1)
        aboutbutt = tk.Button(mainscreenleft, text="About", command=aboutpressed)
        aboutbutt.grid(row=5, column=1, rowspan=1, columnspan=2)

        def logoutpressed():
            appwide.destroy()
            outerloop()
        logoutbutt = tk.Button(mainscreenleft, text="Logout", command=logoutpressed)
        logoutbutt.grid(row=6, column=1, rowspan=1, columnspan=2)

        def exitpress():
            exit()
        exitbutt = tk.Button(mainscreenleft, text="Exit", command=exitpress)
        exitbutt.grid(row=7, column=1, rowspan=1, columnspan=2)



    def loginscreen():
        print("login")
        appwide.title("[REDACTED] Launcher - login")
        loginframe = tk.Frame(appwide)
        loginframe.pack(fill="both")

        logintitle = tk.Label(loginframe ,text="[REDACTED] Launcher\nLogin", font="none 30 bold")
        logintitle.pack(anchor="center", padx=5, pady=3)

        passwordentry = tk.Entry(loginframe)
        passwordentry.pack(anchor="center", padx=5, pady=3)
        def loginpress():
            print("Attempting login...")

            enteredpassword = passwordentry.get()
            if encryptpwd(enteredpassword) == password:
                print("Logged in")
                loginframe.destroy()

                mainrun(enteredpassword)
            else:
                print("Login failed")
                messagebox.showerror("Error", "The login details provided are not valid. Please try again.")
                passwordentry.delete(0, "end")
        loginenterbutton = tk.Button(loginframe, text="Login", command=loginpress)
        loginenterbutton.pack(anchor="center", padx=5, pady=3)
        def loginpressenter(self):
            loginpress()
        appwide.bind('<Return>', loginpressenter)

    loginscreen()
    appwide.mainloop()
outerloop()