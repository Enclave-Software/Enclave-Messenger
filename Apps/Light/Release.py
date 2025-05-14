import socket, threading, tkinter as tk
from tkinter import simpledialog, scrolledtext
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

def generate_keys():
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=2048, backend=default_backend())
    public_key = private_key.public_key()
    with open("private_key.pem", "wb") as f:
        f.write(private_key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.TraditionalOpenSSL, serialization.NoEncryption()))
    with open("public_key.pem", "wb") as f:
        f.write(public_key.public_bytes(serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo))
    return private_key, public_key

def load_keys():
    try:
        with open("private_key.pem", "rb") as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None, backend=default_backend())
        with open("public_key.pem", "rb") as f:
            public_key = serialization.load_pem_public_key(f.read(), backend=default_backend())
        return private_key, public_key
    except:
        return generate_keys()

def encrypt_message(message, pubkey):
    return pubkey.encrypt(message.encode(), padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None))

def decrypt_message(encrypted, privkey):
    return privkey.decrypt(encrypted, padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)).decode()

private_key, public_key = load_keys()

root = tk.Tk()
root.withdraw()
shared_key = simpledialog.askstring("Key", "Enter shared key (or leave blank to generate):")
if not shared_key:
    shared_key = Fernet.generate_key().decode()
    print("Share this key with your peer:", shared_key)
cipher = Fernet(shared_key.encode())
mode = simpledialog.askstring("Mode", "Enter mode (host/client):")
username = simpledialog.askstring("Username", "Enter your username:")

root = tk.Tk()
root.title("Encrypted P2P Chat")
chat = scrolledtext.ScrolledText(root, state='disabled')
chat.pack()
msg_entry = tk.Entry(root)
msg_entry.pack(fill=tk.BOTH, expand=True)

conn = None

def receive(sock):
    while True:
        try:
            data = sock.recv(4096)
            if data:
                decrypted = decrypt_message(data, private_key)
                inner = cipher.decrypt(decrypted.encode()).decode()
                chat.config(state='normal')
                chat.insert(tk.END, f"Peer: {inner}\n")
                chat.config(state='disabled')
        except:
            break

def send_msg(event=None):
    msg = msg_entry.get()
    if msg:
        encrypted = cipher.encrypt(msg.encode())
        conn.send(encrypt_message(encrypted.decode(), public_key))
        chat.config(state='normal')
        chat.insert(tk.END, f"{username}: {msg}\n")
        chat.config(state='disabled')
        msg_entry.delete(0, tk.END)
        with open("chat_log.txt", "ab") as f:
            f.write(encrypt_message(msg, public_key))

msg_entry.bind("<Return>", send_msg)

def setup_connection():
    global conn
    if mode == 'host':
        server = socket.socket()
        server.bind(('0.0.0.0', 12345))
        server.listen(1)
        chat.insert(tk.END, "Waiting for connection...\n")
        conn, _ = server.accept()
    else:
        host_ip = simpledialog.askstring("Connect", "Enter host IP:")
        conn = socket.socket()
        conn.connect((host_ip, 12345))
    threading.Thread(target=receive, args=(conn,), daemon=True).start()

threading.Thread(target=setup_connection, daemon=True).start()
root.mainloop()