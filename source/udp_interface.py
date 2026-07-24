import socket

def init_udp():
    
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind(('localhost', 10000))  # Bind to an available port

    return sock

def receive_message(sock):
    
    data, addr = sock.recvfrom(1260)  # Buffer size is 1260 bytes
    return data, addr

def close_udp(sock):
    sock.close()