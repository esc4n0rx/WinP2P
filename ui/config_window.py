from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QFormLayout, QLineEdit, QComboBox, 
    QPushButton, QCheckBox, QSpinBox, QLabel, QVBoxLayout, 
    QHBoxLayout, QGroupBox, QColorDialog
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QPixmap, QFont
import json
from ui.themes import THEMES
import os

class ConfigWindow(QMainWindow):
    def __init__(self, config):
        super().__init__()
        self.config = config
        self.setWindowTitle('Configurações')
        self.resize(400, 500)

        # Aplicar tema atual às configurações
        if 'theme' in config:
            self.setStyleSheet(THEMES.get(config['theme'], ''))

        # Widget central e layout principal
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        
        # Título
        title = QLabel("Configurações do Chat")
        title.setAlignment(Qt.AlignCenter)
        font = QFont()
        font.setPointSize(16)
        font.setBold(True)
        title.setFont(font)
        main_layout.addWidget(title)
        
        # Grupo: Perfil do usuário
        profile_group = QGroupBox("Perfil do Usuário")
        profile_layout = QFormLayout(profile_group)
        
        self.username = QLineEdit(config.get('username', 'User'))
        self.avatar_color = QPushButton("Escolher Cor")
        self.avatar_color.clicked.connect(self.choose_color)
        
        # Define a cor do avatar (cor padrão se não existir)
        self.current_color = config.get('avatar_color', '#1E88E5')
        self.avatar_color.setStyleSheet(f"background-color: {self.current_color}")
        
        profile_layout.addRow('Nome de Usuário:', self.username)
        profile_layout.addRow('Cor do Avatar:', self.avatar_color)
        
        # Grupo: Rede
        network_group = QGroupBox("Configurações de Rede")
        network_layout = QFormLayout(network_group)
        
        self.port = QSpinBox()
        self.port.setRange(1024, 65535)
        self.port.setValue(config.get('port', 5000))
        
        self.timeout = QSpinBox()
        self.timeout.setRange(5, 120)
        self.timeout.setValue(config.get('timeout', 30))
        self.timeout.setSuffix(" segundos")
        
        network_layout.addRow('Porta:', self.port)
        network_layout.addRow('Timeout de Conexão:', self.timeout)
        
        # Grupo: Interface
        ui_group = QGroupBox("Interface")
        ui_layout = QFormLayout(ui_group)
        
        self.theme = QComboBox()
        self.theme.addItems(THEMES.keys())
        self.theme.setCurrentText(config.get('theme', 'XP'))
        
        self.font_size = QSpinBox()
        self.font_size.setRange(8, 18)
        self.font_size.setValue(config.get('font_size', 10))
        self.font_size.setSuffix(" pt")
        
        self.show_timestamps = QCheckBox()
        self.show_timestamps.setChecked(config.get('show_timestamps', True))
        
        self.sound_effects = QCheckBox()
        self.sound_effects.setChecked(config.get('sound_effects', True))
        
        ui_layout.addRow('Tema:', self.theme)
        ui_layout.addRow('Tamanho da Fonte:', self.font_size)
        ui_layout.addRow('Mostrar Horários:', self.show_timestamps)
        ui_layout.addRow('Efeitos Sonoros:', self.sound_effects)
        
        # Grupo: Segurança
        security_group = QGroupBox("Segurança")
        security_layout = QFormLayout(security_group)
        
        self.encryption = QCheckBox()
        self.encryption.setChecked(config.get('encryption', True))
        
        self.room_password = QLineEdit(config.get('room_password', ''))
        self.room_password.setPlaceholderText("Opcional")
        self.room_password.setEchoMode(QLineEdit.Password)
        
        security_layout.addRow('Criptografia:', self.encryption)
        security_layout.addRow('Senha da Sala:', self.room_password)
        
        # Botões de ação
        btn_layout = QHBoxLayout()
        
        self.btn_reset = QPushButton("Restaurar Padrões")
        self.btn_save = QPushButton("Salvar")
        self.btn_cancel = QPushButton("Cancelar")
        
        self.btn_reset.clicked.connect(self.reset_defaults)
        self.btn_save.clicked.connect(self.save)
        self.btn_cancel.clicked.connect(self.close)
        
        btn_layout.addWidget(self.btn_reset)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_cancel)
        btn_layout.addWidget(self.btn_save)
        
        # Adicionar todos os grupos ao layout principal
        main_layout.addWidget(profile_group)
        main_layout.addWidget(network_group)
        main_layout.addWidget(ui_group)
        main_layout.addWidget(security_group)
        main_layout.addLayout(btn_layout)
        
        # Conectar sinal do tema para atualização ao vivo
        self.theme.currentTextChanged.connect(self.preview_theme)
    
    def preview_theme(self, theme_name):
        """Aplica o tema selecionado em tempo real para visualização"""
        self.setStyleSheet(THEMES.get(theme_name, ''))
    
    def choose_color(self):
        """Abre o seletor de cores para o avatar"""
        color = QColorDialog.getColor(initial=Qt.blue, parent=self)
        if color.isValid():
            self.current_color = color.name()
            self.avatar_color.setStyleSheet(f"background-color: {self.current_color}")
    
    def reset_defaults(self):
        """Restaurar configurações padrão"""
        default_config = {
            'username': 'User',
            'port': 5000,
            'theme': 'XP',
            'font_size': 10,
            'show_timestamps': True,
            'sound_effects': True,
            'encryption': True,
            'timeout': 30,
            'avatar_color': '#1E88E5',
            'room_password': ''
        }
        
        # Atualizar widgets
        self.username.setText(default_config['username'])
        self.port.setValue(default_config['port'])
        self.theme.setCurrentText(default_config['theme'])
        self.font_size.setValue(default_config['font_size'])
        self.show_timestamps.setChecked(default_config['show_timestamps'])
        self.sound_effects.setChecked(default_config['sound_effects'])
        self.encryption.setChecked(default_config['encryption'])
        self.timeout.setValue(default_config['timeout'])
        self.current_color = default_config['avatar_color']
        self.avatar_color.setStyleSheet(f"background-color: {self.current_color}")
        self.room_password.setText(default_config['room_password'])
        
        # Aplicar tema padrão
        self.setStyleSheet(THEMES.get(default_config['theme'], ''))
    
    def save(self):
        """Salvar configurações no arquivo config.json"""
        # Atualizar objeto de configuração
        self.config['username'] = self.username.text().strip() or 'User'
        self.config['port'] = self.port.value()
        self.config['theme'] = self.theme.currentText()
        self.config['font_size'] = self.font_size.value()
        self.config['show_timestamps'] = self.show_timestamps.isChecked()
        self.config['sound_effects'] = self.sound_effects.isChecked()
        self.config['encryption'] = self.encryption.isChecked()
        self.config['timeout'] = self.timeout.value()
        self.config['avatar_color'] = self.current_color
        self.config['room_password'] = self.room_password.text()
        
        # Salvar no arquivo
        try:
            with open('config.json', 'w') as f:
                json.dump(self.config, f, indent=4)
            self.close()
        except Exception as e:
            print(f"Erro ao salvar configurações: {e}")
            # Aqui poderia ser exibido um diálogo de erro