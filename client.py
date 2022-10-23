import socket
import sys
import helper

cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
srv_addr = (sys.argv[1], int(sys.argv[2]))
srv_addr_str = str(srv_addr)

try:
    print("Connecting to " + srv_addr_str + "... ")
    cli_sock.connect(srv_addr)
    print("Connected")
except Exception as e:
    print(e)
    exit(1)
    
try:
    while True:
        bytes_sent = message_to_socket("hello server", srv_sock)
        if bytes_sent == 0:
            print("User-requested exit.")
            break
            
        bytes_read = socket_to_screen(cli_sock, srv_addr_str)
        if bytes_read == 0:
            print("Server closed connection.")
            break
            
finally:
    cli_sock.close()
    exit(0)
    