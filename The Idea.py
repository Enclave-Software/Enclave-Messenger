import requests
def encryption(mes):
  enc_mes=mes+"(This message is encrypted)"
  return enc_mes
def send_sms(mes):
  sem_fin_mes=encryption(mes)
  return fin_mes
message=str(input("Type your message: "))
send_sms(message)