import sys
import socket
import os
import errno

#============helper===========

GET_CMD = "get"
PUT_CMD = "put"
def parse_request(sock, req, list_fn, get_fn, put_fn):
    parts = req.split(" ")
    if len(parts) == 0:
        return "no args in request"
    else:
        if parts[0] == "list":
            return list_fn(sock)
        elif parts[0] == GET_CMD:
            if len(parts) == 1:
                return GET_CMD + ": missing filename arg"
            return get_fn(sock, req[len(GET_CMD) + 1:])
        elif parts[0] == PUT_CMD:
            if len(parts) == 1:
                return PUT_CMD + ": missing filename arg"
            return put_fn(sock, req[len(PUT_CMD) + 1:])
        else:
            return "unrecognized command.\nsupported commands:\n    list\n    get [filename]\n    put [filename]"

RECV_SIZE = 4096

def read_binary(socket):
    return socket.recv(RECV_SIZE)

def read_binary_sized(socket, byte_count):
    data = bytes()
    while byte_count > 0:
        data += socket.recv(RECV_SIZE)
        byte_count -= RECV_SIZE
    return data

def read_string(socket):
    return read_binary(socket).decode()

def send_binary(data, socket):
    return socket.sendall(data);
    
def send_string(msg, socket):
    return send_binary(str.encode(msg), socket)

def get_file_data(filename):
    f = open(filename, "rb")
    data = f.read()
    f.close()
    return data

def save_file_data(filename, data):
    handle = os.open(filename, os.O_CREAT | os.O_EXCL | os.O_WRONLY)  # open only if file does not exist
    with os.fdopen(handle, "wb") as f:
        f.write(data)

def send_file(socket, filename):
    try:
        data = get_file_data(filename)
    except OSError as e:
        if e.errno == errno.ENOENT:
            err = f"err: File {filename} does not exist"
            send_string(err, socket)
            return err
        raise e
    send_string(str(len(data)), socket)    
    print("sending file...")
    read_binary(socket) #sync with recv
    send_binary(data, socket)
    err = read_string(socket)
    if not err.startswith("success"):
        return err

def recv_file(socket, filename):
    filesize = read_string(socket)
    if filesize.startswith("err"):
        return filesize
    send_string("ready", socket) #sync with send
    print("recieving file...")
    data = read_binary_sized(socket, int(filesize))
    if str(len(data)) != filesize:
        return "err: peer timed out"  # assuming missing data means other party is offline
    err = None
    try:
        save_file_data(filename, data)
    except OSError as e:
        if e.errno == errno.EEXIST:
            err = "err: did not write, file already exists"
        else:
            raise e
    if err == None:
        send_string("success", socket)
    else:
        send_string(err, socket) #propagate error to peer
    return err
