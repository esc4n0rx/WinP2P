from cryptography.fernet import Fernet
import base64
import os

# Chave estática para desenvolvimento
# Em produção, a chave seria trocada durante o handshake inicial
CRYPTO_KEY = b'vwP2g-Sq4qzcZk51wuz94JO7l_zMbHwh8vc9Ly8pSw8='

# Inicializar o objeto Fernet com a chave
_fernet = Fernet(CRYPTO_KEY)

def generate_key():
    """Gera uma nova chave de criptografia"""
    return Fernet.generate_key()

def set_crypto_key(key):
    """Configura a chave de criptografia a ser usada"""
    global _fernet
    _fernet = Fernet(key)

def encrypt_message(message):
    """Criptografa uma mensagem de texto"""
    if isinstance(message, str):
        message = message.encode('utf-8')
    
    try:
        token = _fernet.encrypt(message)
        return token.decode('utf-8')  # Retorna como string
    except Exception as e:
        print(f"Encryption error: {e}")
        return message.decode('utf-8') if isinstance(message, bytes) else message

def decrypt_message(token):
    """Descriptografa uma mensagem criptografada"""
    if isinstance(token, str):
        token = token.encode('utf-8')
    
    try:
        message = _fernet.decrypt(token)
        return message.decode('utf-8')  # Retorna como string
    except Exception as e:
        print(f"Decryption error: {e}")
        return token.decode('utf-8') if isinstance(token, bytes) else token

def encrypt_file(file_path, output_path=None):
    """Criptografa um arquivo"""
    if output_path is None:
        output_path = file_path + '.encrypted'
    
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        
        encrypted_data = _fernet.encrypt(data)
        
        with open(output_path, 'wb') as f:
            f.write(encrypted_data)
        
        return output_path
    except Exception as e:
        print(f"File encryption error: {e}")
        return None

def decrypt_file(encrypted_path, output_path=None):
    """Descriptografa um arquivo"""
    if output_path is None:
        if encrypted_path.endswith('.encrypted'):
            output_path = encrypted_path[:-10]
        else:
            output_path = encrypted_path + '.decrypted'
    
    try:
        with open(encrypted_path, 'rb') as f:
            encrypted_data = f.read()
        
        decrypted_data = _fernet.decrypt(encrypted_data)
        
        with open(output_path, 'wb') as f:
            f.write(decrypted_data)
        
        return output_path
    except Exception as e:
        print(f"File decryption error: {e}")
        return None