from socket import *
import pickle
import threading
import const

# Store the registered users and their addresses
user_registry = {}  # Format: {username: (ip, port)}

# Function to handle client communication
def handle_client(client_sock, addr):
    while True:
        marshaled_msg_pack = client_sock.recv(1024)
        if not marshaled_msg_pack:
            break
        msg_pack = pickle.loads(marshaled_msg_pack)
        msg = msg_pack[0]
        dest = msg_pack[1]
        src = msg_pack[2]
        
        print("RELAYING MSG: " + msg + " - FROM: " + src + " - TO: " + dest)
        
        if dest in user_registry:
            dest_addr = user_registry[dest]
            client_sock.send(pickle.dumps("ACK"))
            
            dest_ip = dest_addr[0]
            dest_port = dest_addr[1]
            try:
                client_to_dest_sock = socket(AF_INET, SOCK_STREAM)
                client_to_dest_sock.connect((dest_ip, dest_port))
                msg_pack = (msg, src)
                marshaled_msg_pack = pickle.dumps(msg_pack)
                client_to_dest_sock.send(marshaled_msg_pack)
                marshaled_reply = client_to_dest_sock.recv(1024)
                reply = pickle.loads(marshaled_reply)
                if reply != "ACK":
                    print("Error: Destination client did not receive message properly")
            except:
                print("Error: Failed to send message to destination client")
            finally:
                client_to_dest_sock.close()
        else:
            client_sock.send(pickle.dumps("NACK"))

    client_sock.close()

def main():
    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind(('0.0.0.0', const.CHAT_SERVER_PORT))
    server_sock.listen(5)
    
    print("Chat Server is ready...")
    
    while True:
        (conn, addr) = server_sock.accept()
        
        marshaled_msg_pack = conn.recv(1024)
        msg_pack = pickle.loads(marshaled_msg_pack)
        msg_type = msg_pack[0]
        username = msg_pack[1]
        user_registry[username] = addr
        
        conn.send(pickle.dumps("ACK"))
        conn.close()
        
        threading.Thread(target=handle_client, args=(socket(AF_INET, SOCK_STREAM), addr)).start()

if __name__ == "__main__":
    main()
