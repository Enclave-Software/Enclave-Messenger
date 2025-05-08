import requests

API_URL = "http://127.0.0.1:5000"

def register():
    u = input("New username: ")
    p = input("Password: ")
    r = requests.post(f"{API_URL}/register", json={"username": u, "password": p})
    print("Registered" if r.status_code == 201 else r.json().get("error", "Error"))

def login():
    u = input("Username: ")
    p = input("Password: ")
    r = requests.post(f"{API_URL}/login", json={"username": u, "password": p})
    if r.status_code == 200:
        print("Login successful")
        return u
    else:
        print("Login failed")
        return None

def send_message(user):
    to = input("To: ")
    msg = input("Message: ")
    r = requests.post(f"{API_URL}/send", json={"sender": user, "recipient": to, "message": msg})
    print("Sent" if r.status_code == 200 else "Failed to send")

def inbox(user):
    r = requests.get(f"{API_URL}/inbox/{user}")
    if r.status_code == 200:
        msgs = r.json()
        if not msgs:
            print("Inbox is empty.")
        for m in msgs:
            print(f"{m['from']}: {m['message']}")
    else:
        print("Could not fetch inbox.")

def all_chats(user):
    r = requests.get(f"{API_URL}/chats/{user}")
    if r.status_code == 200:
        users = r.json()
        if users:
            print("Chat history with:")
            for u in users:
                print("-", u)
        else:
            print("No chat history found.")
    else:
        print("Failed to fetch chat list.")

def main():
    print("Ghost CLI Chat")
    while True:
        action = input("[login/register/exit]: ").strip().lower()
        if action == "register":
            register()
        elif action == "login":
            user = login()
            if user:
                while True:
                    cmd = input("[send/inbox/allchats/logout]: ").strip().lower()
                    if cmd == "send":
                        send_message(user)
                    elif cmd == "inbox":
                        inbox(user)
                    elif cmd == "allchats":
                        all_chats(user)
                    elif cmd == "logout":
                        break
        elif action == "exit":
            break

if __name__ == "__main__":
    main()