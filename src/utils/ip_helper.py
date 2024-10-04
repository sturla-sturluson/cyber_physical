import socket

def get_local_ip()->str:
    ip_address = ""

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.connect(("8.8.8.8", 80))
        text = s.getsockname()[0]
        ip_address = text

    return ip_address