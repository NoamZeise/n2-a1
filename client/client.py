import socket
import sys
import helper

#client app

def send_request(srv_addr, req):
    try:
        cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_addr_str = str(srv_addr)
        print("Connecting to " + srv_addr_str + "... ")
        cli_sock.connect(srv_addr)
        print("Connected")
    except Exception as e:
        print(e)
    try:
        bytes_sent = helper.message_to_socket(request, cli_sock)
        if bytes_sent == 0:
            print("0 bytes sent")
            
        bytes_read = helper.read_from_socket(cli_sock, srv_addr_str)
        if bytes_read == 0:
            print("0 bytes read")
            
    finally:
        cli_sock.close()

if len(sys.argv) < 3:
    print("invalid args: need [address] [socket]")
    exit(1)
srv_addr = (sys.argv[1], int(sys.argv[2]))
            
while True:
    request = input("request: ")
    print("sending request")
    send_request(srv_addr, request)
    print("request complete")
