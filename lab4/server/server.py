import threading, socket, sys, os, queue, time

class ClientHandler(threading.Thread):
    def __init__(self, conn):
        threading.Thread.__init__(self)
        self.conn = conn
    def run(self):
        self.conn.send("READY".encode("UTF-8"))
        readyC = self.conn.recv(1024).decode("UTF-8")
        dataArray = readyC.split()
        command = dataArray[0]
        filename = dataArray[1]

        if command == "GET":
            if os.access(filename, os.R_OK):
                self.conn.send("OK".encode("UTF-8"))
                ready = self.conn.recv(1024).decode("UTF-8")

                size = os.path.getsize(filename)
                self.conn.send(size.to_bytes(8, byteorder='big', signed=False))

                ok = self.conn.recv(1024).decode("UTF-8")

                f = open(filename, "rb")
                while size > 0:
                    data = f.read(1024)
                    self.conn.send(data)
                    size -= len(data)
                f.close()
                self.conn.send("DONE".encode("UTF-8"))
                self.conn.close()

            elif (not os.path.isfile(filename)):
                self.conn.send(("ERROR: "+filename+" does not exist").encode("UTF-8"))
                self.conn.close()

        elif command == "PUT":
            self.conn.send("OK".encode("UTF-8"))

            data = self.conn.recv(1024)
            size = int.from_bytes(data, byteorder='big', signed=False)
            f = open(filename, "wb")
            while size > 0:
                data = self.conn.recv(1024)
                f.write(data)
                size -= len(data)
            f.close()
            data = self.conn.recv(1024)
            self.conn.send("DONE".encode("UTF-8"))
            self.conn.close()

        elif command == "DEL":
            if os.path.exists(filename):
                os.remove(filename)
                self.conn.send("DONE".encode("UTF-8"))
            self.conn.close()

class Manager(threading.Thread):
    def __init__(self, maxClient):
        threading.Thread.__init__(self)
        self.maxClient = maxClient
        self.q = queue.Queue()
        self.running = set()

    def add(self, client):
        self.q.put(client)

    def run(self):
        while True:
                kick = []
                for t in self.running:
                    if not t.isAlive(): kick.append(t)
                for t in kick:
                    self.running.remove(t)
                if len(self.running) < self.maxClient:
                    if self.q.qsize() > 0:
                        t = self.q.get()
                        self.running.add(t)
                        t.start()
                    time.sleep(1)

if __name__== "__main__":
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    port = int(sys.argv[1])
    maxClient = int(sys.argv[2])

    s.bind( ("", port) )
    s.listen(0)

    manager = Manager(maxClient)
    manager.start()

    while True:
        conn, address = s.accept()
        t = ClientHandler(conn)
        manager.add(t)
