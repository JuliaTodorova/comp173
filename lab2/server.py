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
		# Put
		data = conn.recv(8)
		size = int.from_bytes(data, byteorder='big', signed=False)
		f = open("received.jpg", "wb")
		while size > 0:
			data = conn.recv(1024)
			f.write(data)
			size -= len(data)
		f.close()
		conn.send("OK".encode("UTF-8"))
		data = conn.recv(1024)
		conn.close()
	elif command == "DEL":
		pass
