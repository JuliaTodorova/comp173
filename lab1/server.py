import sys, socket

port = int(sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))

while True:

	rawData, address = s.recvfrom(1024)

	if int(rawData[0]) == 2**0:
		result = int(rawData[1]) + int(rawData[2])
	elif int(rawData[0]) == 2**1:
		result = int(rawData[1]) - int(rawData[2])
	elif int(rawData[0]) == 2**2:
		result = int(rawData[1]) * int(rawData[2])

	byteArray = bytearray(4)

	byteArray[0] = result		
	s.sendto(byteArray, address)
