import socket
import threading
import json
from PyQt5.QtCore import QThread, pyqtSignal

class Server(QThread):
    message_received = pyqtSignal(str)
    client_connected = pyqtSignal(tuple)
    client_disconnected = pyqtSignal()
    
    def __init__(self, host, port, max_clients=1):
        super().__init__()
        self.host = host
        self.port = port
        self.max_clients = max_clients
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.clients = []
        self.running = True
        self.client_handlers = []
    
    def run(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(1)
        self.sock.settimeout(1) 
        
        while self.running:
            try:
                conn, addr = self.sock.accept()
                
                
                if len(self.clients) >= self.max_clients:
                   
                    reject_msg = json.dumps({"type": "room_full"})
                    conn.send(reject_msg.encode())
                    conn.close()
                    continue
                
                self.clients.append(conn)
                self.client_connected.emit(addr)
                
                handler = threading.Thread(
                    target=self.handle_client, 
                    args=(conn, addr), 
                    daemon=True
                )
                self.client_handlers.append(handler)
                handler.start()
                
            except socket.timeout:
                continue
            except Exception as e:
                print(f"Server accept error: {e}")
                if not self.running:
                    break
    
    def handle_client(self, conn, addr):
        """Processa mensagens de um cliente"""
        buffer = b""
        
        while self.running:
            try:
                chunk = conn.recv(4096)
                if not chunk:
                    break
                
                buffer += chunk
                
                while b"\n" in buffer:
                    message, buffer = buffer.split(b"\n", 1)
                    if message:
                        self.message_received.emit(message.decode())
                
               
                if buffer:
                    self.message_received.emit(buffer.decode())
                    buffer = b""
                    
            except ConnectionResetError:
                break
            except Exception as e:
                print(f"Client handler error: {e}")
                break
        
        if conn in self.clients:
            self.clients.remove(conn)
            self.client_disconnected.emit()
        
        try:
            conn.close()
        except:
            pass
    
    def has_clients(self):
        """Verifica se existem clientes conectados"""
        return len(self.clients) > 0
    
    def broadcast(self, message):
        """Envia mensagem para todos os clientes"""
        if isinstance(message, str):
            if not message.endswith('\n'):
                message = message + '\n'
            message = message.encode()
        elif isinstance(message, bytes) and not message.endswith(b'\n'):
            message = message + b'\n'
            
        disconnected = []
        
        for client in self.clients:
            try:
                client.send(message)
            except:
                disconnected.append(client)
        
        for client in disconnected:
            if client in self.clients:
                self.clients.remove(client)
                self.client_disconnected.emit()
    
    def stop(self):
        """Para o servidor e libera recursos"""
        self.running = False
        
        for client in self.clients:
            try:
                client.close()
            except:
                pass
        
        try:
            self.sock.close()
        except:
            pass
        
        self.wait()