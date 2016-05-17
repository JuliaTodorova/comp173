import socket, sys, os

URL = sys.argv[1]
splitURL = URL.split("/")
webhost = splitURL[2]

if len(splitURL) == 3:
	resource = "/"
else: 
	resource = "/" + splitURL[3]

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect( (webhost, 80) )
s1.send(("GET " + resource + " HTTP/1.1\n").encode("UTF-8"))
s1.send(("Host: " + webhost + "\n\n").encode("UTF-8"))

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect( ("rtvm.cs.camosun.bc.ca", 10010) )
data = s2.recv(1024)

state = 1
previous = ""

while (state != 4):
	if (state == 1): 
		current = s1.recv(1024).decode("UTF-8")
		if ("<HTML>" in (previous + current).upper()):
			tag = (previous + current).upper().index("<HTML>")
			send = (previous + current)[tag:]
			state = 2
			previous = send
			
			if ("</HTML>" in (previous).upper()):
				tag = previous.upper().index("</HTML>")
				sendTo = previous[:tag + 7]
				s2.send(sendTo.encode("UTF-8"))
				state = 3
				previous = ""
		else:
			previous = current
	elif (state == 2): 
			current = s1.recv(1024).decode("UTF-8")
			if ("</HTML>" in (previous + current).upper()):
				tag = (previous+current).upper().index("</HTML>")
				sendTo = (previous+current)[:tag + 7]
				s2.send(sendTo.encode("UTF-8"))
				state = 3
				previous = ""
			else:
				s2.send(previous.encode("UTF-8"))
				previous = current
	elif (state == 3): 
		current = s2.recv(1024).decode("UTF-8")
		if ("COMP173" in (previous+current).upper()):
			tag = (previous+current).upper().index("COMP173")
			print((previous+current)[:tag], end='')
			state = 4
		else:
			print(previous, end='')
			previous = current
			
s1.close()
s2.close()
			
