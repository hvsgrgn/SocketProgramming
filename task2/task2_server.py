import socket
import sys
import select
import struct

#valasz formatum
recv_packer = struct.Struct("3s i i i")

#parancssori adatok
TCP_IP, TCP_PORT, ID = sys.argv[1], int(sys.argv[2]), sys.argv[3]

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((TCP_IP, TCP_PORT))
server.listen()

matrix = [[0, 0, 0], [0, 0, 0], [0, 0, 0]]

players = {}

inputs = [server]
timeout = 5.0

while True:
    try:
        readables, _, _ = select.select(inputs, [], [], timeout)

        for s in readables:
            if s is server:
                client_socket, addr = server.accept()
                print("Kapcsolódott:", addr)
                inputs.append(client_socket)
            else:
                data = s.recv(recv_packer.size)

                if not data:
                    inputs.remove(s)
                    s.close()
                    continue

                op, r, c, v = struct.unpack("3s i i i", data)
                op = op.decode().strip('\x00')

                if(op == "SET"):
                    matrix[r][c] = v
                    print(f"\nrow, column, value: {r}, {c}, {v} : {matrix[r][c]}\n")
                    s.send(struct.pack("i", v))

                elif(op == "GET") :
                    field = matrix[r][c]
                    print(f"\nrow, column, value: {r}, {c} : {field}\n")
                    s.send(struct.pack("i", field))

                elif(op == "SUM") :
                    sum = 0
                    for row in matrix:
                        for column in row:
                            sum += column
                    print(f"\nsum: {sum}\n")
                    s.send(struct.pack("i", sum))

    except KeyboardInterrupt:
        for s in inputs:
            s.close()
        print("Server closing")
        break



#----------------------------------------------------------------

