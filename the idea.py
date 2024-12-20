#imports
import requests

#the values
sent=False

def sent(yes):
  if yes==True:
  print("Sent!")
elif yes==False:
  print("error")

def encryption(mes):
  enc_mes=mes+"(This message is encrypted)"
  return enc_mes

def send_sms(mes):
  fin_mes=encryption(mes)
  return fin_mes

message=str(input("Type your message: "))
print(send_sms(message))
if sent==True:
  print("Sent!")
elif sent==False:
  print("error")
 
