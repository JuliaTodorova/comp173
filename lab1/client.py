import sys, socket 

server = sys.argv[1]
port = int(sys.argv[2])
operation = sys.argv[3]

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.connect((server,port))

data = bytearray(7)

if operation == "+":
	data[0] = 2**0
elif operation == "-":
	data[0] = 2**1
elif operation == "*":
	data[0] = 2**2

MAX_LEN = 14

if len(sys.argv) <= MAX_LEN:
	count = len(sys.argv) - 4
else
	count = MAX_LEN - 4

j = 2
for i in range(4, count):
	if(i % 2 = 0){
		data[j] = (int(sys.argv[i])) << 4
	}
	else
		data[j] = data[j] | sys.argv[i]
		j = j + 1

s.sendall(data)

data = s.recv(1024)
data = int(data[0])

print(data)



