import subprocess
import os
import sys
import shutil
import json
import zipfile
import argparse
import hashlib

def main():
    parser = argparse.ArgumentParser(description='WinP2P - Gerador de Executável com Sistema de Atualizações')
    parser.add_argument('--version', help='Versão a ser incluída no build (ex: 0.2.0)', required=True)
    parser.add_argument('--skip-build', action='store_true', help='Pular a compilação e apenas empacotar a release')
    args = parser.parse_args()

    version = args.version
    
    print(f"=== WinP2P Chat v{version} - Gerador de Executável com Suporte a Atualizações ===")
    
    # Verificar se o PyInstaller está instalado
    if not args.skip_build:
        try:
            subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], 
                          check=True, stdout=subprocess.PIPE)
        except subprocess.CalledProcessError:
            print("Erro: PyInstaller não encontrado.")
            print("Execute: pip install pyinstaller")
            return
    
    # Criar arquivos e diretórios necessários
    create_required_directories()
    
    # Criar/atualizar arquivo de versão
    with open("version.txt", "w") as f:
        f.write(version)
    
    # Atualizar versões nos arquivos de interface
    update_version_in_files(version)
    
    # Verificar/criar config.json
    ensure_config_exists()
    
    if not args.skip_build:
        print("\nConfigurando PyInstaller...")
        
        # Limpar diretórios de build anteriores
        for dir_to_clean in ['build', 'dist']:
            if os.path.exists(dir_to_clean):
                print(f"Limpando diretório {dir_to_clean}...")
                shutil.rmtree(dir_to_clean)
        
        # Adicionar opção de verificação de atualização na configuração
        update_config_with_update_settings()
        
        pyinstaller_command = [
            sys.executable, "-m", "PyInstaller",
            "--name=WinP2P",
            "--windowed",  
            "--onefile",   
            "--add-data=config.json;.",  
            "--add-data=version.txt;.",  
            "--icon=resources/icon.ico" if os.path.exists("resources/icon.ico") else "",
            "main.py" 
        ]
        
        if not os.path.exists("resources/icon.ico"):
            print("Aviso: Arquivo de ícone não encontrado. O executável usará o ícone padrão.")
            pyinstaller_command = [cmd for cmd in pyinstaller_command if not cmd.startswith("--icon")]
        
        print("\nGerando executável... (isso pode levar alguns minutos)")
        try:
            subprocess.run(pyinstaller_command, check=True)
            
            print("\nCopiando arquivos adicionais...")
            for folder in ['logs', 'config', 'received_files', 'resources']:
                dest_folder = f"dist/{folder}"
                os.makedirs(dest_folder, exist_ok=True)
                
                # Se for a pasta resources e ela existir, copie o conteúdo
                if folder == 'resources' and os.path.exists(folder):
                    for item in os.listdir(folder):
                        src = os.path.join(folder, item)
                        dst = os.path.join(dest_folder, item)
                        if os.path.isfile(src):
                            shutil.copy2(src, dst)
            
            print("\nCriando pacote zip para distribuição...")
            create_release_package(version)
            
            print("\n=== Processo concluído com sucesso! ===")
            print(f"O executável foi criado em: dist/WinP2P.exe")
            print(f"O arquivo para atualização foi criado em: releases/WinP2P-v{version}.exe")
            
        except subprocess.CalledProcessError as e:
            print(f"\nErro ao gerar executável: {e}")
            print("Verifique se todas as dependências estão instaladas corretamente.")
    else:
        print("Pulando build, criando apenas o executável para atualização...")
        if os.path.exists("WinP2P.exe"):
            os.makedirs("releases", exist_ok=True)
            release_file = os.path.join("releases", f"WinP2P-v{version}.exe")
            shutil.copy2("WinP2P.exe", release_file)
            
            # Calcular hash
            exe_hash = calculate_file_hash(release_file)
            hash_file = os.path.join("releases", f"WinP2P-v{version}.exe.sha256")
            with open(hash_file, 'w') as f:
                f.write(f"{exe_hash} *WinP2P-v{version}.exe")
                
            print(f"\nArquivo de atualização criado em: {release_file}")
        else:
            print("ERRO: Arquivo WinP2P.exe não encontrado no diretório atual.")
            print("Coloque o executável na mesma pasta deste script ou execute sem a opção --skip-build.")

def create_required_directories():
    """Cria diretórios necessários para a aplicação"""
    dirs = ['logs', 'config', 'received_files', 'releases']
    for dir_name in dirs:
        os.makedirs(dir_name, exist_ok=True)

def update_version_in_files(version):
    """Atualiza o número da versão em arquivos da interface"""
    files_to_update = {
        'ui/about_window.py': ('<h3>Versão 0.1</h3>', f'<h3>Versão {version}</h3>'),
        'ui/startup_window.py': ('"<p>Versão 0.1</p>"', f'"<p>Versão {version}</p>"'),
        'README.md': ('## WinP2P', f'## WinP2P v{version}')
    }
    
    for file_path, (old_text, new_text) in files_to_update.items():
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                updated_content = content.replace(old_text, new_text)
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(updated_content)
                
                print(f"Versão atualizada em {file_path}")
            except Exception as e:
                print(f"Erro ao atualizar versão em {file_path}: {e}")

def ensure_config_exists():
    """Verifica se o arquivo config.json existe e cria se necessário"""
    if not os.path.exists("config.json"):
        default_config = {
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
        with open("config.json", "w") as f:
            json.dump(default_config, f, indent=4)
        print("Arquivo config.json criado com valores padrão")

def update_config_with_update_settings():
    """Adiciona configurações de atualização ao config.json"""
    try:
        with open("config.json", "r") as f:
            config = json.load(f)
        
        # Adicionar configuração de atualização automática se não existir
        if "check_updates_at_startup" not in config:
            config["check_updates_at_startup"] = True
            
        with open("config.json", "w") as f:
            json.dump(config, f, indent=4)
            
        print("Configurações de atualização adicionadas ao config.json")
    except Exception as e:
        print(f"Erro ao atualizar config.json: {e}")

def create_release_package(version):
    """Cria um pacote ZIP contendo todos os arquivos necessários para a atualização"""
    release_dir = "releases"
    os.makedirs(release_dir, exist_ok=True)
    
    # Copiar o executável para o diretório de releases
    if os.path.exists("dist/WinP2P.exe"):
        exe_release_path = os.path.join(release_dir, f"WinP2P-v{version}.exe")
        shutil.copy2("dist/WinP2P.exe", exe_release_path)
        print(f"Executável copiado para: {exe_release_path}")
        
        # Calcular e salvar o hash do arquivo para verificação de integridade
        exe_hash = calculate_file_hash(exe_release_path)
        hash_file = os.path.join(release_dir, f"WinP2P-v{version}.exe.sha256")
        with open(hash_file, 'w') as f:
            f.write(f"{exe_hash} *WinP2P-v{version}.exe")
        
        return True
    else:
        print("ATENÇÃO: Executável não encontrado!")
        return False

def calculate_file_hash(filename):
    """Calcula o hash SHA-256 de um arquivo"""
    sha256 = hashlib.sha256()
    with open(filename, 'rb') as f:
        for block in iter(lambda: f.read(65536), b''):
            sha256.update(block)
    return sha256.hexdigest()

if __name__ == "__main__":
    main()