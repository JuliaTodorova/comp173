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
else:
	count = MAX_LEN - 4

data[1] = count

j = 2
for i in range(0, count):
	if(i % 2 == 0):
		data[j] = (int(sys.argv[i + 4])) << 4
	else:
		data[j] = data[j] | int(sys.argv[i + 4])
		j = j + 1

s.sendall(data)

data = s.recv(2048)

finalResult = (int(data[0])) << 24
finalResult += (int(data[1])) << 16
finalResult += (int(data[2])) << 8
finalResult += (int(data[3]))

if (finalResult >= (2**31)):
	finalResult -= (2**32)

print(finalResult)



