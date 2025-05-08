from PyQt5.QtWidgets import (
    QMainWindow, QLabel, QVBoxLayout, QWidget, 
    QTabWidget, QTextBrowser, QPushButton, QHBoxLayout,
    QFrame, QScrollArea, QGridLayout, QSizePolicy, QSpacerItem
)
from PyQt5.QtCore import Qt, QSize, QUrl
from PyQt5.QtGui import QIcon, QPixmap, QFont, QDesktopServices

class FeatureCard(QFrame):
    """Widget personalizado para exibir recursos em cartões"""
    def __init__(self, icon_path, title, description, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        self.setMinimumHeight(120)
        self.setMinimumWidth(200)
        
        layout = QVBoxLayout(self)
        
        # Ícone e título
        header_layout = QHBoxLayout()
        
        icon = QLabel()
        if icon_path:
            pixmap = QPixmap(icon_path)
            if not pixmap.isNull():
                icon.setPixmap(pixmap.scaled(24, 24, Qt.KeepAspectRatio, Qt.SmoothTransformation))
            else:
                # Criar um ícone colorido simples
                pixmap = QPixmap(24, 24)
                pixmap.fill(Qt.transparent)
                icon.setPixmap(pixmap)
        else:
            # Criar um ícone colorido simples
            pixmap = QPixmap(24, 24)
            pixmap.fill(Qt.transparent)
            icon.setPixmap(pixmap)
            
        title_label = QLabel(f"<b>{title}</b>")
        font = QFont()
        font.setPointSize(10)
        title_label.setFont(font)
        
        header_layout.addWidget(icon)
        header_layout.addWidget(title_label)
        header_layout.addStretch()
        
        # Descrição
        desc_label = QLabel(description)
        desc_label.setWordWrap(True)
        
        layout.addLayout(header_layout)
        layout.addWidget(desc_label)
        layout.addStretch()
        
        # Estilo
        self.setStyleSheet("""
            FeatureCard {
                background-color: rgba(255, 255, 255, 40);
                border-radius: 8px;
                margin: 4px;
                padding: 8px;
            }
            FeatureCard:hover {
                background-color: rgba(255, 255, 255, 80);
            }
        """)

class AboutWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Sobre o WinP2P Chat')
        self.resize(640, 520)
        
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        
        # Cabeçalho
        header_frame = QFrame()
        header_layout = QHBoxLayout(header_frame)
        
        logo = QLabel()
        logo_pixel = QPixmap(80, 80)
        logo_pixel.fill(Qt.transparent)
        logo.setPixmap(logo_pixel)
        
        title_frame = QFrame()
        title_layout = QVBoxLayout(title_frame)
        title_layout.setContentsMargins(0, 0, 0, 0)
        title_layout.setSpacing(5)
        
        app_title = QLabel('<h1>WinP2P</h1>')
        app_version = QLabel('<h3>Versão 0.3.0</h3>')
        app_tagline = QLabel('<i>Comunicação segura com nostalgia visual</i>')
        
        title_layout.addWidget(app_title)
        title_layout.addWidget(app_version)
        title_layout.addWidget(app_tagline)
        
        header_layout.addWidget(logo)
        header_layout.addWidget(title_frame)
        header_layout.addStretch()
        
        # Botões de ação no cabeçalho
        btn_layout = QVBoxLayout()
        btn_layout.setSpacing(8)
        
        btn_website = QPushButton("Visitar Website")
        btn_website.setMinimumWidth(150)
        btn_website.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/esc4n0rx/WinP2P")))
        
        btn_report = QPushButton("Reportar Problema")
        btn_report.setMinimumWidth(150)
        btn_report.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://github.com/esc4n0rx/WinP2P/issues")))
        
        btn_layout.addWidget(btn_website)
        btn_layout.addWidget(btn_report)
        btn_layout.addStretch()
        
        header_layout.addLayout(btn_layout)
        
        # Tabs de conteúdo
        tabs = QTabWidget()
        
        # Tab Sobre
        about_tab = QScrollArea()
        about_tab.setWidgetResizable(True)
        about_container = QWidget()
        about_layout = QVBoxLayout(about_container)
        
        about_text = QTextBrowser()
        about_text.setOpenExternalLinks(True)
        about_text.setHtml("""
            <h2>Bem-vindo ao WinP2P v0.3.0!</h2>
            
            <p>WinP2P é um aplicativo de chat ponto-a-ponto seguro que combina 
            interfaces inspiradas em designs clássicos de sistemas operacionais com 
            tecnologias modernas de segurança e comunicação.</p>
            
            <p>Esta versão inclui o inovador <b>Sistema de Atualizações Automáticas</b>, 
            permitindo que você mantenha seu aplicativo sempre atualizado com as últimas 
            funcionalidades e correções de segurança.</p>
            
            <h3>Por que escolher o WinP2P?</h3>
            
            <p>Desenvolvido em Python e PyQt5, este aplicativo oferece:</p>
            <ul>
                <li><b>Comunicação direta entre peers (P2P)</b> - Sem servidores intermediários</li>
                <li><b>Criptografia de ponta-a-ponta</b> - Suas mensagens permanecem privadas</li>
                <li><b>Temas nostálgicos e modernos</b> - Escolha entre 5 estilos visuais diferentes</li>
                <li><b>Status de usuário em tempo real</b> - Saiba quando alguém está digitando</li>
                <li><b>Salas privadas</b> - Limite de 2 usuários para conversas verdadeiramente privadas</li>
                <li><b>Atualizações automáticas</b> - Mantenha-se sempre com a versão mais recente</li>
            </ul>
            
            <h3>Nossa Filosofia</h3>
            
            <p>Criado para compartilhar a nostalgia das interfaces clássicas
            dos anos 90 e 2000, com toda a segurança e funcionalidade que se espera
            de aplicativos modernos.</p>
            
            <p>Acreditamos que comunicação segura deve ser fácil e acessível para todos,
            independente do nível técnico. Por isso, o WinP2P é projetado para ser
            simples de usar, sem comprometer a segurança.</p>
            
            <h3>Novidades na Versão 0.3.0</h3>
            
            <p>Esta versão traz melhorias significativas na interface de usuário,
            com uma janela "Sobre" completamente redesenhada, oferecendo mais informações
            sobre o aplicativo e seus recursos.</p>
            
            <p>Além disso, foram feitas otimizações internas para melhorar o desempenho
            e a estabilidade geral do aplicativo.</p>
        """)
        
        about_layout.addWidget(about_text)
        about_tab.setWidget(about_container)
        
        # Tab Recursos
        features_tab = QScrollArea()
        features_tab.setWidgetResizable(True)
        features_container = QWidget()
        features_layout = QVBoxLayout(features_container)
        
        # Cards de recursos
        features_grid = QGridLayout()
        features_grid.setSpacing(10)
        
        # Primeira linha
        cards = [
            FeatureCard(None, "Chat P2P", "Comunicação direta entre dispositivos sem servidores intermediários, garantindo maior privacidade."),
            FeatureCard(None, "Criptografia", "Todas as mensagens são criptografadas de ponta a ponta, mantendo suas conversas privadas."),
            FeatureCard(None, "Múltiplos Temas", "Escolha entre 5 temas visuais diferentes, incluindo visuais nostálgicos e modernos.")
        ]
        
        for i, card in enumerate(cards):
            features_grid.addWidget(card, 0, i)
        
        # Segunda linha
        cards = [
            FeatureCard(None, "Status em Tempo Real", "Visualize indicadores de status (online, digitando) para cada usuário."),
            FeatureCard(None, "Salas Privadas", "Limite de 2 usuários por sala, garantindo conversas verdadeiramente privadas."),
            FeatureCard(None, "Atualizações Automáticas", "Mantenha seu aplicativo sempre atualizado com as últimas funcionalidades.")
        ]
        
        for i, card in enumerate(cards):
            features_grid.addWidget(card, 1, i)
            
        features_layout.addLayout(features_grid)
        
        # Detalhes dos recursos
        details_text = QTextBrowser()
        details_text.setHtml("""
            <h3>Detalhes dos Recursos</h3>
            
            <h4>Comunicação</h4>
            <ul>
                <li>Chat ponto-a-ponto direto sem servidores intermediários</li>
                <li>Sistema de códigos de sala para fácil compartilhamento de conexão</li>
                <li>Indicadores de status (online, digitando, offline) para cada usuário</li>
                <li>Notificações de eventos de conexão e desconexão</li>
                <li>Interface moderna com bolhas de chat diferenciadas por usuário</li>
            </ul>
            
            <h4>Segurança</h4>
            <ul>
                <li>Criptografia de mensagens usando a biblioteca Fernet</li>
                <li>Comunicação direta sem armazenamento central de mensagens</li>
                <li>Limite de 2 usuários por sala para garantir conversas privadas</li>
                <li>Proteção por senha opcional para salas</li>
                <li>Codificação de salas em Base64 para compartilhamento seguro</li>
            </ul>
            
            <h4>Interface</h4>
            <ul>
                <li>5 temas visuais diferentes: Windows 95, Windows XP, Modern, Dark e Terminal Vintage</li>
                <li>Bolhas de chat estilizadas para melhor visualização das conversas</li>
                <li>Lista de usuários em tempo real com indicadores de status</li>
                <li>Configurações personalizáveis para adaptar a interface às suas preferências</li>
                <li>Design responsivo que se adapta a diferentes tamanhos de tela</li>
            </ul>
            
            <h4>Sistema de Atualizações</h4>
            <ul>
                <li>Verificação automática de novas versões disponíveis</li>
                <li>Notificações quando uma atualização estiver disponível</li>
                <li>Download e instalação automáticos com um único clique</li>
                <li>Verificação de integridade via hash SHA-256</li>
                <li>Opção para controlar a verificação automática nas configurações</li>
            </ul>
        """)
        
        features_layout.addWidget(details_text)
        features_tab.setWidget(features_container)
        
        # Tab Tecnologias
        tech_tab = QScrollArea()
        tech_tab.setWidgetResizable(True)
        tech_container = QWidget()
        tech_layout = QVBoxLayout(tech_container)
        
        tech_text = QTextBrowser()
        tech_text.setHtml("""
            <h2>Tecnologias Utilizadas</h2>
            
            <h3>Linguagens e Frameworks</h3>
            <ul>
                <li><b>Python 3.8+</b> - Linguagem de programação principal, escolhida pela sua clareza, versatilidade e extensa biblioteca padrão</li>
                <li><b>PyQt5</b> - Framework para interfaces gráficas, permitindo a criação de UIs nativas em múltiplas plataformas</li>
                <li><b>CSS</b> - Utilizado para estilização dos temas visuais através de QSS (Qt Style Sheets)</li>
            </ul>
            
            <h3>Segurança</h3>
            <ul>
                <li><b>cryptography</b> - Biblioteca Python para criptografia moderna</li>
                <li><b>Fernet</b> - Implementação de criptografia simétrica, fornecendo:
                    <ul>
                        <li>Criptografia autenticada (garante que a mensagem não foi alterada)</li>
                        <li>Uso de chaves de 128 bits</li>
                        <li>Implementação do algoritmo AES em modo CBC com PKCS7 padding</li>
                    </ul>
                </li>
                <li><b>base64</b> - Utilizado para codificação segura de informações de conexão</li>
                <li><b>hashlib</b> - Verificação de integridade via SHA-256 para atualizações</li>
            </ul>
            
            <h3>Comunicação em Rede</h3>
            <ul>
                <li><b>socket</b> - API para comunicação de rede de baixo nível</li>
                <li><b>threading</b> - Suporte para operações assíncronas, permitindo comunicação não-bloqueante</li>
                <li><b>JSON</b> - Formato para troca de mensagens e dados de configuração</li>
                <li><b>urllib</b> - Biblioteca para operações HTTP, usada no sistema de atualizações</li>
            </ul>
            
            <h3>Sistema de Atualizações</h3>
            <ul>
                <li><b>requests</b> - Cliente HTTP para verificação de atualizações disponíveis</li>
                <li><b>tempfile</b> - Gerenciamento de arquivos temporários durante atualizações</li>
                <li><b>zipfile</b> - Manipulação de arquivos compactados para pacotes de atualização</li>
                <li><b>subprocess</b> - Execução de processos externos para aplicar atualizações</li>
            </ul>
            
            <h3>Arquitetura</h3>
            <p>O WinP2P utiliza uma arquitetura híbrida Cliente-Servidor/P2P:</p>
            <ul>
                <li>Quando um usuário cria uma sala, ele age como servidor</li>
                <li>Quando um usuário se conecta a uma sala, ele age como cliente</li>
                <li>A comunicação ocorre diretamente entre os peers, sem servidores intermediários</li>
                <li>Sockets TCP são utilizados para garantir a entrega confiável das mensagens</li>
                <li>Um sistema de mensagens baseado em JSON permite a comunicação de diferentes tipos de eventos (chat, status, etc.)</li>
            </ul>
            
            <p>Esta arquitetura proporciona comunicação segura e direta entre os usuários, 
            mantendo a simplicidade do aplicativo e garantindo que as mensagens não sejam 
            armazenadas em servidores centrais.</p>
        """)
        
        tech_layout.addWidget(tech_text)
        tech_tab.setWidget(tech_container)
        
        # Tab Créditos
        credits_tab = QScrollArea()
        credits_tab.setWidgetResizable(True)
        credits_container = QWidget()
        credits_layout = QVBoxLayout(credits_container)
        
        credits_text = QTextBrowser()
        credits_text.setHtml("""
            <h2>Créditos e Agradecimentos</h2>
            
            <h3>Desenvolvedor</h3>
            <p>WinP2P foi desenvolvido por <b>esc4n0rx</b>.</p>
            
            <h3>Contribuidores</h3>
            <p>Agradecemos a todos os contribuidores que ajudaram a melhorar o WinP2P
            através de feedback, sugestões, correções de bugs e novas funcionalidades.</p>
            
            <h3>Bibliotecas e Recursos de Terceiros</h3>
            <ul>
                <li><b>Python</b> - &copy; Python Software Foundation</li>
                <li><b>PyQt5</b> - &copy; Riverbank Computing Limited</li>
                <li><b>Qt</b> - &copy; The Qt Company</li>
                <li><b>cryptography</b> - &copy; The cryptography developers</li>
            </ul>
            
            <h3>Agradecimentos Especiais</h3>
            <p>Um agradecimento especial a todos os usuários que testaram, forneceram feedback
            e apoiaram o desenvolvimento do WinP2P.</p>
            
            <h3>Inspiração Visual</h3>
            <p>Os temas visuais do WinP2P são inspirados nos designs clássicos de sistemas operacionais
            que marcaram gerações de usuários, prestando homenagem à evolução das interfaces gráficas.</p>
            
            <hr>
            
            <h3>Licença</h3>
            <p>Este projeto está licenciado sob a <b>Licença MIT</b>.</p>
            <p>Copyright &copy; 2025 WinP2P</p>
            <p>É concedida permissão, gratuitamente, a qualquer pessoa que obtenha uma cópia deste software
            e arquivos de documentação associados, para lidar com o software sem restrições, incluindo,
            sem limitação, os direitos de usar, copiar, modificar, mesclar, publicar, distribuir, sublicenciar
            e/ou vender cópias do software.</p>
        """)
        
        credits_layout.addWidget(credits_text)
        credits_tab.setWidget(credits_container)

        # Adicionar todas as tabs
        tabs.addTab(about_tab, "Sobre")
        tabs.addTab(features_tab, "Recursos")
        tabs.addTab(tech_tab, "Tecnologias")
        tabs.addTab(credits_tab, "Créditos")
        
        # Botões de ação
        action_layout = QHBoxLayout()
        
        btn_close = QPushButton("Fechar")
        btn_close.setMinimumWidth(100)
        btn_close.clicked.connect(self.close)
        
        action_layout.addStretch()
        action_layout.addWidget(btn_close)
        
        # Layout principal
        layout.addWidget(header_frame)
        layout.addWidget(tabs)
        layout.addLayout(action_layout)
        
        # Estilo personalizado para a janela
        self.setStyleSheet("""
            QTabWidget::pane {
                border: 1px solid #CCCCCC;
                border-radius: 4px;
                padding: 5px;
            }
            
            QTabBar::tab {
                padding: 8px 12px;
                margin-right: 2px;
            }
            
            QTabBar::tab:selected {
                font-weight: bold;
            }
        """)