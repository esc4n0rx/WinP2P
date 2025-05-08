import socket
import threading
from PyQt5.QtCore import QThread, pyqtSignal

class Server(QThread):
    message_received = pyqtSignal(str)

    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []

    def run(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        conn, addr = self.sock.accept()
        self.clients.append(conn)
        threading.Thread(target=self.handle_client, args=(conn,), daemon=True).start()

    def handle_client(self, conn):
        while True:
            try:
                data = conn.recv(1024).decode()
                if not data:
                    break
                self.message_received.emit(data)
            except Exception:
                break
        conn.close()