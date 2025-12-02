import socket, threading, sys, os

def main():
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_ip = input("Vnesi IP serverja: ")
    server_port = int(input("Vnesi port serverja: "))
    client.connect(( server_ip, server_port ))

    connected = False
    username = input("Izberi si ime: ")

    def receive():
        nonlocal connected
        nonlocal username
        while True:
            try:
                message = client.recv(1024).decode('utf-8')
                if not message.strip(): # Če prejemamo prazen niz, pomeni, da se je povezava prekinila
                    print("\nPovezava je bila prekinjena.")
                    client.close()
                    os._exit(0)
                elif message == "::ime" and not connected:
                    client.send(username.encode())
                    connected = True
                    continue
                elif message.startswith("\033[30;47mserver\033[0m: ::ime"):
                    username = message.rsplit("spremenjeno v ", 1)[1].strip()
                    print_message(message.replace("::ime ", ""))
                else:
                    print_message(message)
            except Exception as e:
                print("Prišlo je do napake: ", e)
                client.close()
                break
    
    def print_message(msg: str):
        nonlocal username
        sys.stdout.write("\r" + msg + "\n")
        sys.stdout.write(f'\033[32m{username}\033[0m: ')
        sys.stdout.flush()
 
    def send():
        nonlocal username
        first_time = True # Prepreči, da bi se input besedilo ob zagonu izpisalo dvakrat
        while True:
            try:
                message = input('' if first_time else f'\033[32m{username}\033[0m: ').strip()
                if first_time: first_time = False

                if not message:
                    continue
                elif message.startswith("::izpis"):
                    client.close()
                    os._exit(0)
                else:
                    client.send(message.encode())
            except:
                print("Povezava prekinjena.")   
                client.close()
                break
    
    threading.Thread(target= receive).start()
    threading.Thread(target= send).start()

if __name__ == "__main__":
    main()