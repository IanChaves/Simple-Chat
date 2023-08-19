from socket import *
import sys
import pickle
import threading
import const

class RecvHandler(threading.Thread):
    def __init__(self, sock):
        threading.Thread.__init__(self)
        self.client_socket = sock

    def run(self):
        while True:
            (conn, addr) = self.client_socket.accept()
            marshaled_msg_pack = conn.recv(1024)
            msg_pack = pickle.loads(marshaled_msg_pack)
            print("\nMESSAGE FROM: " + msg_pack[1] + ": " + msg_pack[0])
            conn.send(pickle.dumps("ACK"))
            conn.close()

try:
    me = str(sys.argv[1])
except:
    print('Usage: python3 chatclient.py <Username>')
    sys.exit(1)

client_sock = socket(AF_INET, SOCK_STREAM)
my_port = const.registry[me][1]
client_sock.bind(('0.0.0.0', my_port))
client_sock.listen(5)

recv_handler = RecvHandler(client_sock)
recv_handler.start()

while True:
    dest = input("ENTER DESTINATION: ")
    msg = input("ENTER MESSAGE: ")

    if dest in const.registry:
        dest_ip, dest_port = const.registry[dest]
        server_sock = socket(AF_INET, SOCK_STREAM)
        try:
            server_sock.connect((dest_ip, dest_port))
        except:
            print("Error: Server is down or destination user is not available.")
            continue
        msg_pack = (msg, dest, me)
        marshaled_msg_pack = pickle.dumps(msg_pack)
        server_sock.send(marshaled_msg_pack)
        marshaled_reply = server_sock.recv(1024)
        reply = pickle.loads(marshaled_reply)
        if reply != "ACK":
            print("Error: Server did not accept the message (destination user may not exist).")
        server_sock.close()
    else:
        print("Error: Destination user does not exist.")
