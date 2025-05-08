import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QStyleFactory, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from ui.startup_window import StartupWindow
from ui.themes import THEMES

CONFIG_PATH = 'config.json'

def load_config():
    """Carrega configurações do arquivo ou cria padrão"""
    try:
        with open(CONFIG_PATH, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        # Configurações padrão
        default = {
            "username": "User",
            "port": 5000,
            "theme": "XP",
            "font_size": 10,
            "show_timestamps": True,
            "sound_effects": True,
            "encryption": True,
            "timeout": 30,
            "avatar_color": "#1E88E5",
            "room_password": ""
        }
        
        # Criar pasta config se não existir
        os.makedirs('config', exist_ok=True)
        
        # Salvar configurações padrão
        with open(CONFIG_PATH, 'w') as f:
            json.dump(default, f, indent=4)
            
        return default

def create_required_directories():
    """Cria diretórios necessários para a aplicação"""
    # Diretório para logs
    os.makedirs('logs', exist_ok=True)
    
    # Diretório para cache
    os.makedirs('cache', exist_ok=True)
    
    # Diretório para arquivos recebidos
    os.makedirs('received_files', exist_ok=True)

def setup_logging():
    """Configura sistema de logs"""
    import logging
    
    # Configurar logging para arquivo e console
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )
    
    # Registrar início da aplicação
    logging.info('Aplicação iniciada')
    
    return logging.getLogger('vintage_chat')

if __name__ == '__main__':
    # Configurar diretórios e logging
    create_required_directories()
    logger = setup_logging()
    
    # Carregar configurações
    config = load_config()
    logger.info(f"Configurações carregadas: {config.get('theme')} theme, porta {config.get('port')}")
    
    # Iniciar aplicação
    app = QApplication(sys.argv)
    
    # Garantir que a aplicação use estilos nativos como base
    app.setStyle(QStyleFactory.create('Fusion'))
    
    # Mostrar tela de splash (opcional)

    # splash_pixmap = QPixmap('resources/splash.png')
    # splash = QSplashScreen(splash_pixmap)
    # splash.show()

    
    # Iniciar aplicação após breve delay (simular carregamento)
    def start_app():
        startup = StartupWindow(config)
        startup.show()
        #splash.finish(startup)
        
    QTimer.singleShot(2000, start_app)  # 2 segundos de splash
    
    # Se não usar splash, inicie diretamente
    startup = StartupWindow(config)
    startup.show()
    
    # Log de encerramento ao fechar
    exit_code = app.exec_()
    logger.info(f"Aplicação encerrada com código: {exit_code}")
    sys.exit(exit_code)