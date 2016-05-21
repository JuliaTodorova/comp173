import socket, sys, os
GET_RESOURCE = 1
TRANSCODE = 2
PRINTING = 3
DONE = 4

URL = sys.argv[1]
splitURL = URL.split("/")
webhost = splitURL[2]

if len(splitURL) == 3:
	resource = "/"
else: 
	resource = "/" + splitURL[3]

s1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s1.connect( (webhost, 80) )
s1.send(("GET " + resource + " HTTP/1.1\n" + "Host: " + webhost + "\n\n").encode("UTF-8"))

s2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.connect( ("rtvm.cs.camosun.bc.ca", 10010) )
data = s2.recv(1024)

state = GET_RESOURCE
previous = ""

while (state != DONE):
	if (state == GET_RESOURCE): 
		current = s1.recv(1024).decode("UTF-8")
		current_window = previous + current
		if ("<HTML>" in current_window.upper()):
			tag_index = current_window.upper().index("<HTML>")
			previous = current_window[tag_index:]
			state = TRANSCODE
			
			if ("</HTML>" in (previous).upper()):
				tag_index = previous.upper().index("</HTML>")
				s2.send(previous[:tag_index + 7].encode("UTF-8"))
				state = PRINTING
				previous = ""
			
	elif (state == TRANSCODE): 
			current = s1.recv(1024).decode("UTF-8")
			current_window = previous + current
			if ("</HTML>" in current_window.upper()):
				tag_index = current_window.upper().index("</HTML>")
				s2.send(current_window[:tag_index + 7].encode("UTF-8"))
				state = PRINTING
				previous = ""
			else:
				s2.send(previous.encode("UTF-8"))
				previous = current
				
	elif (state == PRINTING): 
		current = s2.recv(1024).decode("ASCII")
		current_window = previous + current
		if ("COMP173" in current_window.upper()):
			tag_index = current_window.upper().index("COMP173")
			print(current_window[:tag_index], end='')
			state = DONE
		else:
			print(previous, end='')
			previous = current
			
s1.close()
s2.close()