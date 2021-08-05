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

def logData(text,key):
    return __decrypt(text,key)

def tableEnc(text,key):
    return __encrypt(text,key)

def tableBack(text,key):
    return __decrypt(text,key)
