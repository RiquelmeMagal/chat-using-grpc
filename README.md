# 🚀 Chat gRPC - Python

Bem-vindo(a) ao projeto **Chat gRPC em Python**! Este repositório demonstra a criação de um chat utilizando **gRPC (RPC sobre HTTP/2)** com **stream bidirecional**, permitindo que vários participantes enviem e recebam mensagens simultaneamente.

## 📚 Contexto - Sistemas Distribuídos

Este projeto faz parte de estudos na disciplina de **Sistemas Distribuídos (SD)**. Em SD, temos múltiplos processos/nós distribuídos em rede trocando mensagens para realizar tarefas cooperativas.

**gRPC** é um framework de comunicação que utiliza **RPC (Remote Procedure Call)** sobre HTTP/2, oferecendo suporte a **streaming de dados de forma eficiente e tipada**.

### Chat
Cada participante se conecta a um **servidor gRPC** e inicia um **stream bidirecional**. Isso significa que cliente e servidor podem enviar dados (mensagens) a qualquer momento, sem a necessidade de requisitar/responder explicitamente. É ideal para aplicações de bate-papo.

## 🗂 Estrutura do Projeto

```
.
├── chat.proto            # Definição do serviço e das mensagens (Protobuf)
├── chat_pb2.py          # Gerado automaticamente pelo protoc
├── chat_pb2_grpc.py     # Gerado automaticamente pelo protoc
├── chat_server.py        # Implementação do servidor gRPC
├── chat_client.py        # Implementação do cliente
├── requirements.txt        # Importações
└── README.md             # Este arquivo (documentação)
```

> **Observação**: Os arquivos `chat_pb2.py` e `chat_pb2_grpc.py` são gerados a partir do `chat.proto` usando o `grpc_tools.protoc`. Se eles não existirem, basta executar o comando de geração (ver seção de execução).

## 🔧 Pré-Requisitos

- Python (3.7+ recomendado)
- pip (gerenciador de pacotes do Python)
- gRPC e gRPC Tools:
  - `grpcio`
  - `grpcio-tools`
  - `protobuf` (versão compatível)

## 📥 Clonando o repositório

```bash
git clone git@github.com:RiquelmeMagal/chat-using-grpc.git
cd chat-using-gRPC
```

## 🐍 Criação do Ambiente Virtual

Para isolar dependências, recomenda-se criar um **ambiente virtual** em Python.

### Linux/macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

- `python3 -m venv venv` cria o ambiente virtual na pasta `venv`.
- `source venv/bin/activate` ativa o ambiente.

### Windows

```bash
python -m venv venv
.env\Scripts\activate
```

- `python -m venv venv` cria o ambiente virtual.
- `.env\Scripts\activate` ativa o ambiente no **Windows** (PowerShell ou CMD).

## 📦 Instalação de Dependências

Com o ambiente virtual ativo, instale as dependências:

```bash
pip install -r requirements.txt
```

Caso não tenha o arquivo `requirements.txt`, você pode instalar manualmente:

```bash
pip install grpcio grpcio-tools protobuf
```

## 🏗 Gerando Arquivos Protobuf (se necessário)

Se você não ver os arquivos `chat_pb2.py` e `chat_pb2_grpc.py`, gere-os executando no terminal:

```bash
python -m grpc_tools.protoc -I=. --python_out=. --grpc_python_out=. chat.proto
```

Isso compila o arquivo `chat.proto` e gera o código Python para serialização/desserialização (**Protobuf**) e para o serviço **gRPC**.

## ⚙️ Executando o Projeto

Abra **dois ou mais terminais** (um para o servidor, um ou mais para os clientes). Certifique-se de ativar o ambiente virtual em cada terminal antes de executar.

### 1️⃣ Executar o Servidor

No primeiro terminal (ambiente já ativo):

```bash
python chat_server.py
```

Você verá:

```bash
[SERVER] gRPC server rodando na porta 50051...
```

Isso significa que o servidor está esperando conexões **gRPC** na porta `50051`.

### 2️⃣ Executar o Cliente

Em outro terminal (também com ambiente ativo), rode:

```bash
python chat_client.py
```

- Será pedido um **nome de usuário**. Digite algo como `Alice`, `Bob`, etc.
- Pressione **Enter** para enviar mensagens.
- Cada cliente se conecta ao servidor e fica em **stream bidirecional**.
- Para criar outro cliente, abra quantos terminais quiser e execute novamente `chat_client.py`.
- Qualquer mensagem enviada por um cliente será vista por **todos os participantes conectados**.

## 🗣 Exemplo de Uso

### Terminal 1 (Servidor):

```bash
(venv) user@pc:~/chat-using-gRPC$ python chat_server.py
[SERVER] gRPC server rodando na porta 50051...
```

### Terminal 2 (Cliente 1):

```bash
(venv) user@pc:~/chat-using-gRPC$ python chat_client.py
Digite seu nome de usuário: Alice
[CLIENT] Bem-vindo(a), Alice! Digite suas mensagens:
Alice digita: Olá a todos!
```

### Terminal 3 (Cliente 2):

```bash
(venv) user@pc:~/chat-using-gRPC$ python chat_client.py
Digite seu nome de usuário: Bob
[CLIENT] Bem-vindo(a), Bob! Digite suas mensagens:
Bob verá imediatamente a mensagem de Alice: [Alice] Olá a todos!
Bob digita: Oi, Alice!
```

### Terminal 2 (Cliente 1 - Alice) verá:

```bash
[Bob] Oi, Alice!
```

## 🔍 O que está acontecendo internamente?

- **Protocolo**: gRPC utiliza **HTTP/2** para troca de mensagens.
- **Serviço**: `ChatService` define um método de **streaming bidirecional**, `ChatStream`, no arquivo `chat.proto`.
- **Server**:
  - Implementa `ChatServiceServicer`, que:
  - Gerencia todos os **clientes conectados** (fila de mensagens).
  - **Difunde mensagens** para todos (**broadcast**).
- **Client**:
  - Define um **gerador de mensagens** (lê do teclado).
  - Recebe um **iterador de mensagens** (recebe do servidor) ao mesmo tempo, graças a **threads em Python**.

Assim, cada cliente pode **enviar e receber mensagens a qualquer momento**, sem precisar “esperar” o outro enviar.

## 🏆 Conclusão

Este projeto demonstra na prática como usar **gRPC** em um contexto de **Sistemas Distribuídos**, com **stream bidirecional** para criar um **chat** que permite mensagens simultâneas.

- **Escalabilidade**: Você pode adicionar quantos clientes quiser ao servidor.
- **Extensibilidade**: Você pode customizar, adicionar autenticação ou até migrar para um modelo **P2P** com uma lógica mais complexa de descoberta de nós.


Enjoy coding & bons estudos em **Sistemas Distribuídos**! 🚀
