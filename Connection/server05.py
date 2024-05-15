import socket
import json

SERVER_IP = '0.0.0.0'  # Listen on all available interfaces
SERVER_PORT = 12345

def handle_client(conn, addr):
    data = conn.recv(4096)
    if data:
        stats = json.loads(data.decode('utf-8'))
        print(f"Received data from {addr}: {stats}")

if __name__ == "__main__":
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((SERVER_IP, SERVER_PORT))
        s.listen()
        print(f"Server listening on {SERVER_IP}:{SERVER_PORT}")
        while True:
            conn, addr = s.accept()
            handle_client(conn, addr)
            conn.close()
