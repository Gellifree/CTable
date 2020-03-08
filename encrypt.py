import os

def __encrypt(text, key):
    result = ""
    for i in range(len(text)):
        result += chr(ord(text[i]) + key)
    return result

def __decrypt(text,key):
    result = ""
    for i in range(len(text)):
        result += chr(ord(text[i]) - key)
    return result

#f = open(".user","a")
#test = "root;root;admin;"
#f.write(encrypt(test,20))

def logData(text,key):
    return __decrypt(text,key)
