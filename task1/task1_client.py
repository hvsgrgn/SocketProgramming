from socket import socket, AF_INET, SOCK_STREAM
import random
import struct
import sys

#parancssori argumentumban kapjuk az adatot a porthoz es cimhez
USERS_IP, USERS_PORT = sys.argv[1], int(sys.argv[2])
server_addr = (USERS_IP, USERS_PORT)
#BUFFER_SIZE = 1024

#a ket kod formatuma
send_packer = struct.Struct(f"6s 20s")
print("Sending neptune code Y2V0WV and item name 'sweater'...")
data = send_packer.pack("Y2V0WV".encode(), "sweater".encode())

#elkuldjuk a tesztszervernek a ket kodolt adatot
client = socket(AF_INET, SOCK_STREAM)
client.connect(server_addr)
client.sendall(data)
print(f"\nSent: {data}\n")


#a szotarunk a kurzuskodokkal
#records = {'FI-ALG-261': 'John Carter', 'FA-HIS-262': 'Emily Watson', 'EN-MTH-261': 'Robert Hill', 'BS-MKT-262': 'Laura Green', 'FI-NET-261': 'Michael Turner'}


#megkapjuk valaszkent a keresendo kurzuskodot
resp_packer = struct.Struct("i")
response = client.recv(resp_packer.size)
response = struct.unpack("i", response)[0]
print(f"\nreceived {response}\n")
can_purchase = ""
if(int(response)  <= 6000):
    can_purchase = "purchase"
else:
    can_purchase = "back_out"

print(f"\nResponding: {can_purchase}\n")

send_packer = struct.Struct("8s")
data = send_packer.pack(can_purchase.encode())
client.sendall(data)

#varunk a valaszra
resp_packer = struct.Struct("12s")
response = client.recv(resp_packer.size).decode("utf-8")
print(f"\nReply: {response}\n")

client.close()