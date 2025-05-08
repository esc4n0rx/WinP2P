# WinP2P

WinP2P é aplicativo de chat ponto-a-ponto (P2P) com interfaces inspiradas em designs clássicos, criptografia de mensagens e recursos modernos.

## Características

- **Chat P2P direto** sem servidor intermediário
- **Criptografia** de ponta a ponta para mensagens
- **Múltiplos temas visuais** (Windows 95, XP, Moderno, Dark, Terminal)
- **Indicação de status** de usuários (online, digitando, offline)
- **Salas privadas** limitadas a 2 pessoas
- **Notificações de eventos** (conexão, desconexão)
- **Interface moderna** com bolhas de chat estilizadas

## Requisitos

- Python 3.8+
- PyQt5
- cryptography

## Instalação

1. Clone o repositório:
   ```
   git clone https://github.com/esc4n0rx/pp
   cd pp
   ```

2. Crie e ative um ambiente virtual (opcional, mas recomendado):
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```

3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```

## Uso

Execute o aplicativo:
```
python main.py
```

### Criando uma sala de chat

1. Na tela inicial, clique em "Criar Nova Sala"
2. Um código da sala será gerado e copiado para a área de transferência
3. Compartilhe este código com outra pessoa para que ela possa se conectar

### Entrando em uma sala

1. Na tela inicial, clique em "Entrar em uma Sala"
2. Cole o código da sala recebido
3. Você será conectado à sala de chat

## Estrutura do Projeto

```
pp/
├── main.py              # Ponto de entrada do aplicativo
├── config.json          # Arquivo de configuração
├── requirements.txt     # Dependências
├── ui/                  # Interfaces gráficas
│   ├── startup_window.py   # Tela inicial
│   ├── main_window.py      # Janela principal de chat
│   ├── config_window.py    # Configurações
│   ├── about_window.py     # Sobre
│   └── themes.py           # Temas visuais
├── network/             # Módulos de rede
│   ├── server.py           # Servidor para hospedar salas
│   └── client.py           # Cliente para conectar a salas
└── utils/               # Utilitários
    ├── code_generator.py   # Gerador de códigos de sala
    └── crypto.py           # Funções de criptografia
```

## Segurança

- As mensagens são criptografadas usando a biblioteca cryptography (Fernet)
- A conexão é direta entre os peers (P2P), sem armazenamento central
- Os códigos de sala codificam o endereço IP e porta em formato Base64

## Personalização

Você pode personalizar o aplicativo através do menu de configurações:
- Nome de usuário
- Cor do avatar
- Tema da interface
- Porta de rede
- Configurações de segurança
- Opções de exibição

## Licença

Este projeto está licenciado sob a licença MIT.