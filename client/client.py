import socket
import sys
import helper

#==========client============

def get_file(sock, name):
    err = helper.recv_file(sock, name)
    if err == None:
        print("successfully got file from server")
    return err

def put_file(sock, name):
    helper.read_binary(sock) #sync (with server.put_file())
    err = helper.send_file(sock, name)
    if err == None:
        print("successfully put file on server")
    return err
    
def send_request(srv_addr, req):
    try:
        cli_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        srv_addr_str = str(srv_addr)
        cli_sock.connect(srv_addr)
        print("Connected to " + srv_addr_str + "... ")
        helper.send_string(req, cli_sock)
        if req == "shutdown":
            return 1
        error = helper.parse_request(cli_sock, req, lambda sock: print(helper.read_string(sock), end=""), get_file, put_file)
        if error != None:
            print("Request Error: " + error)
    except Exception as e:
        print(e)
    finally:
        cli_sock.close()
        
#==========main============
if len(sys.argv) < 3:
    print("invalid args: need [hostname] [port] [command]")
    exit(1)
srv_addr = (sys.argv[1], int(sys.argv[2]))

if len(sys.argv) == 3:
    print("in interactive mode, [exit] to close")
    while True:
        request = input("\nrequest: ")
        if request == "exit":
            break
        if send_request(srv_addr, request) == 1:
            break
    exit(1)

cmd = sys.argv[3]
i = 4
while i < len(sys.argv):
    cmd += " " + sys.argv[i]
    i+=1
send_request(srv_addr, cmd)
