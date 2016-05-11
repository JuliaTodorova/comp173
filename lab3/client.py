import socket, sys, os

URL = sys.argv[1]
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect( (server, port) )

