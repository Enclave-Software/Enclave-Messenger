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

class AESCipher(object):

    def __init__(self, key):
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return AESCipher._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s) % self.bs) * chr(self.bs - len(s) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

message=str(input("Type your message: "))
print(send_sms(message))
if sent==True:
  print("Sent!")
elif sent==False:
  print("error")


 
