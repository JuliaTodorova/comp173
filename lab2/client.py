import socket, sys, os

server = sys.argv[1]
port = int(sys.argv[2])
command = sys.argv[3]
filename = sys.argv[4]

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

if not os.access(filename, os.R_OK) or not os.path.isfile(filename):
	print("No access to file: " + filename)
	sys.exit(1)

s.connect((server, port))

readyC = s.recv(1024).decode("UTF-8")

if command ==  "GET":
	s.send("GET".encode("UTF-8"))
elif command == "PUT":
	s.send("PUT".encode("UTF-8"))
	okC = s.recv(1024).decode("UTF-8")	

elif command == "DEL":
	s.send("DEL".encode("UTF-8"))

s.close()