import socket
import sys
import helper

srv_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    srv_sock.bind(("0.0.0.0", int(sys.argv[1])))
    srv_sock.listen(5)
except Exception as e:
    exit(1)

while True:
    print("Waiting for new client...")
        
    cli_sock, cli_addr = srv_sock.accept()
    cli_addr_str = str(cli_addr)
    try:
        print("Client " + cli_addr_str + " connected")
        bytes_read = helper.read_from_socket(cli_sock, cli_addr_str)
        if bytes_read == 0:
            print("No data recieved")
        else:
            print("recieved request: " + str(bytes_read))
    finally:
        cli_sock.close()

srv_sock.close()
exit(0)
