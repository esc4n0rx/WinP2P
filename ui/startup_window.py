from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel,
    QHBoxLayout, QFrame, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont, QColor, QPalette
from ui.main_window import MainWindow
from ui.config_window import ConfigWindow
from ui.about_window import AboutWindow
from ui.update_window import UpdateWindow
from ui.themes import THEMES

class MenuButton(QPushButton):
    """Botão estilizado para o menu principal"""
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.setMinimumHeight(50)
        self.setMinimumWidth(200)
        font = QFont()
        font.setPointSize(11)
        self.setFont(font)

class StartupWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle('WinP2P - Menu')
        self.resize(600, 400)
        
        self.setStyleSheet(THEMES.get(config.get('theme', 'XP'), ''))

        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        
        left_panel = QFrame()
        left_panel.setFixedWidth(200)
        left_panel.setFrameShape(QFrame.StyledPanel)
        left_panel.setFrameShadow(QFrame.Raised)
        
        left_layout = QVBoxLayout(left_panel)
        
        logo = QLabel()
        logo_pixmap = QPixmap(150, 150)
        logo_pixmap.fill(Qt.transparent)
        logo.setPixmap(logo_pixmap)
        logo.setAlignment(Qt.AlignCenter)
        
        info_label = QLabel(
            "<div align='center'>"
            "<h3>WinP2P</h3>"
            "<p>Versão 0.2.0</p>"
            "<p>Desenvolvido em Python</p>"
            "</div>"
        )
        info_label.setAlignment(Qt.AlignCenter)
        
        left_layout.addWidget(logo)
        left_layout.addWidget(info_label)
        left_layout.addStretch()
        
        right_panel = QFrame()
        right_layout = QVBoxLayout(right_panel)
        right_layout.setSpacing(20)
        
        title = QLabel("<h1>Bem-vindo ao WinP2P</h1>")
        title.setAlignment(Qt.AlignCenter)
        
        description = QLabel(
            "<p>Comunique-se de forma segura e privada com seus contatos.</p>"
            "<p>Escolha uma opção para começar:</p>"
        )
        description.setAlignment(Qt.AlignCenter)
        
        button_container = QFrame()
        button_layout = QVBoxLayout(button_container)
        button_layout.setSpacing(15)
        button_layout.setContentsMargins(50, 20, 50, 20)
        
        btn_new = MenuButton("Criar Nova Sala")
        btn_join = MenuButton("Entrar em uma Sala")
        btn_config = MenuButton("Configurações")
        btn_update = MenuButton("Verificar Atualizações")
        btn_about = MenuButton("Sobre")
        
        button_layout.addWidget(btn_new)
        button_layout.addWidget(btn_join)
        button_layout.addWidget(btn_config)
        button_layout.addWidget(btn_update)
        button_layout.addWidget(btn_about)
        

        btn_new.clicked.connect(self.new_chat)
        btn_join.clicked.connect(self.join_chat)
        btn_config.clicked.connect(self.open_config)
        btn_update.clicked.connect(self.check_updates)
        btn_about.clicked.connect(self.open_about)
        
        right_layout.addWidget(title)
        right_layout.addWidget(description)
        right_layout.addWidget(button_container)
        right_layout.addStretch()
        

        user_status = QLabel(f"Usuário atual: <b>{config.get('username', 'User')}</b>")
        user_status.setAlignment(Qt.AlignRight)
        right_layout.addWidget(user_status)
        

        main_layout.addWidget(left_panel)
        main_layout.addWidget(right_panel, 1)
        
        self.windows = []
        
        # Verificar atualizações automaticamente na inicialização
        if config.get('check_updates_at_startup', True):
            from ui.update_window import UpdateWindow
            UpdateWindow.check_for_updates_on_startup(self, config)

    def new_chat(self):
        """Iniciar nova sala de chat"""
        self.main = MainWindow(self.config, new_room=True)
        self.main.show()
        self.close()

    def join_chat(self):
        """Juntar-se a uma sala existente"""
        self.main = MainWindow(self.config, new_room=False)
        self.main.show()
        self.close()

    def open_config(self):
        """Abrir janela de configurações"""
        self.config_win = ConfigWindow(self.config)
        self.windows.append(self.config_win)  
        self.config_win.show()
    
    def check_updates(self):
        """Abrir janela de atualizações"""
        self.update_win = UpdateWindow(self.config, self)
        self.windows.append(self.update_win)
        self.update_win.show()

    def open_about(self):
        """Abrir janela Sobre"""
        self.about = AboutWindow()
        self.windows.append(self.about) 
        self.about.show()