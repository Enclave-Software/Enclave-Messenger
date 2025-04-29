import socket, threading, tkinter as tk
from tkinter import simpledialog, scrolledtext
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.backends import default_backend

# Generate RSA keys if they don't exist
def generate_keys():
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend()
    )
    public_key = private_key.public_key()

    # Save private key
    with open("private_key.pem", "wb") as private_file:
        private_file.write(private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.TraditionalOpenSSL,
            encryption_algorithm=serialization.NoEncryption()
        ))

    # Save public key
    with open("public_key.pem", "wb") as public_file:
        public_file.write(public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        ))

    return private_key, public_key

# Load RSA keys
def load_keys():
    try:
        with open("private_key.pem", "rb") as private_file:
            private_key = serialization.load_pem_private_key(private_file.read(), password=None, backend=default_backend())

        with open("public_key.pem", "rb") as public_file:
            public_key = serialization.load_pem_public_key(public_file.read(), backend=default_backend())

        return private_key, public_key
    except:
        return generate_keys()

private_key, public_key = load_keys()

# Encrypt messages with RSA
def encrypt_message(message, public_key):
    encrypted_msg = public_key.encrypt(
        message.encode(),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return encrypted_msg

# Decrypt messages with RSA
def decrypt_message(encrypted_msg, private_key):
    original_msg = private_key.decrypt(
        encrypted_msg,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return original_msg.decode()

# Ask for shared key and mode
root = tk.Tk()
root.withdraw()
shared_key = simpledialog.askstring("Key", "Enter shared key (or leave blank to generate):")
if not shared_key:
    shared_key = Fernet.generate_key().decode()
    print("Share this key with your peer:", shared_key)
cipher = Fernet(shared_key.encode())
mode = simpledialog.askstring("Mode", "Enter mode (host/client):")

# GUI setup
root = tk.Tk()
root.title("Encrypted P2P Chat")
chat = scrolledtext.ScrolledText(root, state='disabled')
chat.pack()
msg_entry = tk.Entry(root)
msg_entry.pack(fill=tk.BOTH, expand=True)

# Networking setup
conn = None
username = simpledialog.askstring("Username", "Enter your username:")

# Networking and message handling
def receive(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                decrypted_msg = decrypt_message(data, private_key)
                chat.config(state='normal')
                chat.insert(tk.END, f"Peer: {decrypted_msg}\n")
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
        # Save encrypted message to log
        with open("chat_log.txt", "ab") as log_file:
            log_file.write(encrypt_message(msg, public_key))

msg_entry.bind("<Return>", send_msg)

# Socket connection
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