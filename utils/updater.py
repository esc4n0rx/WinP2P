import os
import sys
import json
import tempfile
import time
import shutil
import zipfile
import subprocess
from pathlib import Path
import hashlib
import logging
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
from PyQt5.QtCore import QObject, pyqtSignal, QThread

# Configuração de logging
logger = logging.getLogger('winp2p.updater')

class UpdateChecker(QThread):
    """Thread para verificar atualizações disponíveis"""
    update_available = pyqtSignal(dict)
    check_complete = pyqtSignal(bool)
    error = pyqtSignal(str)
    
    def __init__(self, current_version, repo_owner="esc4n0rx", repo_name="WinP2P"):
        super().__init__()
        self.current_version = current_version
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.api_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/releases/latest"
    
    def run(self):
        try:
            # Criar um request com User-Agent para evitar bloqueios da API do GitHub
            request = Request(self.api_url)
            request.add_header('User-Agent', 'WinP2P Update Checker')
            
            # Obter informações sobre a release mais recente
            with urlopen(request, timeout=10) as response:
                release_info = json.loads(response.read().decode())
            
            latest_version = release_info.get('tag_name', '').lstrip('v')
            
            if self._is_newer_version(latest_version, self.current_version):
                # Encontrou uma versão mais recente
                update_info = {
                    'version': latest_version,
                    'release_notes': release_info.get('body', 'Notas de lançamento não disponíveis.'),
                    'download_url': self._get_asset_download_url(release_info),
                    'release_date': release_info.get('published_at', ''),
                    'size': self._get_asset_size(release_info)
                }
                self.update_available.emit(update_info)
                self.check_complete.emit(True)
            else:
                # Já está na versão mais recente
                self.check_complete.emit(False)
                
        except (URLError, HTTPError) as e:
            logger.error(f"Erro ao verificar atualizações: {e}")
            self.error.emit(f"Erro de conexão: {str(e)}")
        except Exception as e:
            logger.error(f"Erro inesperado na verificação: {e}")
            self.error.emit(f"Erro: {str(e)}")
    
    def _is_newer_version(self, latest, current):
        """Compara versões semânticas (major.minor.patch)"""
        try:
            latest_parts = [int(x) for x in latest.split('.')]
            current_parts = [int(x) for x in current.split('.')]
            
            # Garantir que ambas as listas tenham o mesmo tamanho
            while len(latest_parts) < 3:
                latest_parts.append(0)
            while len(current_parts) < 3:
                current_parts.append(0)
            
            # Comparar major, minor e patch
            for i in range(3):
                if latest_parts[i] > current_parts[i]:
                    return True
                elif latest_parts[i] < current_parts[i]:
                    return False
            
            return False  # Versões são iguais
            
        except (ValueError, AttributeError):
            # Se houver erro na comparação, assume que a versão remota é mais recente
            logger.warning(f"Erro ao comparar versões: {latest} vs {current}")
            return True
    
    def _get_asset_download_url(self, release_info):
        """Obtém a URL do arquivo executável da release"""
        assets = release_info.get('assets', [])
        for asset in assets:
            if asset.get('name', '').endswith('.exe') and 'WinP2P' in asset.get('name', ''):
                return asset.get('browser_download_url')
        
        # Se não encontrou o executável específico, procura por ZIP como backup
        for asset in assets:
            if asset.get('name', '').endswith('.zip'):
                return asset.get('browser_download_url')
        
        # Se não encontrou nenhum asset específico, usa a URL de download do zip do código fonte
        return release_info.get('zipball_url')
    
    def _get_asset_size(self, release_info):
        """Obtém o tamanho do arquivo para download"""
        assets = release_info.get('assets', [])
        for asset in assets:
            if asset.get('name', '').endswith('.zip') or asset.get('name', '').endswith('.exe'):
                size_bytes = asset.get('size', 0)
                # Converte para MB
                return f"{size_bytes / (1024 * 1024):.2f} MB"
        
        return "Desconhecido"


class UpdateDownloader(QThread):
    """Thread para baixar e aplicar atualizações"""
    progress = pyqtSignal(int)
    finished = pyqtSignal(bool, str)
    error = pyqtSignal(str)
    
    def __init__(self, download_url, current_version, target_version):
        super().__init__()
        self.download_url = download_url
        self.current_version = current_version
        self.target_version = target_version
        self.temp_dir = tempfile.mkdtemp(prefix="winp2p_update_")
        
    def run(self):
        try:
            # Determinar o tipo de arquivo pela URL
            is_exe_file = self.download_url.lower().endswith('.exe')
            
            # Baixar o arquivo de atualização
            if is_exe_file:
                local_filename = os.path.join(self.temp_dir, f"WinP2P.exe")
            else:
                local_filename = os.path.join(self.temp_dir, f"winp2p_update_{self.target_version}.zip")
                
            self._download_file(self.download_url, local_filename)
            
            # Verificar o download
            if not os.path.exists(local_filename) or os.path.getsize(local_filename) < 1000:
                raise Exception("Download da atualização incompleto ou corrompido")
            
            if is_exe_file:
                # Se for um .exe, não precisa extrair
                executable_path = local_filename
            else:
                # Se for um .zip, extrair o arquivo
                extract_path = os.path.join(self.temp_dir, "extracted")
                os.makedirs(extract_path, exist_ok=True)
                
                with zipfile.ZipFile(local_filename, 'r') as zip_ref:
                    zip_ref.extractall(extract_path)
                
                # Encontrar o executável dentro dos arquivos extraídos
                executable_path = self._find_executable(extract_path)
                if not executable_path:
                    raise Exception("Executável não encontrado no pacote de atualização")
            
            # Criar o script de atualização
            update_script = self._create_update_script(executable_path)
            
            # Finalizar com sucesso
            self.finished.emit(True, update_script)
            
        except Exception as e:
            logger.error(f"Erro no download da atualização: {e}")
            self._cleanup()
            self.error.emit(f"Erro na atualização: {str(e)}")
    
    def _download_file(self, url, dest_path):
        """Baixa um arquivo com atualização de progresso"""
        try:
            request = Request(url)
            request.add_header('User-Agent', 'WinP2P Updater')
            
            with urlopen(request, timeout=60) as response:
                file_size = int(response.headers.get('Content-Length', 0))
                downloaded = 0
                chunk_size = 8192
                last_percent = 0
                
                with open(dest_path, 'wb') as f:
                    while True:
                        chunk = response.read(chunk_size)
                        if not chunk:
                            break
                        
                        f.write(chunk)
                        downloaded += len(chunk)
                        
                        if file_size > 0:
                            percent = int((downloaded / file_size) * 100)
                            if percent > last_percent:
                                self.progress.emit(percent)
                                last_percent = percent
            
            self.progress.emit(100)
            
        except Exception as e:
            raise Exception(f"Falha no download: {str(e)}")
    
    def _find_executable(self, extract_path):
        """Procura pelo executável dentro dos arquivos extraídos"""
        for root, dirs, files in os.walk(extract_path):
            for file in files:
                if file.endswith('.exe') and 'WinP2P' in file:
                    return os.path.join(root, file)
        return None
    
    def _create_update_script(self, new_exe_path):
        """Cria um script batch para realizar a atualização após a aplicação fechar"""
        # Determinar o executável atual
        if getattr(sys, 'frozen', False):
            current_exe = sys.executable
        else:
            # Se estiver rodando do código fonte, simula um caminho para testes
            current_exe = os.path.abspath(os.path.join(os.getcwd(), 'WinP2P.exe'))
        
        # Criar o script de atualização
        script_path = os.path.join(self.temp_dir, "update.bat")
        
        with open(script_path, 'w') as f:
            f.write('@echo off\n')
            f.write('echo Atualizando WinP2P...\n')
            f.write(f'timeout /t 2 /nobreak > nul\n')  # Espera 2 segundos
            f.write(f'if exist "{current_exe}" (\n')
            # Tenta matar qualquer processo residual
            f.write(f'  taskkill /f /im "{os.path.basename(current_exe)}" > nul 2>&1\n')
            f.write(f'  timeout /t 1 /nobreak > nul\n')
            # Copia o novo executável
            f.write(f'  copy /y "{new_exe_path}" "{current_exe}"\n')
            # Copia pastas necessárias se existirem no pacote
            f.write(f'  if exist "{os.path.dirname(new_exe_path)}\\resources" (\n')
            f.write(f'    xcopy /e /i /y "{os.path.dirname(new_exe_path)}\\resources" "{os.path.dirname(current_exe)}\\resources"\n')
            f.write(f'  )\n')
            # Atualiza o arquivo de versão
            f.write(f'  echo {self.target_version} > "{os.path.dirname(current_exe)}\\version.txt"\n')
            f.write(f')\n')
            # Limpa arquivos temporários
            f.write(f'rmdir /s /q "{self.temp_dir}"\n')
            # Inicia a aplicação atualizada
            f.write(f'start "" "{current_exe}"\n')
            f.write('exit\n')
        
        return script_path
    
    def _cleanup(self):
        """Limpa arquivos temporários em caso de erro"""
        try:
            shutil.rmtree(self.temp_dir, ignore_errors=True)
        except:
            pass


def get_current_version():
    """Obtém a versão atual do aplicativo"""
    # Primeiro verifica se há um arquivo version.txt
    version_path = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), 'version.txt')
    
    if os.path.exists(version_path):
        try:
            with open(version_path, 'r') as f:
                version = f.read().strip()
                if version:
                    return version
        except:
            pass
    
    # Se não encontrar, usa a versão codificada
    return "0.1"


def apply_update(script_path):
    """Executa o script de atualização e fecha a aplicação atual"""
    try:
        # Inicia o script como um processo separado
        if sys.platform == 'win32':
            subprocess.Popen(['cmd', '/c', script_path], 
                             creationflags=subprocess.CREATE_NEW_CONSOLE,
                             close_fds=True)
        else:
            # Em outros sistemas, seria necessária uma abordagem diferente
            subprocess.Popen(['bash', script_path])
        
        # Fecha a aplicação atual
        time.sleep(1)  # Pequena pausa para garantir que o processo foi iniciado
        sys.exit(0)
    except Exception as e:
        logger.error(f"Erro ao aplicar atualização: {e}")
        return False