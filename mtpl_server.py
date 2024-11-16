import socket
import threading

# Server settings
HOST = '127.0.0.1'  # Localhost
PORT = 12345        # Port to listen on

# List to store connected clients
clients = []

# Function to handle each client
def handle_client(client_socket, addr):
    print(f"New connection: {addr}")
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            print(f"Received from {addr}: {message}")
            broadcast(f"{addr}: {message}", client_socket)
        except ConnectionResetError:
            break
    print(f"Connection closed: {addr}")
    clients.remove(client_socket)
    client_socket.close()

# Function to broadcast messages to all clients
def broadcast(message, sender_socket):
    for client in clients:
        if client != sender_socket:
            client.sendall(message.encode('utf-8'))

# Main server function
def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print(f"Server started on {HOST}:{PORT}")
    while True:
        client_socket, addr = server.accept()
        clients.append(client_socket)
        thread = threading.Thread(target=handle_client, args=(client_socket, addr))
        thread.start()

if __name__ == "__main__":
    start_server()
