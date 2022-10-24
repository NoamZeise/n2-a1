import sys
import socket

#helper

def read_from_socket(socket, sock_addr):
    print(sock_addr + ": ", end="", flush=True) 
    data = bytearray(1)
    bytes_read = 0
    data = socket.recv(4096);
    print(data.decode(), end="")
    bytes_read += len(data)
    print("")
    return bytes_read


def read_string(socket):
    return read_binary(socket).decode()

def read_binary(socket):
    return socket.recv(4096)

def binary_to_socket(data, socket):
    return socket.sendall(data);
    
def message_to_socket(msg, socket):
    return binary_to_socket(str.encode(msg), socket)
