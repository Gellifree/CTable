################################################
#--- Kovács Norbert - PTI-FOSZ              ---#
#--- 2020                                   ---#
#--- Operációsrendszerek gyakorlat beadandó ---#

from getpass import getpass
import os,encrypt

os.system("clear")

class User:
    def __init__(self,userName = "user",userPassword = "",userType = "normal"):
        self.userName = userName
        self.userPassword = userPassword
        self.userType = userType

class TimeTable():
    def __init__(self,user,data="000000-000000-000000-000000-000000-000000"):
        self.user = user
        self.data = data

#szintaxis ellenőrzés?
#def systaxCheck():
#    ?


def readData(data):
    index = 0
    userInformation = []
    for i in range(3):
        userInformation.append("")
        while(data[index] != ";"):
            userInformation[i] += data[index]
            index+=1
        index+=1
    result = User(userInformation[0],userInformation[1],userInformation[2])
    #Jelszó kódolása a .user file-ban
    return result

def menu(menuElements):
    result = 0

    for i in range(len(menuElements)):
        print("[{1}] {0}".format(menuElements[i],i+1))

    result = input("Kérlek adj meg egy menüopciót: ")
    return result

def login():
    os.system("clear")
    result = False

    print("Üdvözlöm a CTable bejelentkezési képernyőjén")
    adminName = input("Admin felhasználó: ")
    adminPassword = getpass("Admin jelszó: ")
    f = open(".user","r")
    for x in f:
        data = x
    data = encrypt.logData(data,20)
    f.close()
    admin = readData(data)
    if(adminName == admin.userName and adminPassword == admin.userPassword):
        print("Sikeres bejelentkezés!")
        result = True
    else:
        print("Felhasználónév vagy jelszó helytelen!")
    return result

def adminmenu():
    menuElements = ["Órarend hozzáadása","Órarend megtekintése","Órarend módosítása","Órarend törlése"]
    menuResult = menu(menuElements)
    return menuResult

def AddTimeTable():
    #tábla hozzáadása
    os.system("clear")
    print("CTable - Órarend hozzáadása")
    user = input("Az órarend tulajdonosa: ")
    #inputMethot = input("Beviteli módszer kiválasztása?")
    timeTable = input("Az órarend X formátumban: ")
    f = open(".tables","a")
    data = user + "-" + timeTable + "&" + "\n"
    f.write(data)
    f.close()


def DrawLine(size,count):
    print("+",end="")
    for i in range(count):
        for j in range(size):
            print("-",end = "")
        print("+", end = "")
    print()

def LookTimeTable(timeTable):
    print(timeTable.user)
    for i in range(7):
        DrawLine(8,6)
        print("| itt lesz az adat a timeTable.data-ból")

def GenerateTT_Class(dataInString):
    user = ""
    data = ""
    i = 0
    while(dataInString[i] != "-"):
        user += dataInString[i]
        i += 1
    i += 1
    while(dataInString[i] != "&"):
        data += dataInString[i]
    result = TimeTable(user,data)
    return result

def DrawBlock(number):
    print("+",end="")
    for i in range(number+2):
        print("-",end="")
    #print("+",end="")

def DrawLineFromList(list):
    for i in list:
        DrawBlock(len(i))
    print("+",end="")
    print()

def DrawDatasFromList(list):
    for i in list:
        print("| ",end="")
        print(i,"",end="")
    print("|",end="")
    print()

def DrawLessonsOut(Lessons,list):
    for i in range(6):
        #+8
        #print("| ",end="")
        #print(Lessons[i],end="")
        #for spaces in range(len(list[0])):
        #    print(" ",end="")
        print("| ",end="")
        for j in range(i,41,7):
            print(Lessons[j],end="")
            for spaces in range(0,len(list[j % 6-i])):
                   print(" ",end="")
                

            print("| ",end="")
        print()
        DrawLineFromList(list)
    
def DrawTable(list):
    DrawLineFromList(list)
    DrawDatasFromList(list)
    DrawLineFromList(list)
        


#_____MAIN_____
menuElements = ["Bejelentkezés","Segítség","Kilépés"]
adatok = ["Hétfő","Kedd","Szerda","Csütörtök","Péntek","Szombat"]
DrawTable(adatok)
DrawLessonsOut("W00000-W00000-E00000-G00000-000000-E00GGE",adatok)
print("CTable -- Szervezés és időbeosztás")
menuResult = menu(menuElements)
if(menuResult == "1"):
    #Bejelentkezés
    if(login() == True):
        os.system("clear")
        print("CTable Admin felület")
        admenu = adminmenu()
        if(admenu == "1"):
            print("tábla hozzáadása")
            #Tábla hozzáadása működget - jólenne üres tábla funkció beépítése
            AddTimeTable()
        if(admenu == "2"):
            print("Tábla megtekintése")
            f = open(".tables","r")
            for line in f:
                #Nyers stringből kiolvasás
                if(line[0] != "#"):
                    # Nem komment
                    print(GenerateTT_Class(line).user)
            f.close()
            #DrawLine(8,6)
        if(admenu == "3"):
            print("Tábla módosítása")
        if(admenu == "4"):
            print("Tábla törlése")
elif(menuResult == "2"):
    #Segítség
    print("--help")
else:
    print("A program most kilép.")



















    
