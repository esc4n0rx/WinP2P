from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, 
    QLabel, QProgressBar, QTextBrowser, QMessageBox, QCheckBox,
    QFrame, QSpacerItem, QSizePolicy
)
from PyQt5.QtCore import Qt, QTimer, QSize, QObject
from PyQt5.QtGui import QIcon, QPixmap, QFont
import sys
import os
from utils.updater import UpdateChecker, UpdateDownloader, get_current_version, apply_update
from ui.themes import THEMES

# Objeto global para manter referências aos checkers de atualização
# Isso evita que os threads sejam destruídos enquanto ainda estão em execução
_update_checkers = []

class UpdateWindow(QMainWindow):
    def __init__(self, config, parent=None):
        super().__init__(parent)
        self.config = config
        self.parent = parent
        self.current_version = get_current_version()
        self.update_info = None
        
        self.setWindowTitle('WinP2P - Atualizações')
        self.resize(550, 450)
        self.setStyleSheet(THEMES.get(config.get('theme', 'XP'), ''))
        
        # Centralizar a janela
        if parent:
            geo = parent.geometry()
            self.setGeometry(
                geo.x() + (geo.width() - self.width()) // 2,
                geo.y() + (geo.height() - self.height()) // 2,
                self.width(), self.height()
            )
        
        self.setup_ui()
        
        # Verifica automaticamente atualizações ao iniciar
        if config.get('check_updates_at_startup', True):
            self.check_updates()
    
    def setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        main_layout = QVBoxLayout(central)
        
        # Título
        title_frame = QFrame()
        title_layout = QHBoxLayout(title_frame)
        
        title = QLabel("<h1>Atualizações do WinP2P</h1>")
        title.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        
        title_layout.addWidget(title)
        title_layout.addStretch()
        
        # Versão atual
        version_label = QLabel(f"<h3>Versão atual: v{self.current_version}</h3>")
        
        # Área de informações
        info_frame = QFrame()
        info_frame.setFrameShape(QFrame.StyledPanel)
        info_layout = QVBoxLayout(info_frame)
        
        self.status_label = QLabel("Clique em 'Verificar Atualizações' para buscar novas versões.")
        self.status_label.setWordWrap(True)
        info_layout.addWidget(self.status_label)
        
        self.release_notes = QTextBrowser()
        self.release_notes.setHidden(True)
        self.release_notes.setOpenExternalLinks(True)
        info_layout.addWidget(self.release_notes)
        
        # Barra de progresso
        self.progress_frame = QFrame()
        progress_layout = QVBoxLayout(self.progress_frame)
        
        self.progress_label = QLabel("Baixando atualização:")
        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        
        progress_layout.addWidget(self.progress_label)
        progress_layout.addWidget(self.progress_bar)
        
        self.progress_frame.setHidden(True)
        
        # Opção de verificação automática
        self.auto_check = QCheckBox("Verificar atualizações automaticamente ao iniciar")
        self.auto_check.setChecked(self.config.get('check_updates_at_startup', True))
        self.auto_check.stateChanged.connect(self.toggle_auto_check)
        
        # Botões
        btn_layout = QHBoxLayout()
        
        self.btn_check = QPushButton("Verificar Atualizações")
        self.btn_check.setMinimumWidth(150)
        self.btn_check.clicked.connect(self.check_updates)
        
        self.btn_download = QPushButton("Baixar e Instalar")
        self.btn_download.setMinimumWidth(150)
        self.btn_download.setHidden(True)
        self.btn_download.clicked.connect(self.download_update)
        
        self.btn_close = QPushButton("Fechar")
        self.btn_close.clicked.connect(self.close)
        
        btn_layout.addWidget(self.btn_check)
        btn_layout.addWidget(self.btn_download)
        btn_layout.addStretch()
        btn_layout.addWidget(self.btn_close)
        
        # Adicionar todos os componentes ao layout principal
        main_layout.addWidget(title_frame)
        main_layout.addWidget(version_label)
        main_layout.addWidget(info_frame, 1)
        main_layout.addWidget(self.progress_frame)
        main_layout.addWidget(self.auto_check)
        main_layout.addSpacing(20)
        main_layout.addLayout(btn_layout)
        
        # Preparar o checker e downloader
        self.checker = None
        self.downloader = None
    
    def toggle_auto_check(self, state):
        """Atualiza a configuração de verificação automática"""
        self.config['check_updates_at_startup'] = (state == Qt.Checked)
        
        try:
            import json
            with open('config.json', 'w') as f:
                json.dump(self.config, f, indent=4)
        except Exception as e:
            print(f"Erro ao salvar configuração: {e}")
    
    def check_updates(self):
        """Verifica se há atualizações disponíveis"""
        self.status_label.setText("Verificando atualizações disponíveis...")
        self.btn_check.setEnabled(False)
        self.release_notes.setHidden(True)
        self.btn_download.setHidden(True)
        
        # Criar e iniciar a thread de verificação
        self.checker = UpdateChecker(self.current_version)
        self.checker.update_available.connect(self.on_update_available)
        self.checker.check_complete.connect(self.on_check_complete)
        self.checker.error.connect(self.on_check_error)
        
        # Manter uma referência global para evitar que o thread seja coletado pelo GC
        global _update_checkers
        _update_checkers.append(self.checker)
        
        self.checker.start()
    
    def on_update_available(self, update_info):
        """Callback quando uma atualização está disponível"""
        self.update_info = update_info
        version = update_info.get('version')
        size = update_info.get('size', 'Desconhecido')
        
        self.status_label.setText(
            f"<b>Nova versão disponível: v{version}</b><br/>"
            f"Tamanho do download: {size}"
        )
        
        # Exibir notas de release
        notes = update_info.get('release_notes', 'Sem informações disponíveis.')
        self.release_notes.setHtml(f"<h3>O que há de novo na versão {version}:</h3>{notes}")
        self.release_notes.setHidden(False)
        
        # Mostrar botão de download
        self.btn_download.setHidden(False)
    
    def on_check_complete(self, updates_available):
        """Callback quando a verificação é concluída"""
        self.btn_check.setEnabled(True)
        
        # Limpar a referência ao checker concluído
        if self.checker in _update_checkers:
            _update_checkers.remove(self.checker)
        
        if not updates_available:
            self.status_label.setText("Você já está usando a versão mais recente.")
            
            # Adicionar informações para depuração
            if self.current_version:
                self.status_label.setText(
                    f"Você já está usando a versão mais recente (v{self.current_version})."
                )
    
    def on_check_error(self, error_msg):
        """Callback quando ocorre um erro na verificação"""
        self.btn_check.setEnabled(True)
        self.status_label.setText(f"<span style='color:red'>Erro ao verificar: {error_msg}</span>")
        
        # Limpar a referência ao checker com erro
        if self.checker in _update_checkers:
            _update_checkers.remove(self.checker)
    
    def download_update(self):
        """Inicia o download e instalação da atualização"""
        if not self.update_info:
            return
        
        reply = QMessageBox.question(
            self, 'Confirmar Atualização',
            f"O WinP2P será fechado e atualizado para a versão {self.update_info.get('version')}.\n"
            f"Deseja continuar?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        # Preparar UI para download
        self.btn_check.setEnabled(False)
        self.btn_download.setEnabled(False)
        self.btn_close.setEnabled(False)
        self.progress_frame.setHidden(False)
        self.progress_bar.setValue(0)
        
        # Iniciar download
        self.downloader = UpdateDownloader(
            self.update_info.get('download_url'),
            self.current_version,
            self.update_info.get('version')
        )
        self.downloader.progress.connect(self.update_progress)
        self.downloader.finished.connect(self.on_download_finished)
        self.downloader.error.connect(self.on_download_error)
        
        # Manter uma referência global para evitar que o thread seja coletado pelo GC
        global _update_checkers
        _update_checkers.append(self.downloader)
        
        self.downloader.start()
    
    def update_progress(self, percent):
        """Atualiza a barra de progresso"""
        self.progress_bar.setValue(percent)
    
    def on_download_finished(self, success, script_path):
        """Callback quando o download é concluído"""
        # Limpar a referência ao downloader concluído
        if self.downloader in _update_checkers:
            _update_checkers.remove(self.downloader)
            
        if success:
            QMessageBox.information(
                self, 'Download Concluído',
                "A atualização foi baixada com sucesso. O aplicativo será reiniciado para aplicar as mudanças."
            )
            # Aplicar a atualização
            apply_update(script_path)
        else:
            self.btn_check.setEnabled(True)
            self.btn_download.setEnabled(True)
            self.btn_close.setEnabled(True)
            self.progress_frame.setHidden(True)
            QMessageBox.warning(
                self, 'Falha na Atualização',
                "Houve um problema ao finalizar a atualização."
            )
    
    def on_download_error(self, error_msg):
        """Callback quando ocorre um erro no download"""
        # Limpar a referência ao downloader com erro
        if self.downloader in _update_checkers:
            _update_checkers.remove(self.downloader)
            
        self.btn_check.setEnabled(True)
        self.btn_download.setEnabled(True)
        self.btn_close.setEnabled(True)
        self.progress_frame.setHidden(True)
        QMessageBox.critical(
            self, 'Erro',
            f"Erro no download: {error_msg}"
        )
    
    def closeEvent(self, event):
        """Garante que os threads sejam encerrados corretamente ao fechar a janela"""
        if self.checker and self.checker.isRunning():
            self.checker.quit()
            self.checker.wait()
            
        if self.downloader and self.downloader.isRunning():
            self.downloader.quit()
            self.downloader.wait()
            
        event.accept()
    
    @staticmethod
    def check_for_updates_on_startup(parent, config):
        """Método estático para verificar atualizações silenciosamente na inicialização"""
        if not config.get('check_updates_at_startup', True):
            return
        
        current_version = get_current_version()
        checker = UpdateChecker(current_version)
        
        # Manter uma referência global para o checker
        global _update_checkers
        _update_checkers.append(checker)
        
        def on_update_found(update_info):
            version = update_info.get('version')
            
            reply = QMessageBox.question(
                parent, 'Nova Versão Disponível',
                f"Uma nova versão do WinP2P está disponível (v{version}).\n"
                f"Deseja abrir o gerenciador de atualizações?",
                QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
            )
            
            # Limpar a referência ao checker
            if checker in _update_checkers:
                _update_checkers.remove(checker)
            
            if reply == QMessageBox.Yes:
                update_window = UpdateWindow(config, parent)
                update_window.update_info = update_info
                update_window.on_update_available(update_info)
                update_window.show()
        
        def on_check_complete(updates_available):
            # Limpar a referência quando a verificação estiver concluída
            if checker in _update_checkers:
                _update_checkers.remove(checker)
        
        def on_check_error(error_msg):
            # Limpar a referência em caso de erro
            if checker in _update_checkers:
                _update_checkers.remove(checker)
            print(f"Erro ao verificar atualizações: {error_msg}")
                
        # Conectar sinais
        checker.update_available.connect(on_update_found)
        checker.check_complete.connect(on_check_complete)
        checker.error.connect(on_check_error)
        checker.start()