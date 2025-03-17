# chat_server.py

import grpc
import time
import queue
import threading
from concurrent import futures

import chat_pb2
import chat_pb2_grpc

# Armazenaremos uma lista (global) de filas. Cada fila representará
# as mensagens destinadas a um cliente conectado.
client_queues = []  # lista de queues.Queue()

class ChatServiceServicer(chat_pb2_grpc.ChatServiceServicer):
    def ChatStream(self, request_iterator, context):
        """
        Implementação do método de stream bidirecional.
        Cada novo cliente que entra:
          1) Cria sua queue exclusiva.
          2) Lança uma thread para ler as mensagens vindas do cliente (request_iterator),
             e quando chegam, difunde para todos.
          3) Faz yield das mensagens que estão na sua queue para devolver ao cliente.
        """
        # 1) Cria a fila deste cliente
        q = queue.Queue()
        client_queues.append(q)

        # 2) Função de thread para consumir as mensagens de entrada (request_iterator)
        def receive_messages():
            try:
                for msg in request_iterator:
                    # Ao receber mensagem, vamos difundir para todas as filas
                    broadcast_message(msg)
            except grpc.RpcError as e:
                # Se o cliente desconectar, isso gera exception. Apenas finalize.
                print("[SERVER] Client disconnected.")
            finally:
                # Remove a fila deste cliente da lista global, se ainda estiver lá
                if q in client_queues:
                    client_queues.remove(q)

        # 3) Iniciamos a thread para consumir mensagens de entrada
        t = threading.Thread(target=receive_messages, daemon=True)
        t.start()

        # 4) Enquanto esse cliente estiver ativo, faça yield de qualquer mensagem
        # que cair na queue 'q'.
        try:
            while True:
                msg = q.get()  # bloqueia até ter mensagem para este cliente
                yield msg
        except GeneratorExit:
            # Quando o cliente encerrar o stream (desconectou),
            # 'GeneratorExit' é lançado. Limpamos recursos, se necessário.
            if q in client_queues:
                client_queues.remove(q)
            print("[SERVER] Client stream closed.")

def broadcast_message(msg):
    """
    Envia 'msg' para todas as filas (de todos os clientes).
    """
    for q in client_queues:
        q.put(msg)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    chat_pb2_grpc.add_ChatServiceServicer_to_server(ChatServiceServicer(), server)
    server.add_insecure_port('[::]:50051')  # porta de escuta
    server.start()
    print("[SERVER] gRPC server rodando na porta 50051...")
    print("[SERVER] Digite 'q' para encerrar o servidor.")

    # Em vez de ficar bloqueado em um while True + time.sleep,
    # agora ficamos aguardando um input 'q' para encerrar.
    try:
        while True:
            cmd = input()
            if cmd.strip().lower() == 'q':
                print("[SERVER] Encerrando servidor...")
                break
    except EOFError:
        # Caso o input seja interrompido por EOF (Ctrl+D em alguns terminais), 
        # também encerramos o servidor.
        pass
    finally:
        server.stop(0)

if __name__ == '__main__':
    serve()
