import socket
import sys
import helper
import os

def list_dir(sock):
    msg = "server contents:\n"
    for f in os.listdir():
        msg += "    " + str(f) + "\n"
    helper.message_to_socket(msg, sock)

def get_sent_file(sock):

    return

def send_file(sock):

    return

def get_request(sock):
    msg = helper.read_string(sock)
    print("message from client: " + msg)
    if msg == "ls":
        list_dir(sock)
    else:
        print("unrecognized command: " + msg)
        helper.message_to_socket("unrecognized command. supported:  [ls] [sendfile] [recvfile]", sock)


#server app

ip_val = "0.0.0.0"
soc_val = 0

srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    if len(sys.argv) < 2:
        raise Exception("invalid args: need [socket]")
    sock_val = int(sys.argv[1]);
    srv_sock.bind((ip_val, sock_val))
    srv_sock.listen(5)
except Exception as e:
    print(e)
    exit(1)

print(f"Sever up and running. /n IP: {ip_val}, Socket: {soc_val}")
while True:
    print("waiting for client...")
    cli_sock, cli_addr = srv_sock.accept()
    cli_addr_str = str(cli_addr)
    try:
        print("Client " + cli_addr_str + " connected")
        m = get_request(cli_sock)
    finally:
        cli_sock.close()

srv_sock.close()

exit(0)

