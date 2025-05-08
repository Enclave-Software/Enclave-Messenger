import socket
import threading
import json
import time
import os
import base64
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP
from getpass import getuser

# Globals
peer_status = "Offline"
activity_timeout = 60
easter_eggs = {
    "/joke": "Why do programmers hate nature? It has too many bugs.",
    "/ascii": "(>_<)",
    "/boom": "BOOM! (But quietly...)",
    "/matrix": "[101010] Welcome to Hacker Mode.",
    "/beep": "\a"
}

# Generate or load keys
def load_keys():
    if not os.path.exists("private.pem") or not os.path.exists("public.pem"):
        key = RSA.generate(2048)
        with open("private.pem", "wb") as f:
            f.write(key.export_key())
        with open("public.pem", "wb") as f:
            f.write(key.publickey().export_key())
    with open("private.pem", "rb") as f:
        private_key = RSA.import_key(f.read())
    with open("public.pem", "rb") as f:
        public_key = RSA.import_key(f.read())
    return private_key, public_key

def encrypt_message(public_key, message):
    cipher = PKCS1_OAEP.new(public_key)
    return base64.b64encode(cipher.encrypt(message.encode()))

def decrypt_message(private_key, enc_message):
    try:
        cipher = PKCS1_OAEP.new(private_key)
        return cipher.decrypt(base64.b64decode(enc_message)).decode()
    except:
        return "[Decryption Failed]"

# Status updater
def update_status():
    global peer_status
    last_time = time.time()
    while True:
        if time.time() - last_time > activity_timeout:
            peer_status = "Idle"
        time.sleep(5)

def handle_input(sock, pubkey):
    global peer_status
    while True:
        msg = input()
        peer_status = "Online"
        if msg in easter_eggs:
            print("You:", easter_eggs[msg])
            continue
        enc = encrypt_message(pubkey, msg)
        sock.send(enc)
        log_message("me", msg)

def handle_receive(sock, privkey):
    global peer_status
    while True:
        try:
            data = sock.recv(4096)
            if data:
                peer_status = "Online"
                msg = decrypt_message(privkey, data)
                print("Friend:", msg)
                log_message("friend", msg)
        except:
            peer_status = "Offline"
            break

def log_message(sender, message):
    now = datetime.now().isoformat()
    data = {"time": now, "from": sender, "message": message}
    enc_data = base64.b64encode(json.dumps(data).encode()).decode()
    with open("chat_log.json", "a") as f:
        json.dump({"entry": enc_data}, f)
        f.write("\n")

def start_server(port):
    priv, pub = load_keys()
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(('', port))
    server.listen(1)
    print("Waiting for connection...")
    conn, addr = server.accept()
    print("Connected to", addr)
    threading.Thread(target=handle_input, args=(conn, pub)).start()
    threading.Thread(target=handle_receive, args=(conn, priv)).start()

def start_client(ip, port):
    priv, pub = load_keys()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((ip, port))
    print("Connected to server.")
    threading.Thread(target=handle_input, args=(sock, pub)).start()
    threading.Thread(target=handle_receive, args=(sock, priv)).start()

if __name__ == "__main__":
    print("Encrypted P2P Chat (CLI)")
    mode = input("Start as server or client? (s/c): ").lower()
    threading.Thread(target=update_status, daemon=True).start()
    if mode == "s":
        port = int(input("Enter port to listen on: "))
        start_server(port)
    else:
        ip = input("Enter server IP: ")
        port = int(input("Enter server port: "))
        start_client(ip, port)