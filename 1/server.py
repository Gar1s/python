import socket
import datetime

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind(("127.0.0.1", 5000))
server.listen()

while True:
	user, address = server.accept()
	print("Connected by ", address)
	data = user.recv(1024).decode("utf-8")
	current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
	print("received data from client: ", data)
	print("time: ", current_time)
	user.close()
server.close()