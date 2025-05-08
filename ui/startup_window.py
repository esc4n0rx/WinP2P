from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from ui.main_window import MainWindow
from ui.config_window import ConfigWindow
from ui.about_window import AboutWindow

class StartupWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle('Vintage P2P Chat - Menu')
        self.resize(300, 200)

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setSpacing(10)

        title = QLabel('<h2>Vintage P2P Chat</h2>')
        layout.addWidget(title)

        btn_new = QPushButton('Novo Chat')
        btn_join = QPushButton('Entrar em uma Sala')
        btn_config = QPushButton('Configurações')
        btn_about = QPushButton('Sobre')

        layout.addWidget(btn_new)
        layout.addWidget(btn_join)
        layout.addWidget(btn_config)
        layout.addWidget(btn_about)

        btn_new.clicked.connect(self.new_chat)
        btn_join.clicked.connect(self.join_chat)
        btn_config.clicked.connect(self.open_config)
        btn_about.clicked.connect(self.open_about)

    def new_chat(self):
        self.main = MainWindow(self.config, new_room=True)
        self.main.show()
        self.close()

    def join_chat(self):
        self.main = MainWindow(self.config, new_room=False)
        self.main.show()
        self.close()

    def open_config(self):
        self.config_win = ConfigWindow(self.config)
        self.config_win.show()

    def open_about(self):
        self.about = AboutWindow()
        self.about.show()