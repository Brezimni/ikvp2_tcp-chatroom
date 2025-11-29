import socket, threading, urllib.request, json

HOST = '127.0.0.1'
PORT = 9090

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(( HOST, PORT ))
server.listen()

server_ip = json.load(urllib.request.urlopen("https://api.ipify.org?format=json"))["ip"]
clients = []
usernames = []

def broadcast(message, exception = None):
    for client in clients:
        if exception is client:
            continue
        try:
            client.send(message)
        except:
            terminante_connection(client)

def handle_connection(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message, client)
        except:
            terminante_connection(client)
            break

def terminante_connection(client):
    client_index = clients.index(client)
    clients.remove(client)
    client.close()
    username = usernames[client_index]
    print(f"{username} odstranjen.")
    broadcast(f"\n{username} je zapustil/a pogovor.".encode())
    usernames.remove(username)


def connect_client():
    print("Server deluje.", f"Server IP: {server_ip}", sep="\n")
    while True:
        client, address = server.accept()
        print(f"Nova povezava: {str(address)}.")

        client.send("::ime".encode())
        username = client.recv(1024).decode()
        usernames.append(username)
        clients.append(client)
        print(f"{address} je {username}.")

        broadcast(f"{username} se je pridružil/a pogovoru.".encode(), client)
        client.send("Povezava je bila uspešno vzpostavljena.".encode())

        thread = threading.Thread(target = handle_connection, args = (client,))
        thread.start()

if __name__ == "__main__":
    connect_client()
