import socket

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('127.0.0.1', 5005))
data, addr = sock.recvfrom(1024)
print(data)
print(addr)
sock.sendto("reply from server".encode(), ('127.0.0.1', 5006))
