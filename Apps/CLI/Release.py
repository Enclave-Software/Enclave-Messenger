import socket, threading, json, time, os, base64
from datetime import datetime
from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_OAEP

peer_status = "Offline"
activity_timeout = 60
easter_eggs = {
    "/joke": "Why do programmers hate nature? It has too many bugs.",
    "/ascii": "(>_<)", "/boom": "BOOM!", "/matrix": "[101010]", "/beep": "\a"
}

def load_keys():
    if not os.path.exists("private.pem") or not os.path.exists("public.pem"):
        key = RSA.generate(2048)
        with open("private.pem", "wb") as f: f.write(key.export_key())
        with open("public.pem", "wb") as f: f.write(key.publickey().export_key())
    with open("private.pem", "rb") as f: private_key = RSA.import_key(f.read())
    with open("public.pem", "rb") as f: public_key = RSA.import_key(f.read())
    return private_key, public_key

def encrypt_message(pub, msg):
    return base64.b64encode(PKCS1_OAEP.new(pub).encrypt(msg.encode()))

def decrypt_message(priv, enc):
    try:
        return PKCS1_OAEP.new(priv).decrypt(base64.b64decode(enc)).decode()
    except: return "[Decryption Failed]"

def update_status():
    global peer_status
    last = time.time()
    while True:
        if time.time() - last > activity_timeout:
            peer_status = "Idle"
        time.sleep(5)

def handle_input(sock, peer_pub):
    global peer_status
    while True:
        msg = input()
        peer_status = "Online"
        if msg in easter_eggs:
            print("You:", easter_eggs[msg]); continue
        sock.send(encrypt_message(peer_pub, msg))
        log_message("me", msg)

def handle_receive(sock, priv):
    global peer_status
    while True:
        try:
            data = sock.recv(4096)
            if data:
                peer_status = "Online"
                msg = decrypt_message(priv, data)
                print("Friend:", msg)
                log_message("friend", msg)
        except:
            peer_status = "Offline"
            break

def log_message(sender, msg):
    now = datetime.now().isoformat()
    data = {"time": now, "from": sender, "message": msg}
    enc = base64.b64encode(json.dumps(data).encode()).decode()
    with open("chat_log.json", "a") as f:
        json.dump({"entry": enc}, f)
        f.write("\n")

def start_server(port):
    priv, pub = load_keys()
    s = socket.socket(); s.bind(('', port)); s.listen(1)
    print("Waiting for connection..."); conn, addr = s.accept()
    print("Connected to", addr)
    conn.send(pub.export_key())
    peer_pub = RSA.import_key(conn.recv(4096))
    threading.Thread(target=handle_input, args=(conn, peer_pub)).start()
    threading.Thread(target=handle_receive, args=(conn, priv)).start()

def start_client(ip, port):
    priv, pub = load_keys()
    s = socket.socket(); s.connect((ip, port))
    s.send(pub.export_key())
    peer_pub = RSA.import_key(s.recv(4096))
    print("Connected to server.")
    threading.Thread(target=handle_input, args=(s, peer_pub)).start()
    threading.Thread(target=handle_receive, args=(s, priv)).start()

if __name__ == "__main__":
    print("Encrypted P2P Chat (CLI)")
    threading.Thread(target=update_status, daemon=True).start()
    mode = input("Start as server or client? (s/c): ").lower()
    if mode == "s":
        port = int(input("Enter port to listen on: "))
        start_server(port)
    else:
        ip = input("Enter server IP: ")
        port = int(input("Enter server port: "))
        start_client(ip, port)