import socket

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 5000))
server.listen()

while True:
	user, address = server.accept()
	print("Connected by ", address)

	while True:
		data = user.recv(1024).decode("utf-8")
		print("received data from client: ", data)
		user.send(data.encode("utf-8"))
		if(data == "exit"):
			break
			
	user.close()
server.close()