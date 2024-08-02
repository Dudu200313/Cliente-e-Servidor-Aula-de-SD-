# A simple server that listens for multiple clients and prints their messages
# Each client on a separate thread

import socket
import threading

# Create a socket object
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to a specific address and port
server.bind(('0.0.0.0', 1235))

# Listen for incoming connections
server.listen()

# List of clients
clients = []

# Function to handle incoming messages from clients
def pegar_mensagem(client):
    while True:
        try:
            # Receive data from client
            message = client.recv(150).decode('utf-8')
            if not message:
                break
            print(f'Message from client: {message}')
        except Exception as e:
            print(f"Error receiving message: {e}")
            clients.remove(client)
            client.close()
            break

# Function to send messages to the client
def mandar_mensagem(client):
    while True:
        try:
            mensagem = input("Digite uma mensagem para enviar: ")
            if mensagem.lower() == 'sair':  # Command to exit
                client.sendall(mensagem.encode())
                break
            client.sendall(mensagem.encode())
        except Exception as e:
            print(f"Erro no envio: {e}")
            break 

# Main loop to accept clients
while True:
    print('Aguardando conexão...')
    # Accept incoming connection
    client, address = server.accept()
    print(f'Conectado com {str(address)}')

    # Add the client to the list
    clients.append(client)

    # Create a thread for receiving messages
    receber_thread = threading.Thread(target=pegar_mensagem, args=(client,))
    receber_thread.start()

    # Create a thread for sending messages
    enviar_thread = threading.Thread(target=mandar_mensagem, args=(client,))
    enviar_thread.start()