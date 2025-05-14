import socket, threading, tkinter as tk
from tkinter import simpledialog, scrolledtext, messagebox
from cryptography.fernet import Fernet
import random, time

# Shared key input
root = tk.Tk()
root.withdraw()
shared_key = simpledialog.askstring("Key", "Enter shared key (or leave blank to generate):")
if not shared_key:
    shared_key = Fernet.generate_key().decode()
    print("Share this key:", shared_key)
cipher = Fernet(shared_key.encode())
mode = simpledialog.askstring("Mode", "Enter mode (host/client):")


# GUI setup
root = tk.Tk()
root.title("Encrypted P2P Chat")
chat = scrolledtext.ScrolledText(root, state='disabled', bg="white")
chat.pack()
msg_entry = tk.Entry(root)
msg_entry.pack(fill=tk.BOTH, expand=True)


conn = None
username = simpledialog.askstring("Username", "Enter your username:")


# Konami code sequence
konami_sequence = ['Up', 'Up', 'Down', 'Down', 'Left', 'Right', 'Left', 'Right', 'b', 'a']
user_sequence = []


# Easter eggs
jokes = [
    "Why don't programmers like nature? Too many bugs.",
    "There are only 10 types of people in the world: those who understand binary and those who don’t.",
    "To understand recursion, you must first understand recursion."
]
ascii_art = [
    "( ͡° ͜ʖ ͡°)", "¯\\_(ツ)_/¯", "༼ つ ◕_◕ ༽つ"
]

def beep():
    try:
        print("beep")
    except:
        print("Beep not supported")


def matrix_mode():
    chat.config(bg="black", fg="green")
    msg_entry.config(bg="black", fg="lime")


def emoji_rain():
    emojis = ['💥', '✨', '🔥', '💣', '⚡']
    def drop():
        for _ in range(10):
            chat.config(state='normal')
            chat.insert(tk.END, random.choice(emojis) + '\n')
            chat.config(state='disabled')
            root.update()
            time.sleep(0.1)
    threading.Thread(target=drop).start()


def show_konami():
    messagebox.showinfo("Easter Egg!", "You unlocked the Konami secret!")


# Receive messages
def receive(sock):
    while True:
        try:
            data = sock.recv(1024)
            if data:
                msg = cipher.decrypt(data).decode()
                chat.config(state='normal')
                chat.insert(tk.END, f"Peer: {msg}\n")
                chat.config(state='disabled')
        except:
            break

# Send messages
def send_msg(event=None):
    msg = msg_entry.get()
    if msg:
        # Easter egg triggers
        if msg == "/joke":
            msg = random.choice(jokes)
        elif msg == "/ascii":
            msg = random.choice(ascii_art)
        elif msg == "/boom":
            emoji_rain()
            msg_entry.delete(0, tk.END)
            return
        elif msg == "/matrix":
            matrix_mode()
            msg_entry.delete(0, tk.END)
            return
        elif msg == "/beep":
            beep()
            msg_entry.delete(0, tk.END)
            return
        elif msg == "/send_boom":
            emoji_rain()
            encrypted_boom = cipher.encrypt("/boom".encode())
            conn.send(encrypted_boom)
            chat.config(state='normal')
            chat.insert(tk.END, f"{username}: /boom (sent)\n")
            chat.config(state='disabled')
            msg_entry.delete(0, tk.END)
            return


        encrypted = cipher.encrypt(msg.encode())
        conn.send(encrypted)
        chat.config(state='normal')
        chat.insert(tk.END, f"{username}: {msg}\n")
        chat.config(state='disabled')
        msg_entry.delete(0, tk.END)


# Konami sequence detection
def track_keys(event):
    key = event.keysym
    user_sequence.append(key)
    if user_sequence[-len(konami_sequence):] == konami_sequence:
        show_konami()


msg_entry.bind("<Return>", send_msg)
root.bind("<KeyPress>", track_keys)


# Connection setup
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

