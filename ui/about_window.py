from PyQt5.QtWidgets import QMainWindow, QLabel, QVBoxLayout, QWidget

class AboutWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sobre')
        self.resize(300, 150)
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        info = QLabel('<b>Vintage P2P Chat</b><br>Versão 1.0<br>Desenvolvido em Python e PyQt5')
        layout.addWidget(info)