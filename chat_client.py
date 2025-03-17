# chat_client.py

import grpc
import threading
import chat_pb2
import chat_pb2_grpc
import os

def generate_messages(username):
    """
    Função geradora que lê mensagens do teclado
    e as envia para o servidor via stream.
    """
    while True:
        text = input()
        # Caso o usuário digite /quit, encerramos a stream de forma limpa
        if text.strip().lower() == '/quit':
            print("[CLIENT] Encerrando cliente...")
            os._exit(0)  # Força o encerramento imediato do processo

        yield chat_pb2.ChatMessage(
            user=username,
            text=text,
        )

def run_client(username):
    # Conecta ao servidor gRPC (ajuste host:porta se estiver remoto)
    channel = grpc.insecure_channel('localhost:50051')
    stub = chat_pb2_grpc.ChatServiceStub(channel)

    # Chama o método ChatStream (stream bidirecional).
    # Precisamos passar um iterador de mensagens de saída (generate_messages)
    # e receber um iterador de mensagens de entrada (response_iterator).
    response_iterator = stub.ChatStream(generate_messages(username))

    # Cria uma thread para ficar lendo as mensagens recebidas do servidor.
    def read_incoming_messages():
        try:
            for msg in response_iterator:
                # Imprime as mensagens no console
                print(f"[{msg.user}] {msg.text}")
        except grpc.RpcError as e:
            print("[CLIENT] Conexão encerrada pelo servidor.")

    # Inicia a thread de recepção
    t = threading.Thread(target=read_incoming_messages, daemon=True)
    t.start()

    # Mantém o cliente ativo até que a thread se encerre
    print(f"[CLIENT] Bem-vindo(a), {username}! Digite suas mensagens (ou /quit para sair):")
    t.join()  # Espera a thread de leitura terminar (ou interromper)

if __name__ == '__main__':
    nome = input("Digite seu nome de usuário: ")
    run_client(nome)
