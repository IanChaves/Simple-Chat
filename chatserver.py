from socket import *
import pickle
import const
import threading

registered_users = {
    "Alice": ("10.128.0.2", 5002),
    "Bob": ("10.128.0.4", 5002),
    # Adicione mais usuários aqui
}

def handle_client(conn, addr):
    try:
        marshaled_msg_pack = conn.recv(1024)
        msg_pack = pickle.loads(marshaled_msg_pack)
        msg = msg_pack[0]
        dest = msg_pack[1]
        src = msg_pack[2]
        print("RELAYING MSG: " + msg + " - FROM: " + src + " - TO: " + dest)

        if dest in registered_users:
            dest_ip, dest_port = registered_users[dest]
            dest_sock = socket(AF_INET, SOCK_STREAM)
            dest_sock.connect((dest_ip, dest_port))
            dest_sock.send(marshaled_msg_pack)
            dest_sock.close()
        else:
            conn.send(pickle.dumps("NACK"))
            return
        conn.send(pickle.dumps("ACK"))
    except:
        pass
    finally:
        conn.close()

def main():
    server_sock = socket(AF_INET, SOCK_STREAM)
    server_sock.bind(('0.0.0.0', const.CHAT_SERVER_PORT))
    server_sock.listen(5)
    print("Chat Server is ready...")

    while True:
        try:
            conn, addr = server_sock.accept()
            client_handler = threading.Thread(target=handle_client, args=(conn, addr))
            client_handler.start()
        except KeyboardInterrupt:
            print("Server shutting down...")
            break

if __name__ == "__main__":
    main()
