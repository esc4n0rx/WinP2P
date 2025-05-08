from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, 
    QTabWidget, QTextBrowser, QPushButton, QHBoxLayout
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont

class AboutWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sobre o WinP2P Chat')
        self.resize(500, 400)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        title_layout = QHBoxLayout()
        
        logo = QLabel()
        logo_pixel = QPixmap(64, 64)
        logo_pixel.fill(Qt.transparent)
        logo.setPixmap(logo_pixel)
        
        title_text = QLabel('<h1>WinP2P</h1><h3>Versão 0.1</h3>')
        title_text.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        title_layout.addWidget(logo)
        title_layout.addWidget(title_text)
        title_layout.addStretch()
        
        tabs = QTabWidget()
        
        about_tab = QWidget()
        about_layout = QVBoxLayout(about_tab)
        
        about_text = QTextBrowser()
        about_text.setOpenExternalLinks(True)
        about_text.setHtml("""
            <p>WinP2P  é um aplicativo de chat ponto-a-ponto seguro
            e com interfaces inspiradas em designs clássicos de sistemas operacionais.</p>
            
            <p>Desenvolvido em Python e PyQt5, este aplicativo oferece:</p>
            <ul>
                <li>Comunicação direta entre peers (P2P)</li>
                <li>Criptografia de ponta-a-ponta</li>
                <li>Temas vintage e modernos</li>
                <li>Status de usuário em tempo real</li>
                <li>Salas privadas com limite de 2 usuários</li>
            </ul>
            
            <p>Criado para compartilhar a nostalgia das interfaces clássicas
            dos anos 90 e 2000, com toda a segurança e funcionalidade modernas.</p>
        """)
        
        about_layout.addWidget(about_text)
        
        features_tab = QWidget()
        features_layout = QVBoxLayout(features_tab)
        
        features_text = QTextBrowser()
        features_text.setHtml("""
            <h3>Recursos Principais</h3>
            
            <h4>Comunicação</h4>
            <ul>
                <li>Chat ponto-a-ponto direto</li>
                <li>Indicadores de status (online, digitando)</li>
                <li>Notificações de eventos de conexão</li>
            </ul>
            
            <h4>Segurança</h4>
            <ul>
                <li>Criptografia de mensagens</li>
                <li>Limite de 2 usuários por sala</li>
                <li>Proteção por senha opcional</li>
            </ul>
            
            <h4>Interface</h4>
            <ul>
                <li>5 temas visuais diferentes</li>
                <li>Bolhas de chat estilo moderno</li>
                <li>Lista de usuários em tempo real</li>
            </ul>
        """)
        
        features_layout.addWidget(features_text)
        
        tech_tab = QWidget()
        tech_layout = QVBoxLayout(tech_tab)
        
        tech_text = QTextBrowser()
        tech_text.setHtml("""
            <h3>Tecnologias Utilizadas</h3>
            
            <ul>
                <li><b>Python 3.8+</b> - Linguagem de programação principal</li>
                <li><b>PyQt5</b> - Framework para interfaces gráficas</li>
                <li><b>cryptography</b> - Biblioteca para criptografia</li>
                <li><b>Socket</b> - API para comunicação de rede</li>
                <li><b>Threading</b> - Suporte para operações assíncronas</li>
                <li><b>JSON</b> - Formato para troca de mensagens</li>
            </ul>
            
            <p>Este projeto utiliza sockets TCP para comunicação direta 
            entre os peers, e a biblioteca Fernet para criptografia simétrica
            das mensagens.</p>
        """)
        
        tech_layout.addWidget(tech_text)
        

        tabs.addTab(about_tab, "Sobre")
        tabs.addTab(features_tab, "Recursos")
        tabs.addTab(tech_tab, "Tecnologias")
        

        btn_close = QPushButton("Fechar")
        btn_close.clicked.connect(self.close)
        

        layout.addLayout(title_layout)
        layout.addWidget(tabs)
        layout.addWidget(btn_close, alignment=Qt.AlignRight)