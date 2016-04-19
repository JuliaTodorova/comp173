import sys, socket

port = int(sys.argv[1])
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(("", port))

while True:

	rawData, address = s.recvfrom(2048)

	argLen = int(rawData[1]) - 1
	leftMask = (2**4) - 1
	
	result = (int(rawData[2])) >> 4
	j = 2
	for i in range(0, argLen):
		if(i % 2 == 0):
			if(int(rawData[0]) == 2**0):
				result += (int(rawData[j])) & leftMask
			elif(int(rawData[0]) == 2**1):
				result -= (int(rawData[j])) & leftMask
			elif(int(rawData[0]) == 2**2):
				result *= (int(rawData[j])) & leftMask
			j = j + 1
		else:
			if(int(rawData[0]) == 2**0):
				result += (int(rawData[j])) >> 4
			elif(int(rawData[0]) == 2**1):
				result -= (int(rawData[j])) >> 4
			elif(int(rawData[0]) == 2**2):
				result *= (int(rawData[j])) >> 4

	byteArray = bytearray(4)

	rightMask = (2**8) - 1

	byteArray[0] = rightMask & (result >> 24)
	byteArray[1] = rightMask & (result >> 16)
	byteArray[2] = rightMask & (result >> 8)
	byteArray[3] = rightMask & result 

	s.sendto(byteArray, address)