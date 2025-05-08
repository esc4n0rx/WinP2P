import sys
import json
import os
from PyQt5.QtWidgets import QApplication, QStyleFactory, QSplashScreen
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from ui.startup_window import StartupWindow
from ui.themes import THEMES
from utils.updater import get_current_version

CONFIG_PATH = 'config.json'

def load_config():
    """Carrega configurações do arquivo ou cria padrão"""
    try:
        with open(CONFIG_PATH, 'r') as f:
            config = json.load(f)
            
            # Garantir que a configuração de atualizações existe
            if 'check_updates_at_startup' not in config:
                config['check_updates_at_startup'] = True
                with open(CONFIG_PATH, 'w') as f_update:
                    json.dump(config, f_update, indent=4)
                    
            return config
    except FileNotFoundError:
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
            "room_password": "",
            "check_updates_at_startup": True
        }
        
        os.makedirs('config', exist_ok=True)
        
        with open(CONFIG_PATH, 'w') as f:
            json.dump(default, f, indent=4)
            
        return default

def create_required_directories():
    """Cria diretórios necessários para a aplicação"""
    
    os.makedirs('logs', exist_ok=True)
    
    os.makedirs('cache', exist_ok=True)
    
    os.makedirs('received_files', exist_ok=True)

def setup_logging():
    """Configura sistema de logs"""
    import logging
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler('logs/app.log'),
            logging.StreamHandler()
        ]
    )
    
    logging.info('Aplicação iniciada')
    current_version = get_current_version()
    logging.info(f'Versão: {current_version}')
    
    return logging.getLogger('winp2p')

def create_version_file_if_needed():
    """Cria o arquivo version.txt se não existir"""
    version_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'version.txt')
    
    if not os.path.exists(version_path):
        with open(version_path, 'w') as f:
            f.write("0.1")

if __name__ == '__main__':
    # Criar diretórios necessários
    create_required_directories()
    
    # Criar arquivo de versão se não existir
    create_version_file_if_needed()
    
    # Configurar logging
    logger = setup_logging()
    
    # Carregar configurações
    config = load_config()
    logger.info(f"Configurações carregadas: {config.get('theme')} theme, porta {config.get('port')}")
    
    # Iniciar aplicação
    app = QApplication(sys.argv)
    app.setStyle(QStyleFactory.create('Fusion'))
    
    # Descomente para usar splash screen
    # splash_pixmap = QPixmap('resources/splash.png')
    # splash = QSplashScreen(splash_pixmap)
    # splash.show()

    # def start_app():
    #     startup = StartupWindow(config)
    #     startup.show()
    #     splash.finish(startup)
        
    # QTimer.singleShot(2000, start_app)
    
    startup = StartupWindow(config)
    startup.show()
    
    exit_code = app.exec_()
    logger.info(f"Aplicação encerrada com código: {exit_code}")
    sys.exit(exit_code)