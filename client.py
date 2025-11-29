import socket, threading, sys

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect(( "127.0.0.1", 9090 ))

    connected = False
    username = input("Izberi si ime: ")

    def receive():
        nonlocal connected
        while True:
            try:
                message = client.recv(1024).decode()
                if message == "::ime" and not connected:
                    client.send(username.encode())
                    connection_state = True
                else:
                    print_message(message)
            except Exception as e:
                print("Prišlo je do napake: ", e)
                client.close()
                break
    
    def print_message(msg: str):
        nonlocal username
        sys.stdout.write("\r" + msg + "\n")
        sys.stdout.write(f'{username}:')
        sys.stdout.flush()
 
    def send():
        nonlocal username
        while True:
            try:
                message = input(f'{username}: ')
                if not message.strip():
                    continue
                elif message.startswith("::"):
                    print("Ukaz je:", message.replace("::", ""))
                else:
                    client.send(f"{username}: {message}".encode())
            except:
                print("Povezava prekinjena.")
                client.close()
                break
    
    threading.Thread(target= receive).start()
    threading.Thread(target= send).start()

if __name__ == "__main__":
    main()