import random
import string
import base64


WORDS = [
    'apple','banana','cherry','delta','echo','foxtrot',
    'golf','hotel','india','juliet','kilo','lima'
]

def generate_room_code(ip: str, port: int) -> str:
    """
    Gera código no formato: <palavra><4 dígitos>-<base64(ip:port)>.
    """
    word = random.choice(WORDS)
    digits = ''.join(random.choices(string.digits, k=4))
    raw = f"{ip}:{port}".encode()
    b64 = base64.urlsafe_b64encode(raw).decode()
    return f"{word}{digits}-{b64}"

def decode_room_code(code: str):
    """
    Decodifica '<prefix>-<base64>' ou 'ip:port'.
    """
    if '-' in code:
        _, b64 = code.split('-', 1)
        raw = base64.urlsafe_b64decode(b64.encode()).decode()
        ip, port = raw.split(':')
        return ip, int(port)
    if ':' in code:
        ip, port = code.split(':', 1)
        return ip, int(port)
    raise ValueError('Formato de código inválido')