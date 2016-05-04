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

	data = s.recv(1024)
	size = int.from_bytes(data, byteorder='big', signed=False)
	
	f = open(filename, "wb")
	while size > 0:
		data = s.recv(1024)
		f.write(data)
		size -= len(data)
	f.close()
	data = s.recv(1024)
	s.close()

elif command == "PUT":
	s.send(("PUT"+filename).encode("UTF-8"))

	if not os.access(filename, os.R_OK) or not os.path.isfile(filename):
		print("No access to file: " + filename)

	size = os.path.getsize(filename)
	s.send(size.to_bytes(8, byteorder='big', signed=False))
	f = open(filename, "rb")
	
	while size > 0:
		data = f.read(1024)
		s.send(data)
		size -= len(data)
	f.close()
	s.close()
	
elif command == "DEL":
	s.send(("DEL"+filename).encode("UTF-8"))
	s.close()