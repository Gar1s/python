import socket
import datetime
import time

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 5000))
server.listen()

while True:
	user, address = server.accept()
	print("Connected by ", address)

	data = user.recv(1024).decode("utf-8")
	time.sleep(5)
	print("received data from client: ", data)

	user.send(data.encode("utf-8"))

	response = user.recv(1024).decode("utf-8")
	print("response: ", response)
	
	user.close()
server.close()