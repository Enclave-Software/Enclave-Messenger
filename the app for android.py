from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.clock import Clock
from kivy.core.window import Window
import socket, threading, time, random
from cryptography.fernet import Fernet

shared_key = Fernet.generate_key()
cipher = Fernet(shared_key)
conn = None

# Easter egg content
jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs.",
    "I told my computer I needed a break, and it said no problem — it’ll go to sleep."
]
ascii_art = ["¯\\_(ツ)_/¯", "( ͡° ͜ʖ ͡°)", "ಠ_ಠ"]

class ChatScreen(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(orientation='vertical', **kwargs)
        self.log = Label(size_hint_y=None, text_size=(Window.width, None), valign='top')
        self.scroll = ScrollView(size_hint=(1, 0.9))
        self.scroll.add_widget(self.log)
        self.add_widget(self.scroll)
        self.input = TextInput(size_hint=(1, 0.1), multiline=False)
        self.input.bind(on_text_validate=self.send_message)
        self.add_widget(self.input)

        threading.Thread(target=self.setup_connection, daemon=True).start()

    def log_msg(self, msg):
        self.log.text += msg + "\n"
        self.log.texture_update()
        self.log.height = self.log.texture_size[1]
        self.scroll.scroll_y = 0

    def emoji_rain(self):
        emojis = ['✨', '⚡', '🔥', '💣', '💥']
        for _ in range(10):
            self.log_msg(random.choice(emojis))
            time.sleep(0.1)

    def send_message(self, instance):
        msg = self.input.text
        if not msg: return

        # Easter eggs
        if msg == "/joke":
            msg = random.choice(jokes)
        elif msg == "/ascii":
            msg = random.choice(ascii_art)
        elif msg == "/boom":
            threading.Thread(target=self.emoji_rain).start()
            self.input.text = ""
            return

        encrypted = cipher.encrypt(msg.encode())
        if conn:
            conn.send(encrypted)
        self.log_msg(f"You: {msg}")
        self.input.text = ""

    def receive(self):
        while True:
            try:
                data = conn.recv(1024)
                if data:
                    msg = cipher.decrypt(data).decode()
                    Clock.schedule_once(lambda dt: self.log_msg(f"Peer: {msg}"))
            except:
                break

    def setup_connection(self):
        global conn
        try:
            server = socket.socket()
            server.bind(('0.0.0.0', 12345))
            server.listen(1)
            conn, _ = server.accept()
        except:
            conn = socket.socket()
            conn.connect(("192.168.0.2", 12345))  # Replace with actual IP

        threading.Thread(target=self.receive, daemon=True).start()

class ChatApp(App):
    def build(self):
        return ChatScreen()

if __name__ == "__main__":
    ChatApp().run()