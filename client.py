import Pyro4
import socket
from threading import Thread

TCP_PORT = 5005
MSG_SIZE = 1024

class Th(Thread):
    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock
        self.running = True

    def run(self):
        while self.running:
            data, addr = self.sock.recvfrom(1024)
            data = data.decode("utf-8")  # buffer size is 1024 bytes
            print(data)

# ending class

serverIP = input("Digite o IP do servidor:\n")
name = input("Digite seu nome no chat:\n")

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((serverIP, TCP_PORT))
s.send(bytes(name, "UTF8"))
uri = s.recvfrom(1024)[0]
uri = uri.decode("utf-8")

proxy = Pyro4.Proxy(uri)         # get a Pyro proxy to the greeting object

receiver = Th(s)
receiver.start()

print("/w [nick] /m [msg]: whisper to nick /roll")
print("/e: exit")

inp = input("Digite mensagens:\n")

while True:
    if(inp == "/e"):
        receiver.running = False
        s.close()
        raise Exception("FECHA")

    if(inp[0:2] == "/w"):
        st = "/w"
        for i in range(2, len(inp)):
            if (inp[i] == '/' and inp[i + 1] == 'm'):
                st += "/m " + name + ": " + inp[i + 2::]
                # print(st)
                s.send(bytes(st, "UTF8"))
                break
            else:
                st += inp[i]

    if(inp.startswith("/roll")):
        ue = Pyro4.Proxy(uri).a
        print(ue)

    else:
        s.send(bytes(name + ": " + inp, "UTF8"))

    inp = input()
