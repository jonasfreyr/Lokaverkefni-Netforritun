import socket
import _thread


HOST = "127.0.0.1"
PORT = 65432

conns = []
nicks = {}

def new_client(conn, addr):
    print("Connection started with:", addr)

    msg = str(["c", nicks[conn]])
    for a in conns:
        if a != conn:
            a.sendall(msg.encode())

    users = []
    for a in nicks:
        if a != conn:
            users.append(nicks[a])
    conn.sendall(str(users).encode())

    while True:
        try:
            data = conn.recv(1024)
            a = eval(data.decode())

            if a[0] == "cn":
                nicks[conn] = a[2]

            print(nicks)
            print(data.decode())

        except:
            print("Connection ended with:", addr)
            msg = str(["dc", nicks[conn]]).encode()
            for a in conns:
                if a != conn:
                    a.sendall(msg)
            conns.remove(conn)
            del nicks[conn]
            break

        for a in conns:
            if a != conn:
                a.sendall(data)



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
