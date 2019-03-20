import socket
import _thread


HOST = "127.0.0.1"
PORT = 65432

conns = []
nicks = {}

def new_client(conn, addr):
    print("Connection started with:", addr)


    msg = nicks[conn] + ":" + "cn"
    for a in conns:
        if a != conn:
            a.sendall(msg.encode())

    while True:
        try:
            conn.sendall("yay!".encode())

        except:
            print("Connection ended with:", addr)
            break

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(2)

    print("Server started!")

    while True:
        conn, addr = s.accept()

        nick = conn.recv(1024).decode("utf-8")
        conns.append(conn)
        nicks[conn] = nick

        _thread.start_new_thread(new_client, (conn, addr))


