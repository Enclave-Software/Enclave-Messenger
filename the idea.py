#imports
import requests
import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

#the values
sent=False

def sent(yes):
  if yes==True:
    print("Sent!")
  elif yes==False:
    print("error")

def encryption(mes):
  msg = input("Enter a message to encrypt: ")
  encmsg = ""
  for ch in msg:
    asc = ord(ch) + 3
    ench = chr(asc)
    encmsg += ench
  return encmsg

def send_sms(mes):
  fin_mes=encryption(mes)
  return fin_mes

message=str(input("Type your message: "))
print(send_sms(message))
if sent==True:
  print("Sent!")
elif sent==False:
  print("error")


 
