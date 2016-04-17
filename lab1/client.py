import sys, socket 

server = sys.argv[1]
port = int(sys.argv[2])

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.connect((server,port))

data = bytearray(4)

if sys.argv[3] == "+":
	data[0] = 2**0
elif sys.argv[3] == "-":
	data[0] = 2**1
elif sys.argv[3] == "*":
	data[0] = 2**2

data[1] = int(sys.argv[4])
data[2] = int(sys.argv[5])

s.sendall(data)

data = s.recv(1024)
data = int(data[0])

print(data)



