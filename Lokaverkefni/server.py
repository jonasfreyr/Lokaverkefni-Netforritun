import socket
import _thread
import time

HOST = "127.0.0.1"
PORT = 65432

nicks = {}

lobby_names = ["Lobby 1", "Lobby 2", "Lobby 3"]
lobby = {}
for a in lobby_names:
    lobby[a] = []

def new_client(conn, addr):
    print("Connection started with:", addr)

    clobby = lobby_names[0]
    lobby[clobby].append(conn)

    conn.sendall(lobby_names[0].encode())
    conn.sendall(str(lobby_names).encode())

    msg = str(["c", nicks[conn]])
    for a in lobby[clobby]:
        if a != conn:
            a.sendall(msg.encode())

    users = []
    for a in lobby[clobby]:
        if a != conn:
            users.append(nicks[a])

    time.sleep(0.1)
    conn.sendall(str(users).encode())

    while True:
        try:
            send = True
            data = conn.recv(100000000)
            dataD = eval(data.decode())

            if dataD[0] == "cn":
                nicks[conn] = dataD[2]

            elif dataD[0] == "cl":
                msg = str(["dc", nicks[conn]]).encode()
                for a in lobby[clobby]:
                    if a != conn:
                        a.sendall(msg)

                lobby[clobby].remove(conn)
                clobby = dataD[2]

                users = []
                for a in lobby[clobby]:
                    if a != conn:
                        users.append(nicks[a])

                msg = ["du", users]
                conn.sendall(str(msg).encode())

                lobby[clobby].append(conn)

                msg = str(["c", nicks[conn]])
                for a in lobby[clobby]:
                    if a != conn:
                        a.sendall(msg.encode())

                send = False

            elif dataD[0] == "gu":
                for a in lobby[clobby]:
                    if nicks[a] == dataD[1]:
                        a.sendall(str(["gu", nicks[conn]]).encode())
                        break

                send = False

            elif dataD[0] == "su":
                print(data)
                for a in lobby[clobby]:
                    if nicks[a] == dataD[1]:
                        a.sendall(data)
                        break

                send = False

            print(data.decode())

        except:
            print("Connection ended with:", addr)
            msg = str(["dc", nicks[conn]]).encode()
            for a in lobby[clobby]:
                if a != conn:
                    a.sendall(msg)

            lobby[clobby].remove(conn)
            del nicks[conn]
            break

        if send == True:
            for a in lobby[clobby]:
                if a != conn:
                    a.sendall(data)



with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()

    print("Server started!")

    while True:
        conn, addr = s.accept()

        nick = conn.recv(1024).decode("utf-8")
        nicks[conn] = nick

        _thread.start_new_thread(new_client, (conn, addr))
