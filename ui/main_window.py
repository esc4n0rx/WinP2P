from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTextEdit, QLineEdit, QPushButton, QLabel,
    QInputDialog, QMessageBox, QApplication
)
from network.server import Server
from network.client import Client
from utils.code_generator import generate_room_code, decode_room_code
from ui.themes import THEMES
import socket

class MainWindow(QMainWindow):
    def __init__(self, config, new_room=False):
        super().__init__()
        self.config = config
        self.setWindowTitle('Vintage P2P Chat')
        self.resize(600, 400)
        self.setStyleSheet(THEMES.get(config.get('theme', 'XP'), ''))

        # Widgets
        self.chat_display = QTextEdit(readOnly=True)
        self.msg_input = QLineEdit()
        self.send_btn = QPushButton('Send')
        self.user_label = QLabel(f"User: {config['username']}")

        central = QWidget()
        self.setCentralWidget(central)
        vbox = QVBoxLayout(central)
        vbox.addWidget(self.user_label)
        vbox.addWidget(self.chat_display)
        hmsg = QHBoxLayout()
        hmsg.addWidget(self.msg_input)
        hmsg.addWidget(self.send_btn)
        vbox.addLayout(hmsg)

        self.server = None
        self.client = None

        if new_room:
            # Start server
            port = config['port']
            self.server = Server('0.0.0.0', port)
            self.server.message_received.connect(self.display_message)
            self.server.start()

            # Generate code embedding IP:port
            local_ip = socket.gethostbyname(socket.gethostname())
            room_code = generate_room_code(local_ip, port)

            # Copy to clipboard
            clipboard = QApplication.clipboard()
            clipboard.setText(room_code)

            # Inform user
            QMessageBox.information(
                self, 'Room Code',
                f'Código da Sala:\n{room_code}\n\n(copiado para a área de transferência)'
            )
        else:
            code, ok = QInputDialog.getText(self, 'Entrar na Sala', 'Insira o Código da Sala:')
            if ok:
                try:
                    ip, port = decode_room_code(code)
                    self.client = Client(ip, port)
                    self.client.message_received.connect(self.display_message)
                    self.client.start()
                except Exception as e:
                    QMessageBox.critical(self, 'Erro', str(e))

        self.send_btn.clicked.connect(self.send_message)

    def display_message(self, msg):
        self.chat_display.append(msg)

    def send_message(self):
        text = self.msg_input.text().strip()
        if not text:
            return
        msg = f"{self.config['username']}: {text}"
        if self.client:
            self.client.send(msg)
        self.display_message(msg)
        self.msg_input.clear()