import socket, sys, os

port = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind( ("", port) )
s.listen(3)

while True:
	conn, address = s.accept()
	conn.send("READY".encode("UTF-8"))

	command = conn.recv(1024).decode("UTF-8")
	print("mah command be:", command)
	if command == "GET":
		print("gimme gimme gimme GET")
	
	elif command == "PUT":
		print("but mommy I want to PUT")
		data = conn.recv(1024)
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
		name = conn.recv(1024).decode("UTF-8")
		print("doing the DEL")
		if os.path.exists(name):
			print("found dat file yo")
			os.remove(name)
		else:
			print("file does not exist")	
