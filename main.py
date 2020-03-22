# >> Kovács Norbert          <<
# >> 2020                    <<
# >> Op. rend. gyakorlat     <<
# >> CTable alkalmazás       <<

import os
import encrypt as en
from getpass import getpass


# Classes
class User():
    def __init__(self, userName, userPassword = "",userType = "normal"):
        self.userName = userName
        self.userPassword = userPassword
        self.userType = userType

class TimeTable():
    def __init__(self,user,data="000000-000000-000000-000000-000000-000000"):
        self.user = user
        self.data = data

class SyntaxChecker():
    def musntContain(self,text,char):
        for i in text:
            if(i == char):
                return False
        return True
        
    def mustContain(self,text,char,piece):
        count = 0
        for i in text:
            if(i == char):
                count += 1
        if(count == piece):
            return True
        else:
            return False
            
    def distanceCheck(self,text,char,distance):
        distanceList = []
        lessons = ""
        for i in range(len(text)):
            if(text[i] != char):
                lessons += text[i]
            if(text[i] == char):
                distanceList.append(len(lessons))
                lessons = ""
        distanceList.append(len(lessons))
        for i in distanceList:
            if(i != distance):
                return False
        return True

    def nameCheck(self,name):
        if(self.musntContain(name,"-") == True and len(name)>3):
            return True
        else:
            return False

    def lessonsCheck(self, lessons):
        if(self.mustContain(lessons,"-",5) == True and self.distanceCheck(lessons,"-",6) == True):
            return True
        else:
            return False
    #Lesson char check? [L-W-P-0]

    
# Functions

# User
def readUserData(data):
    index = 0
    userInformation = []
    for i in range(3):
        userInformation.append("")
        while(data[index] != ";"):
            userInformation[i] += data[index]
            index += 1
        index+=1
    return User(userInformation[0],userInformation[1],userInformation[2])

# Functions for Executable Menu
def login():
    os.system('setterm -foreground yellow')
    userName = input(" Username: ")
    userPassword = getpass(" Password: ")
    os.system('setterm -foreground white')
    users = open(".user","r")

    for user in users:
        data = user
        # Only one user exist at the time - maybe later we want to expand
    data = en.logData(data,20)
    users.close()
    user = readUserData(data)
    if(userName == user.userName and userPassword == user.userPassword):
        print("\n > Login successful <")
        return True
    else:
        print(" > Username or Password is not correct <\n")
        logAttempt(userName,userPassword)
        return False
    
# saving unsuccesfull login attempts
def logAttempt(userName,userPassword):
    f = open(".log","a")
    f.write(" > login attempt <\n")
    f.write("username: "+userName+"; password: "+userPassword+"\n") # Time
    f.close()
    
# displaying help file
def help():
    os.system("clear")
    width = os.get_terminal_size().columns
    os.system('setterm -foreground blue')
    print("CTable",end="")
    print("CTable help screen\n".center(width))
    os.system('setterm -foreground white')
    os.system("cat help")
    #os.system("less help")
    #not readable on small screen

def settings():
    print("     >> Settings are not available yet<<\n")
    #language change (eng, hun), stay logged in, delete/exit/logout without confirmation
    #set encryption key, simple-mode [yes-no] -> not draws tables 

# Search for existing owner
def fileContaining(name):
    f = open(".tables","r")
    users = []
    for line in f:
        if(line[0] != "#"):
            actualTimeTable = generateTT_Class(line)
            users.append(actualTimeTable.user)
    f.close()
    for user in users:
        if(name == user):
            return True
    return False

def addTimeTable():
    os.system("clear")
    width = os.get_terminal_size().columns
    os.system('setterm -foreground blue')
    print("CTable",end="")
    print("Add TimeTable\n".center(width))
    os.system('setterm -foreground white')
    
    synCh = SyntaxChecker()
    owner = ""
    while(synCh.nameCheck(owner) == False or fileContaining(owner) == True):    
        owner = input(" The owner of the table: ")
        if(synCh.nameCheck(owner) == False):
            print(" > Name has to be longer tha 3 characters, and can not contain '-' symbol <\n")
        elif(fileContaining(owner) == True):
            print(" > Owner allready exist in database <\n")
        else:
            print(" > Name accepted <\n")
    timeTable = ""
    while(synCh.lessonsCheck(timeTable) == False):
        timeTable = input(" The formatted lessons[6x6]: ")
        if(synCh.lessonsCheck(timeTable) == False):
            print(" > Wrong format <")
            print(" > Please read the help file instructions <\n")
        else:
            print(" > TimeTable accepted <\n")
    f = open(".tables","a")
    data = owner + "-" + timeTable + "&\n"
    f.write(data)
    f.close()
    
# generating class from a string
def generateTT_Class(line):
    user = ""
    lessons = ""
    i = 0
    while(line[i] != "-"):
        user += line[i]
        i += 1
    i += 1
    while(line[i] != "&"):
        lessons += line[i]
        i += 1
    return TimeTable(user,lessons)

def watchTimeTable():
    f = open(".tables","r")
    menuItems = []
    userList = []

    for line in f:
        #ignoring comments
        if(line[0] != "#"):
            actualTimeTable = generateTT_Class(line)
            menuItems.append(actualTimeTable.user)
            userList.append(actualTimeTable)
    print("     Which TimeTable you want to watch?\n")
    menuItems.append("Cancel")
    result =  drawMenu(menuItems)

    if(result == str(len(menuItems)-1)):
        print(" > action cancelled <")
    else:
        days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
        print("\n Owner: "+menuItems[int(result)])
        drawTable(days)
        drawLessonsOut(userList[int(result)].data,days)

def logOut():
    result = input(" Are you sure you want to log out? [Y/n]: ")
    if(result == "n" or result == "N"):
        return True
    elif(result == "" or result == "Y" or result == "y"):
        return False

def deleteTable():
    f = open(".tables","r")
    menuItems = []
    informations = []
    for line in f:
        informations.append(line)
        if(line[0] != "#"):
            actualTimeTable = generateTT_Class(line)
            menuItems.append(actualTimeTable.user)
    menuItems.append("Cancel")
    print("     Which TimeTable you want to Delete?\n")
    result = drawMenu(menuItems)
    deleTable = menuItems[int(result)]
    f.close()
    

    if(deleTable == "Cancel"):
        print("\n > action cancelled <")
    else:
        f = open(".tables","w")
        for line in informations:
            if(deleTable in line):
                print("\n > " + deleTable + " deleted <")
            else:
                f.write(line)
        f.close()

def watchDay():
    menuItems = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    print("     Which day you wish to inspect?\n")
    result = drawMenu(menuItems)
    daylist = calculateDay(int(result))
    drawColumnFromList(daylist,menuItems[int(result)])
    quit = input(" Do you wish to inspect a specific time? [Y/n]: ")
    if(quit == "y" or quit == "Y" or quit == ""):
        calculateOneLesson(int(result))


def watchWeek():
    drawWeek()
    watchD = input("\n Do you wish to watch a specific day? [Y/n]: ")

    menuItems = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    print("\n     Which day you wish to inspect?\n")
    result = drawMenu(menuItems)
    
    if(watchD == "y" or watchD == "Y" or watchD == ""):
        calculateOneLesson(int(result))
    
# Drawing session
def drawBlock(number):
    print("+",end="")
    for i in range(number+2):
        print("-",end="")

def drawLineFromList(list):
    for i in list:
        drawBlock(len(i))
    print("+")

def drawDatasFromList(list):
    for i in list:
        print("| ",end="")
        print(str(i)+"",end=" ")
    print("|")

def drawLessonsOut(Lessons,list):
    for i in range(6):
        print("| ",end="")
        for j in range(i,41,7):
            print(Lessons[j],end="")
            for spaces in range(0,len(list[j % 6-i])): 
                   print(" ",end="")
            print("| ",end="")
        print()
        drawLineFromList(list)
    
def drawTable(list):
    os.system('setterm -foreground blue -bold on')
    drawLineFromList(list)
    drawDatasFromList(list)
    drawLineFromList(list)
    os.system('setterm -foreground white -bold off')

def drawSingleItem(item):
    drawBlock(len(item))
    os.system('setterm -foreground blue -bold on')
    print("+\n| "+item+" |")
    drawBlock(len(item))
    print("+")
    os.system('setterm -foreground white -bold off')

def drawColumn(data,header):
    drawSingleItem(header)
    
    for inf in data:
        print("| "+inf,end="")
        for spaces in range(len(header)):
            print(" ",end="")
        print("|")
        drawBlock(len(header))
        print("+")

def drawColumnFromList(datas,header):
    drawSingleItem(header)
    for inf in datas:
        print("| "+str(inf)+" %",end="")
        for spaces in range(len(header)-len(str(inf))-1):
            print(" ",end="")
        print("|")
        drawBlock(len(header))
        print("+")

def drawWeek():
    days = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"]
    drawTable(days)
    weekData = calculateWeek()

    for i in range(6):
        for j in range(6):
            print("| "+str(weekData[j][i]),end=" % ")
            for spaces in range(len(str(days[j % 6]) ) - len(str(weekData[j][i]))-2):
                print(" ",end="")
        print("|")
        drawLineFromList(days)

# Menu
def drawMenu(menuElements):
    index = 0
    for menuItem in menuElements:
        print("     [{0}] {1}".format(index,menuItem))
        index += 1
    print()
    return input(" >> ")

# Calculations
def calculateDay(dayIndex):
    result = [0,0,0,0,0,0] # count
    tablesList = []
    f = open(".tables","r")
    for line in f:
        if(line[0] != "#"):
            tablesList.append(generateTT_Class(line))
    f.close()
    for table in tablesList:
        index = 0
        for i in range(dayIndex*7,dayIndex*7+6):
            if(table.data[i] == "0"):
                result[index] +=1
            index +=1

    for i in range(len(result)):
        result[i] = int((result[i]/len(tablesList))*100) #percent   
    return result

def calculateOneLesson(dayIndex):
    print("\n     Which time?\n")
    menuItems = ["8:00 - 9:40","10:00 - 11:40","11:50 - 13:30","13:40 - 15:20","15:30 - 17:10","17:20 - 19:00"]
    result = drawMenu(menuItems)
    tablesList = []
    availableMembers = []
    nonAvailableMembers = []
    f = open(".tables","r")
    for line in f:
        if(line[0] != "#"):
            tablesList.append(generateTT_Class(line))
    f.close()
    
    for table in tablesList:
        index = 0
        if(table.data[dayIndex*7+int(result)] == "0"):
            availableMembers.append(table.user)
        else:
            nonAvailableMembers.append(table.user + " - [" + table.data[dayIndex*7+int(result)]+"]")
    print("\n The list of the available members of the group at "+menuItems[int(result)]+": \n")

    os.system('setterm -foreground green')
    for member in availableMembers:
        print(" -- "+member)
    os.system('setterm -foreground white')
    print("\n The list of the non available members of the group at "+menuItems[int(result)]+":\n")
    #print(" -- Name - [R]eason\n")
    os.system('setterm -foreground red')
    for member in nonAvailableMembers:
        print(" -- "+member)
    os.system('setterm -foreground white')
    print()

def calculateWeek():
    weekDays = [[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0],[0,0,0,0,0,0]]
    tablesList = []
    f = open(".tables","r")
    for line in f:
        if(line[0] != "#"):
            tablesList.append(generateTT_Class(line))
    f.close()
    dayIndex = 0
    index = 0
    result = [0,0,0,0,0,0]
    for table in tablesList:
        for times in range(6):
            index = 0
            for i in range(dayIndex*7,dayIndex*7+6):
                if(table.data[i] == "0"):
                    result[index] +=1
                index +=1
            for i in range(6):
                weekDays[dayIndex][i] += result[i]
            dayIndex +=1
            result = [0,0,0,0,0,0]
        dayIndex = 0

    for i in range(6):
        for j in range(6):
            weekDays[i][j] = int((weekDays[i][j]/len(tablesList))*100) # to percent
    return weekDays 
        

# Main block
loggedIn = False
menuState = 0
subMenuState = 0
answer = "0"
mainMenu = ["Login","Help","Settings"]
mainMenuExec = ["loggedIn = login()","help()","settings()"]

adminMenu = ["Add Table","Watch Table","Delete Table","Watch Day","Watch Week","Log out"]
adminMenuExec = ["addTimeTable()","watchTimeTable()","deleteTable()","watchDay()","watchWeek()","loggedIn = logOut()"] 

menues = []
menues.append(mainMenu)
menues.append(adminMenu)

execMenu = []
execMenu.append(mainMenuExec)
execMenu.append(adminMenuExec)

while(answer != "q" and answer != "Q"):
    os.system("clear")
    
    width = os.get_terminal_size().columns
    log = ""
    if(loggedIn == True):
        log = "Logged in as root"
        menuState = 1
    else:
        log = "Logged out       "
        menuState = 0
    os.system('setterm -foreground blue')
    print(log,end="")
    print("CTable\n".center(width-len(log)-6))
    os.system('setterm -foreground white')

    answer = drawMenu(menues[menuState])
    if(answer != "q" and answer != "Q"):
        subMenuState = int(answer)
        print(" >> "+menues[menuState][subMenuState]+" <<\n")
        exec(execMenu[menuState][subMenuState])

        input(" >> done << ")
    else:
        quit = input(" Are you sure, you want to quit? [Y/n]: ")
        if(quit == "n" or quit == "N"):
            answer = "0"
        elif(quit == ""):
            answer = "q"
            os.system("clear")
