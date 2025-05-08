import socket
import threading
import json
from PyQt5.QtCore import QThread, pyqtSignal

class Client(QThread):
    message_received = pyqtSignal(str)
    connected = pyqtSignal()
    disconnected = pyqtSignal()
    
    def __init__(self, host, port):
        super().__init__()
        self.host = host
        self.port = int(port)
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.settimeout(10)  # 10 segundos de timeout para conexão
        self.running = True
        self._connected = False
    
    def run(self):
        try:
            self.sock.connect((self.host, self.port))
            self._connected = True
            self.connected.emit()
            
            # Iniciar loop de recebimento
            self.receive_thread = threading.Thread(
                target=self.receive_loop, 
                daemon=True
            )
            self.receive_thread.start()
            
        except Exception as e:
            print(f"Connection error: {e}")
            self.disconnected.emit()
    
    def receive_loop(self):
        """Loop de recebimento de mensagens"""
        buffer = b""
        
        self.sock.settimeout(1)  # Timeout curto para permitir interrupção limpa
        
        while self.running:
            try:
                # Receber dados em buffer
                chunk = self.sock.recv(4096)
                if not chunk:
                    break
                
                buffer += chunk
                
                # Processar múltiplas mensagens no buffer
                while b"\n" in buffer:
                    message, buffer = buffer.split(b"\n", 1)
                    if message:
                        self.message_received.emit(message.decode())
                
                # Se não há marcador de fim, mas temos dados completos
                if buffer:
                    self.message_received.emit(buffer.decode())
                    buffer = b""
                    
            except socket.timeout:
                continue
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"Receive error: {e}")
                if not self.running:
                    break
                continue
        
        self._connected = False
        self.disconnected.emit()
        
        try:
            self.sock.close()
        except:
            pass
    
    def send(self, message):
        """Envia mensagem para o servidor"""
        if not self._connected:
            return False
            
        try:
            if isinstance(message, str):
                message = message.encode()
                
            self.sock.send(message)
            return True
            
        except Exception as e:
            print(f"Send error: {e}")
            self._connected = False
            self.disconnected.emit()
            return False
    
    def is_connected(self):
        """Verifica se está conectado"""
        return self._connected
    
    def disconnect(self):
        """Desconecta do servidor"""
        self.running = False
        
        try:
            self.sock.close()
        except:
            pass
        
        self._connected = False