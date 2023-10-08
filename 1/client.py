import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5000))

send_data = input("Enter: ")
client.send(send_data.encode("utf-8"))

data = client.recv(1024).decode("utf-8")
if data:
	print("data = ", data)
	client.send("Data is cleared!".encode("utf-8"))
else: 
	client.send("Data is damaged!".encode("utf-8"))
client.close()