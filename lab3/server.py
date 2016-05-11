import socket, sys, os

URL = int(sys.argv[1])

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind( ("", port) )
s.listen(0)

