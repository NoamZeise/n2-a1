import socket
import sys
import os
import helper

#=========server========

def list_dir(sock):
    msg = "server contents:\n"
    for f in os.listdir():
        msg += "    " + str(f) + "\n"
    helper.send_string(msg, sock)
    print("client served: sent file listing")

def put_file(sock, name):
    helper.send_string("ready", sock) #sync (with client.put_file())
    err = helper.recv_file(sock, name)
    if err == None:
        print("client served: added file to server")
    return err

def get_file(sock, name):
    err = helper.send_file(sock, name)
    if err == None:
        print("client served: sent file to client")
    return err

def handle_request(sock):
    request = helper.read_string(sock)
    print("request recieved: " + request)
    if request == "shutdown":
        return 1
    error = helper.parse_request(sock, request, list_dir, get_file, put_file)
    if error != None:
        print("client request error: " + error)

#=============main=============
ip_val = "0.0.0.0"
if len(sys.argv) < 2:
    print("invalid args: need [socket]")
    exit(1)

sock_val = int(sys.argv[1]);
srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    srv_sock.bind((ip_val, sock_val))
    srv_sock.listen(5)
except Exception as e:
    print(e)
    exit(1)

print(f"Sever up and running. \nIP: {ip_val}, Socket: {sock_val}")
while True:
    print("\nwaiting for client...")
    cli_sock, cli_addr = srv_sock.accept()
    print("Client " + str(cli_addr) + " connected")
    try:
        if handle_request(cli_sock) == 1:
            break
    except Exception as e:
        print("Server error: " + str(e))
    finally:
        cli_sock.close()
srv_sock.close()
