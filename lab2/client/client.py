import socket, sys, os

server = sys.argv[1]
port = int(sys.argv[2])
command = sys.argv[3]
filename = sys.argv[4]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

s.connect( (server, port) )

readyC = s.recv(1024).decode("UTF-8")

if command ==  "GET":
	s.send(("GET"+filename).encode("UTF-8"))

	error = s.recv(1024).decode("UTF-8")
	if error[0:5] == "ERROR":
		print(error)
		exit(0)
	else:
		pass

	data = s.recv(1024)
	size = int.from_bytes(data, byteorder='big', signed=False)

	print("client receiving file " + filename + " ("+ str(size) +" bytes)")

	f = open(filename, "wb")
	while size > 0:
		data = s.recv(min(size, 1024))
		f.write(data)
		size -= len(data)
	f.close()
	data = s.recv(min(size, 1024))
	done = s.recv(8).decode("UTF-8")
	print(done)
	#if done:
		#print("Complete")
	s.close()

elif command == "PUT":

	s.send(("PUT "+filename).encode("UTF-8"))

	okC = s.recv(1024).decode("UTF-8")

	if os.access(filename, os.R_OK):
		size = os.path.getsize(filename)
		print("client sending file " + filename + " ("+ str(size) +" bytes)")
		s.send(size.to_bytes(8, byteorder='big', signed=False))

		numBytes = s.recv(1024).decode("UTF-8")

		f = open(filename, "rb")
		
		while size > 0:
			data = f.read(1024)
			s.send(data)
			size -= len(data)
		f.close()
		s.close()
	elif not os.access(filename, os.R_OK) or not os.path.isfile(filename):
		print("does not exist”" + filename)

elif command == "DEL":
	s.send(("DEL "+filename).encode("UTF-8"))
	s.close()