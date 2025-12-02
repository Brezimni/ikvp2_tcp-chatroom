import socket, threading, time
import server_utils

HOST = '0.0.0.0'
PORT = int(input("Izberi port: "))
SERVER_VERSION = "1.3"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(( HOST, PORT ))
server.listen()

server_ip = server_utils.get_ip()
clients = {}
clients_lock = threading.Lock()

def broadcast(message, exception=None):
    with clients_lock:
        clients_copy = list(clients.items())
    
    for client, username in clients_copy:
        if exception is client:
            continue
        try:
            client.send(message)
        except Exception as e:
            print(f"Napaka pri pošiljanju sporočila '{username}': {e}")
            terminate_connection(client)

def private_message(receiver, message):
    receiver = list(clients.keys())[list(clients.values()).index(receiver)]
    receiver.send(message)

def handle_connection(client):
    while True:
        try:
            message =  client.recv(1024).decode()
            if not message:
                terminate_connection(client)
                break
            
            if message.startswith("::p"):
                target, message = message[4:].split(" ", 1)
                message = server_utils.construct_message(clients[client], message, 'privat')
                try:
                    private_message(target, message)
                except Exception as e:
                    print(e)
                    message = server_utils.construct_message("server", "Ta uporabnik ne obstaja.", "opozorilo")
                    client.send(message)
            else:
                message = server_utils.construct_message(clients[client], message, 'navadno')
                broadcast(message, client)

        except Exception as e:
            print(e)
            terminate_connection(client)
            break

def terminate_connection(client, end=False):
    username = clients.get(client)

    if username is None:
        return  # je že odstranjen
    try:
        client.close()
    except:
        pass

    del clients[client]

    print(f"{username} odstranjen.")
    if not end:
        broadcast(f"\n{username} je zapustil/a pogovor.".encode())


def connect_client():
    print(f"Server [v{SERVER_VERSION}] deluje.", f"Server IP: {server_ip}:{PORT}", sep="\n")
    while True:
        client, address = server.accept()
        print(f"Nova povezava: {str(address)}.")

        client.send("::ime".encode())
        username = client.recv(1024).decode()
        clients[client] = username
        print(f"{username} je {address[0]}.")

        message = server_utils.construct_message("server", f"{username} se je pridružil/a pogovoru.", "obvestilo")
        broadcast(message, client)
        message = server_utils.construct_message("server", "Povezava je bila uspešno vzpostavljena.", "obvestilo")
        client.send(message)

        thread = threading.Thread(target = handle_connection, args = (client,))
        thread.start()

def admin_console():
    while True:
        command = input('').split(" ", 1)
        if command[0] == "izklop":
            message = server_utils.construct_message("server", "Server se bo izklopil.", "opozorilo")
            broadcast(message)
            for client in list(clients.keys()):
                terminate_connection(client, True)
            server.close()
            print("Server je izklopljen.")
        elif command[0] == "?":
            print("Seznam ukazov:")
        elif command[0] == "ip":
            print(server_ip, ":", PORT, sep="")
        elif command[0] == "oznani":
            try:
                message = command[1]
            except:
                message = "Ni sporočila."
            message = server_utils.construct_message("server", message, "obvestilo")
            broadcast(message)
        elif command[0] == "odstrani" or command[0] == "blokiraj":
            try:
                user = list(clients.keys())[list(clients.values()).index(command[1])]
            except Exception as e:
                print("Ta uporabnik ne obstaja.")
                print(e)
                continue
            message = server_utils.construct_message("server", f"Admin je odstranil {command[1]}.{' Admin je uporabnika tudi blokiral.' if command[0] == 'blokiraj' else ''}", "opozorilo")
            terminate_connection(user)
            broadcast(message, user)
        else:
            print("Neznan ukazni poziv:", command[0], "Za seznam ukazov pritisnite '?'")


if __name__ == "__main__":
    threading.Thread(target=admin_console, daemon=True).start()
    connect_client()
