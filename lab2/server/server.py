import socket, sys, os

port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind( ("", port) )
s.listen(3)

while True:
	conn, address = s.accept()
	conn.send("READY".encode("UTF-8"))

	data = conn.recv(1024).decode("UTF-8")
	command = data[0:3]
	filename = data[3:]

	if command == "GET":

		size = os.path.getsize(filename)
		conn.send(size.to_bytes(8, byteorder='big', signed=False))
		f = open(filename, "rb")

		while size > 0:
			data = f.read(1024)
			conn.send(data)
			size -= len(data)
		f.close()
		conn.close()

	elif command == "PUT":
		data = conn.recv(1024)
		size = int.from_bytes(data, byteorder='big', signed=False)
		
		f = open(filename, "wb")
		while size > 0:
			data = conn.recv(1024)
			f.write(data)
			size -= len(data)
		f.close()
		data = conn.recv(1024)
		conn.close()

	elif command == "DEL":
		if os.path.exists(filename):
			os.remove(filename)