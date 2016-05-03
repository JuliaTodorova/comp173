import socket, sys

port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind( ("", port) )
s.listen(3)

while True:
	conn, address = s.accept()
	conn.send("READY".encode("UTF-8"))

	command = conn.recv(1024).decode("UTF-8")

	if command == "GET":
		pass
	elif command == "PUT":
		conn.send("OK".encode("UTF-8"))
	elif command == "DEL":
		pass
