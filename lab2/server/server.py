import socket, sys, os

port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind( ("", port) )
s.listen(0)

while True:
	conn, address = s.accept()
	conn.send("READY".encode("UTF-8"))

	data = conn.recv(1024).decode("UTF-8")
	command = data[0:3]
	filename = data[3:]
	if command == "GET":
		if os.access(filename, os.R_OK):
			conn.send("OK".encode("UTF-8"))
			
			size = os.path.getsize(filename)
			conn.send(size.to_bytes(1024, byteorder='big', signed=False))
			f = open(filename, "rb")

			while size > 0:
				data = f.read(1024)
				conn.send(data)
				size -= len(data)
			f.close()
			conn.send("DONE".encode("UTF-8"))
			conn.close()

		elif (not os.path.isfile(filename)):
			conn.send(("ERROR: "+filename+" does not exist").encode("UTF-8"))
			conn.close()

	elif command == "PUT":
		conn.send("OK".encode("UTF-8"))
		
		data = conn.recv(1024)
		size = int.from_bytes(data, byteorder='big', signed=False)
		print(size)
		conn.send("OK".encode("UTF-8"))

		f = open(filename, "wb")
		while size > 0:
			data = conn.recv(1024)
			f.write(data)
			size -= len(data)
		f.close()
		data = conn.recv(1024)
		conn.send("DONE".encode("UTF-8"))
		conn.close()

	elif command == "DEL":
		if os.path.exists(filename):
			os.remove(filename)
		conn.close()