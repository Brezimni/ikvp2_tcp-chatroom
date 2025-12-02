import socket

def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def construct_message(sender, message, namen):
    colors = {
        "navadno": "\033[34m",
        "privat": "\033[30;104m",
        "opozorilo": "\033[30;101m",
        "obvestilo": "\033[30;47m"
    }
    return f"{colors[namen]}{sender}{' <zasebno>' if namen == 'privat' else ''}\033[0m: {message}".encode()
