from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSplitter,
    QTextEdit, QLineEdit, QPushButton, QLabel, QFrame, QScrollArea,
    QInputDialog, QMessageBox, QApplication, QListWidget, QListWidgetItem
)
from PyQt5.QtCore import Qt, QTimer, pyqtSignal
from PyQt5.QtGui import QColor, QIcon, QPixmap, QFont
from network.server import Server
from network.client import Client
from utils.code_generator import generate_room_code, decode_room_code
from utils.crypto import encrypt_message, decrypt_message
from ui.themes import THEMES
import socket
import time
import json

class ChatBubble(QFrame):
    """Widget personalizado para bolhas de chat"""
    def __init__(self, username, message, is_own=False, parent=None):
        super().__init__(parent)
        self.setFrameShape(QFrame.StyledPanel)
        self.setFrameShadow(QFrame.Raised)
        
        # Estilo base para todas as bolhas
        self.setStyleSheet("""
            QFrame {
                border-radius: 10px;
                padding: 5px;
                margin: 5px;
            }
        """)
        
        # Layout da bolha
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 5, 10, 5)
        
        # Nome do usuário (em negrito)
        name_label = QLabel(f"<b>{username}</b>")
        
        # Texto da mensagem
        msg_label = QLabel(message)
        msg_label.setWordWrap(True)
        
        # Timestamp
        time_label = QLabel(time.strftime("%H:%M"))
        time_label.setStyleSheet("color: #666; font-size: 8pt;")
        
        # Adicionar widgets ao layout
        layout.addWidget(name_label)
        layout.addWidget(msg_label)
        layout.addWidget(time_label, alignment=Qt.AlignRight)
        
        # Definir estilos diferentes para mensagens próprias vs. outros
        if is_own:
            self.setStyleSheet("""
                QFrame {
                    background-color: #DCF8C6;
                    border-radius: 10px;
                    margin-left: 50px;
                    margin-right: 10px;
                }
            """)
        else:
            self.setStyleSheet("""
                QFrame {
                    background-color: #FFFFFF;
                    border-radius: 10px;
                    margin-left: 10px;
                    margin-right: 50px;
                }
            """)


class UserListItem(QWidget):
    """Widget personalizado para itens da lista de usuários"""
    def __init__(self, username, status="online", parent=None):
        super().__init__(parent)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Status indicator (circle)
        self.status_indicator = QLabel()
        self.status_indicator.setFixedSize(10, 10)
        self.set_status(status)
        
        # Username
        self.username_label = QLabel(username)
        
        layout.addWidget(self.status_indicator)
        layout.addWidget(self.username_label)
        layout.addStretch()
    
    def set_status(self, status):
        """Define o indicador de status (círculo colorido)"""
        color = "#44c767"  # verde/online por padrão
        if status == "typing":
            color = "#5cabff"  # azul
        elif status == "away":
            color = "#ffbe5c"  # laranja
        elif status == "offline":
            color = "#cccccc"  # cinza
            
        self.status_indicator.setStyleSheet(f"""
            background-color: {color};
            border-radius: 5px;
        """)


class MainWindow(QMainWindow):
    typing_signal = pyqtSignal(bool)
    
    def __init__(self, config, new_room=False):
        super().__init__()
        self.config = config
        self.setWindowTitle('WinP2P - Chat P2P')
        self.resize(800, 600)
        self.setStyleSheet(THEMES.get(config.get('theme', 'XP'), ''))
        
        # Estado de digitação e timer
        self.is_typing = False
        self.typing_timer = QTimer()
        self.typing_timer.timeout.connect(self.stop_typing)
        self.typing_signal.connect(self.send_typing_status)
        
        # Lista de usuários conectados (incluindo a si mesmo)
        self.users = {config['username']: "online"}
        self.max_users = 2  # Limitar a 2 usuários (peer-to-peer)
        self.encrypted = True
        
        # Configurar layout principal
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QHBoxLayout(central)
        
        # Área de lista de usuários (lado esquerdo)
        users_frame = QFrame()
        users_frame.setFrameShape(QFrame.StyledPanel)
        users_layout = QVBoxLayout(users_frame)
        
        users_header = QLabel("<h3>Usuários</h3>")
        self.users_list = QListWidget()
        self.update_users_list()
        
        room_info = QLabel()
        if new_room:
            room_info.setText("<b>Sua Sala</b>")
        else:
            room_info.setText("<b>Sala de outro usuário</b>")
        
        users_layout.addWidget(users_header)
        users_layout.addWidget(self.users_list)
        users_layout.addWidget(room_info)
        
        # Status da conexão
        self.conn_status = QLabel("Conectado: Não")
        self.encryption_status = QLabel("Criptografia: Ativada")
        
        users_layout.addWidget(self.conn_status)
        users_layout.addWidget(self.encryption_status)
        
        # Área do chat (lado direito)
        chat_frame = QFrame()
        chat_frame.setFrameShape(QFrame.StyledPanel)
        chat_layout = QVBoxLayout(chat_frame)
        
        # Área de mensagens com rolagem
        self.chat_area = QScrollArea()
        self.chat_area.setWidgetResizable(True)
        self.chat_widget = QWidget()
        self.chat_layout = QVBoxLayout(self.chat_widget)
        self.chat_layout.setAlignment(Qt.AlignTop)
        self.chat_layout.addStretch()
        self.chat_area.setWidget(self.chat_widget)
        
        # Área de entrada
        input_frame = QFrame()
        input_layout = QHBoxLayout(input_frame)
        
        self.typing_label = QLabel("")
        self.msg_input = QLineEdit()
        self.msg_input.setPlaceholderText("Digite sua mensagem")
        self.msg_input.textChanged.connect(self.on_text_changed)
        self.send_btn = QPushButton("Enviar")
        self.send_btn.clicked.connect(self.send_message)
        self.msg_input.returnPressed.connect(self.send_message)
        
        input_layout.addWidget(self.msg_input)
        input_layout.addWidget(self.send_btn)
        
        chat_layout.addWidget(self.chat_area)
        chat_layout.addWidget(self.typing_label)
        chat_layout.addWidget(input_frame)
        
        # Adicionar os frames ao layout principal com splitter
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(users_frame)
        splitter.addWidget(chat_frame)
        splitter.setSizes([200, 600])
        main_layout.addWidget(splitter)
        
        # Elementos de rede
        self.server = None
        self.client = None
        self.peer_connected = False
        
        # Iniciar servidor ou cliente
        if new_room:
            self.start_server()
        else:
            self.join_room()
            
        # Timer para verificar conexão periodicamente
        self.conn_timer = QTimer()
        self.conn_timer.timeout.connect(self.check_connection)
        self.conn_timer.start(5000)  # A cada 5 segundos
    
    def start_server(self):
        """Inicia o servidor e gera código da sala"""
        port = self.config['port']
        self.server = Server('0.0.0.0', port, max_clients=1)  # Limitar a 1 cliente
        self.server.message_received.connect(self.process_message)
        self.server.client_connected.connect(self.on_client_connected)
        self.server.client_disconnected.connect(self.on_client_disconnected)
        self.server.start()

        # Gerar e exibir código da sala
        local_ip = socket.gethostbyname(socket.gethostname())
        room_code = generate_room_code(local_ip, port)

        # Copiar para a área de transferência
        clipboard = QApplication.clipboard()
        clipboard.setText(room_code)

        QMessageBox.information(
            self, 'Código da Sala',
            f'Código da Sala:\n{room_code}\n\n(copiado para a área de transferência)'
        )
    
    def join_room(self):
        """Conecta a uma sala existente"""
        code, ok = QInputDialog.getText(self, 'Entrar na Sala', 'Insira o Código da Sala:')
        if ok:
            try:
                ip, port = decode_room_code(code)
                self.client = Client(ip, port)
                self.client.message_received.connect(self.process_message)
                self.client.connected.connect(self.on_connected)
                self.client.disconnected.connect(self.on_disconnected)
                self.client.start()
                
                # Quando conectado, enviar informações do usuário
                self.send_system_message("user_join", {"username": self.config['username']})
                
            except Exception as e:
                QMessageBox.critical(self, 'Erro', f"Falha ao conectar: {str(e)}")
    
    def check_connection(self):
        """Verifica periodicamente o status da conexão"""
        if self.server and self.server.has_clients():
            self.peer_connected = True
            self.conn_status.setText("Conectado: Sim")
        elif self.client and self.client.is_connected():
            self.peer_connected = True
            self.conn_status.setText("Conectado: Sim")
        else:
            self.peer_connected = False
            self.conn_status.setText("Conectado: Não")
            # Limpar status de digitação se não houver conexão
            self.typing_label.setText("")
    
    def on_client_connected(self, client_info):
        """Chamado quando um cliente se conecta ao servidor"""
        self.peer_connected = True
        self.conn_status.setText("Conectado: Sim")
    
    def on_client_disconnected(self):
        """Chamado quando um cliente se desconecta do servidor"""
        self.peer_connected = False
        self.conn_status.setText("Conectado: Não")
        self.add_system_message("O outro usuário desconectou")
        
        # Remover usuário da lista e atualizar
        for username in list(self.users.keys()):
            if username != self.config['username']:
                self.users.pop(username, None)
        self.update_users_list()
    
    def on_connected(self):
        """Chamado quando cliente se conecta com sucesso"""
        self.peer_connected = True
        self.conn_status.setText("Conectado: Sim")
    
    def on_disconnected(self):
        """Chamado quando cliente é desconectado"""
        self.peer_connected = False
        self.conn_status.setText("Conectado: Não")
        self.add_system_message("Desconectado da sala")
        
        # Remover usuário da lista e atualizar
        for username in list(self.users.keys()):
            if username != self.config['username']:
                self.users.pop(username, None)
        self.update_users_list()
    
    def on_text_changed(self):
        """Detectar quando o usuário está digitando"""
        if not self.is_typing:
            self.is_typing = True
            self.typing_signal.emit(True)
        
        # Reiniciar timer a cada alteração do texto
        self.typing_timer.start(2000)  # 2 segundos sem digitar = não está mais digitando
    
    def stop_typing(self):
        """Parar o status de digitação após período de inatividade"""
        self.is_typing = False
        self.typing_signal.emit(False)
        self.typing_timer.stop()
    
    def send_typing_status(self, is_typing):
        """Envia status de digitação para o outro usuário"""
        if self.peer_connected:
            status = "typing" if is_typing else "online"
            self.send_system_message("typing_status", {
                "username": self.config['username'],
                "status": status
            })
    
    def process_message(self, data):
        """Processa mensagens recebidas (chat ou sistema)"""
        try:
            # Tentar decodificar como JSON primeiro (mensagens do sistema)
            msg_obj = json.loads(data)
            
            # Verificar tipo de mensagem do sistema
            if msg_obj.get("type") == "chat":
                # Mensagem normal de chat, possivelmente criptografada
                content = msg_obj.get("content", "")
                if self.encrypted and "encrypted" in msg_obj:
                    content = decrypt_message(content)
                
                self.display_message(msg_obj.get("username", "Anônimo"), content)
                
            elif msg_obj.get("type") == "user_join":
                # Novo usuário entrou
                username = msg_obj.get("data", {}).get("username", "Anônimo")
                if username not in self.users and len(self.users) < self.max_users:
                    self.users[username] = "online"
                    self.update_users_list()
                    self.add_system_message(f"{username} entrou na sala")
                    
                    # Enviar lista atual de usuários para sincronizar
                    self.send_system_message("user_list", {"users": self.users})
                    
                elif len(self.users) >= self.max_users:
                    # Sala cheia, rejeitar conexão
                    self.send_system_message("room_full", {})
            
            elif msg_obj.get("type") == "user_list":
                # Atualizar lista de usuários
                user_list = msg_obj.get("data", {}).get("users", {})
                self.users.update(user_list)
                self.update_users_list()
            
            elif msg_obj.get("type") == "room_full":
                # Sala está cheia
                QMessageBox.warning(self, "Sala Cheia", 
                                    "Esta sala já atingiu o limite de 2 usuários.")
                if self.client:
                    self.client.disconnect()
            
            elif msg_obj.get("type") == "typing_status":
                # Atualizar status de digitação
                username = msg_obj.get("data", {}).get("username", "")
                status = msg_obj.get("data", {}).get("status", "online")
                
                if username in self.users:
                    self.users[username] = status
                    self.update_users_list()
                    
                    if status == "typing" and username != self.config['username']:
                        self.typing_label.setText(f"{username} está digitando...")
                    else:
                        self.typing_label.setText("")
                        
        except json.JSONDecodeError:
            # Modo de compatibilidade: mensagem formatada no estilo antigo
            parts = data.split(": ", 1)
            if len(parts) == 2:
                username, message = parts
                self.display_message(username, message)
            else:
                self.display_message("Anônimo", data)
    
    def send_system_message(self, msg_type, data=None):
        """Envia mensagem de sistema com formato JSON"""
        if data is None:
            data = {}
            
        message = {
            "type": msg_type,
            "data": data
        }
        
        payload = json.dumps(message)
        if self.client:
            self.client.send(payload)
        elif self.server:
            self.server.broadcast(payload)
    
    def send_message(self):
        """Envia mensagem de chat"""
        text = self.msg_input.text().strip()
        if not text:
            return
            
        # Parar indicador de digitação
        self.stop_typing()
        
        # Criar objeto da mensagem
        message = {
            "type": "chat",
            "username": self.config['username'],
            "content": text
        }
        
        # Criptografar se necessário
        if self.encrypted:
            message["content"] = encrypt_message(text)
            message["encrypted"] = True
        
        # Enviar e exibir
        payload = json.dumps(message)
        if self.client:
            self.client.send(payload)
        elif self.server:
            self.server.broadcast(payload)
            
        # Sempre mostrar mensagem decriptografada localmente
        self.display_message(self.config['username'], text, is_own=True)
        self.msg_input.clear()
    
    def display_message(self, username, message, is_own=False):
        """Exibe mensagem de chat em bolhas"""
        bubble = ChatBubble(username, message, is_own)
        
        # Garantir que haja pelo menos um espaço antes da bolha
        spacer = QWidget()
        spacer.setFixedHeight(5)
        self.chat_layout.addWidget(spacer)
        
        # Adicionar bolha de chat
        self.chat_layout.addWidget(bubble)
        
        # Rolar para o final
        self.chat_area.verticalScrollBar().setValue(
            self.chat_area.verticalScrollBar().maximum()
        )
    
    def add_system_message(self, message):
        """Adiciona mensagem do sistema (não bolha)"""
        label = QLabel(f"<i>{message}</i>")
        label.setAlignment(Qt.AlignCenter)
        label.setStyleSheet("color: #666;")
        self.chat_layout.addWidget(label)
    
    def update_users_list(self):
        """Atualiza a lista de usuários na interface"""
        self.users_list.clear()
        
        for username, status in self.users.items():
            item = QListWidgetItem()
            user_widget = UserListItem(username, status)
            item.setSizeHint(user_widget.sizeHint())
            
            self.users_list.addItem(item)
            self.users_list.setItemWidget(item, user_widget)
    
    def closeEvent(self, event):
        """Limpar recursos ao fechar a janela"""
        if self.client:
            self.client.disconnect()
        if self.server:
            self.server.stop()
        event.accept()