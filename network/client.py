import socket
import threading
from PyQt5.QtCore import QThread, pyqtSignal

class Client(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def run(self):
        self.sock.connect((self.host, self.port))
        threading.Thread(target=self.receive_loop, daemon=True).start()

    def receive_loop(self):
        while True:
            try:
                data = self.sock.recv(1024).decode()
                if not data:
                    break
                self.message_received.emit(data)
            except Exception:
                break
        self.sock.close()

    def send(self, msg):
        try:
            self.sock.send(msg.encode())
        except Exception as e:
            print(f"Send error: {e}")