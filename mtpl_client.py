import socket
import threading

# Server settings
HOST = '127.0.0.1'  # Server address
PORT = 12345        # Server port

# Function to receive messages from the server
def receive_messages(client_socket):
    while True:
        try:
            message = client_socket.recv(1024).decode('utf-8')
            if message:
                print(message)
        except ConnectionResetError:
            print("Disconnected from server.")
            break

# Main client function
def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))
    print("Connected to the server.")

    # Start a thread to listen for messages
    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    # Main loop to send messages
    try:
        while True:
            message = input("You: ")
            client_socket.sendall(message.encode('utf-8'))
    except KeyboardInterrupt:
        print("Exiting...")
        client_socket.close()

if __name__ == "__main__":
    start_client()
