import socket
import threading

server_ip = '10.35.4.5'
server_port = 1235

def receive_messages(sock):
    while True:
        try:
            mensagem = sock.recv(1024).decode()
            if mensagem:
                print(f"Mensagem do servidor: {mensagem}")
            else:
                # Conexão fechada pelo servidor
                print("Servidor fechou a conexão.")
                break
        except Exception as e:
            print(f"Erro ao receber mensagem: {e}")
            break

def send_messages(sock):
    while True:
        try:
            mensagem = input("Digite uma mensagem para enviar ao servidor: ")
            if mensagem.lower() == 'sair':
                print("Encerrando conexão...")
                break
            sock.sendall(mensagem.encode())
        except Exception as e:
            print(f"Erro ao enviar mensagem: {e}")
            break

def main():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        sock.connect((server_ip, server_port))
        print(f"Conectado ao servidor {server_ip}:{server_port}")

        # Iniciar thread para receber mensagens
        receive_thread = threading.Thread(target=receive_messages, args=(sock,))
        receive_thread.daemon = True  # Permite que a thread termine quando a principal terminar
        receive_thread.start()

        # Iniciar thread para enviar mensagens
        send_thread = threading.Thread(target=send_messages, args=(sock,))
        send_thread.start()

        # Esperar a thread de envio terminar
        send_thread.join()

    finally:
        sock.close()

if __name__ == "__main__":
    main()