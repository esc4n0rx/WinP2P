import subprocess
import os
import sys
import shutil

def main():
    print("=== WinP2P Chat - Gerador de Executável ===")
    
    try:
        subprocess.run([sys.executable, "-m", "PyInstaller", "--version"], 
                      check=True, stdout=subprocess.PIPE)
    except subprocess.CalledProcessError:
        print("Erro: PyInstaller não encontrado.")
        print("Execute: pip install pyinstaller")
        return
    
    os.makedirs("logs", exist_ok=True)
    os.makedirs("config", exist_ok=True)
    os.makedirs("received_files", exist_ok=True)
    
    if not os.path.exists("config.json"):
        import json
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
            "room_password": ""
        }
        with open("config.json", "w") as f:
            json.dump(default_config, f, indent=4)
    
    print("\nConfigurando PyInstaller...")
    
    pyinstaller_command = [
        sys.executable, "-m", "PyInstaller",
        "--name=WinP2P",
        "--windowed",  
        "--onefile",   
        "--add-data=config.json;.",  
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
        if os.path.exists("dist/WinP2P"):
            os.makedirs("dist/WinP2P/logs", exist_ok=True)
            os.makedirs("dist/WinP2P/config", exist_ok=True)
            os.makedirs("dist/WinP2P/received_files", exist_ok=True)
        
        print("\n=== Processo concluído com sucesso! ===")
        print("O executável foi criado em: dist/WinP2P.exe")
        print("\nObservações:")
        print("1. Ao distribuir, inclua as pastas 'logs', 'config' e 'received_files'")
        print("2. Para personalizar o ícone, adicione um arquivo 'icon.ico' na pasta 'resources'")
        
    except subprocess.CalledProcessError as e:
        print(f"\nErro ao gerar executável: {e}")
        print("Verifique se todas as dependências estão instaladas corretamente.")

if __name__ == "__main__":
    main()