import socket, threading, json, time, os
from datetime import datetime
from pgpy import PGPKey, PGPMessage, PGPUID
from pgpy.constants import PubKeyAlgorithm, KeyFlags, HashAlgorithm, SymmetricKeyAlgorithm

# Generate/load keys
key_file = "pgp_key.json"
if os.path.exists(key_file):
    with open(key_file, "r") as f:
        keys = json.load(f)
        priv_key = PGPKey()
        priv_key.parse(keys["private"])
        pub_key = PGPKey()
        pub_key.parse(keys["public"])
else:
    priv_key = PGPKey.new(PubKeyAlgorithm.RSAEncryptOrSign, 2048)
    uid = PGPUID.new("Ghost", comment="Secure CLI", email="ghost@cli")
    priv_key.add_uid(uid, usage={KeyFlags.EncryptCommunications},
                     hashes=[HashAlgorithm.SHA256], ciphers=[SymmetricKeyAlgorithm.AES256])
    pub_key = priv_key.pubkey
    with open(key_file, "w") as f:
        json.dump({"private": str(priv_key), "public": str(pub_key)}, f)

log_file = "chat_log.json"
status_file = "status.json"
chats = []

def save_log(entry):
    chats.append(entry)
    with open(log_file, "w") as f:
        json.dump(chats, f, indent=2)

def update_status(status):
    with open(status_file, "w") as f:
        json.dump({"status": status, "timestamp": time.time()}, f)

def encrypt(msg):
    return str(pub_key.encrypt(PGPMessage.new(msg)))

def decrypt(enc):
    try:
        return priv_key.decrypt(PGPMessage.from_blob(enc)).message
    except:
        return "[Decryption failed]"

def handle_client(conn, addr):
    print(f"[+] Connection from {addr}")
    update_status("Online")
    while True:
        try:
            data = conn.recv(4096).decode()
            if not data:
                break
            msg = decrypt(data)
            print(f"{addr}: {msg}")
            save_log({"from": str(addr), "message": msg, "time": datetime.now().isoformat()})
        except:
            break
    conn.close()
    update_status("Offline")

def server_thread(port=12345):
    s = socket.socket()
    s.bind(("0.0.0.0", port))
    s.listen(1)
    print("[*] Listening on port", port)
    while True:
        conn, addr = s.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

def send_message(ip, port, message):
    s = socket.socket()
    s.connect((ip, port))
    s.send(encrypt(message).encode())
    s.close()
    save_log({"to": ip, "message": message, "time": datetime.now().isoformat()})

def easter_egg(cmd):
    if cmd == "/joke":
        return "Why do Python devs wear glasses? Because they can't C."
    elif cmd == "/ascii":
        return "  (•_•)\n <)   )╯ ASCII!\n /    \\"
    elif cmd == "/status":
        return f"Status: {json.load(open(status_file))}"
    return None

# Start server thread
threading.Thread(target=server_thread, daemon=True).start()

# CLI Loop
print("Ghost Secure Messenger CLI (type '/help' for commands)")
while True:
    inp = input("> ")
    if inp == "/help":
        print("Commands: /send [ip] [message], /joke, /ascii, /status, /exit")
    elif inp.startswith("/send"):
        parts = inp.split()
        ip = parts[1]
        msg = " ".join(parts[2:])
        send_message(ip, 12345, msg)
    elif inp == "/exit":
        break
    elif inp.startswith("/"):
        egg = easter_egg(inp)
        if egg:
            print(egg)
        else:
            print("Unknown command")
