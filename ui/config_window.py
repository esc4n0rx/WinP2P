from PyQt5.QtWidgets import QMainWindow, QWidget, QFormLayout, QLineEdit, QComboBox, QPushButton
import json
from ui.themes import THEMES

class ConfigWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle('Configurações')
        self.resize(300, 200)

        central = QWidget()
        self.setCentralWidget(central)
        form = QFormLayout(central)

        self.username = QLineEdit(config['username'])
        self.port = QLineEdit(str(config['port']))
        self.theme = QComboBox()
        self.theme.addItems(THEMES.keys())
        self.theme.setCurrentText(config['theme'])

        form.addRow('Usuário:', self.username)
        form.addRow('Porta:', self.port)
        form.addRow('Tema:', self.theme)

        btn_save = QPushButton('Salvar')
        btn_save.clicked.connect(self.save)
        form.addRow(btn_save)

    def save(self):
        self.config['username'] = self.username.text().strip() or 'User'
        self.config['port'] = int(self.port.text())
        self.config['theme'] = self.theme.currentText()
        with open('config.json', 'w') as f:
            json.dump(self.config, f, indent=4)
        self.close()