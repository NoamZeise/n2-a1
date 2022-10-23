import sys
import socket

def read_from_socket(socket, sock_addr):
    print(sock_addr + ": ", end="", flush=True) 
    data = bytearray(1)
    bytes_read = 0
    while len(data) > 0 and "\n" not in data.decode():
        data = socket.recv(4096);
        print(data.decode(), end="")
        bytes_read += len(data)
        return bytes_read


def binary_to_socket(data, socket):
    return socket.sendall(data);
    
def message_to_socket(msg, socket):
    return binary_to_socket(str.encode(msg), socket)
