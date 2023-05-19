import socket

client_sock = socket.socket()
client_sock.connect(('localhost', 9090))

while True:
	comand = input(">>")
	client_sock.send(comand.encode())
	data = client_sock.recv(1024).decode()
	if not data:
		print("Сеанс завершён\n")
		break
	else:
		print(data)
			

client_sock.close()
