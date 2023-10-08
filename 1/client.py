import socket

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(("127.0.0.1", 5000))

while True:
	send_data = input("Enter: ")
	client.send(send_data.encode("utf-8"))
	data = client.recv(1024).decode("utf-8")
	if(data == "exit"):
		break

client.close()