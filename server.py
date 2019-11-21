import Pyro4
import socket
from threading import Thread
import re

connections = []
TCP_PORT = 5005
MSG_SIZE = 1024

def removeCon(x):
    connections.remove(x)

class Th(Thread):
    def __init__(self, con, id):
        Thread.__init__(self)
        self._con = con
        self.name = self._con.recv(MSG_SIZE).decode("utf-8")
        self.running = True
        self.id = id

    def send(self, msg):
        self._con.send(msg)

    def run(self):
        data = []
        while self.running:
            try:
                msg = self._con.recv(MSG_SIZE).decode("utf-8")

                if (msg[0:2] == "/w"):
                    nick = msg[2:re.search(r"/m", msg).start()].strip()

                    for c in connections:
                        if (c.name == nick):
                            c.send(bytes("(whisper)" + msg[re.search(r"/m", msg).end()::].strip(), "UTF8"))
                            break
                else:
                    for c in connections:
                        if (c.name != self.name):
                            c.send(bytes(msg, "UTF8"))

            except Exception as error:
                print("Error: " + error.__str__())
                print("Ended", self.id)
                self._con.close()
                self.running = False
                self.name = None
                removeCon(self)

# ending class

@Pyro4.expose
class PyroClass(object):
    def a(self):
        return "a"

# ending class

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(("localhost", TCP_PORT))

daemon = Pyro4.Daemon()                # make a Pyro daemon
uri = daemon.register(PyroClass)       # register the greeting maker as a Pyro object
class thDaemon(Thread):
    def __init__(self, daemon):
        Thread.__init__(self)
        self.daemon = daemon

    def run(self):
        self.daemon.requestLoop()

thDaemon(daemon).start()

print("Server funcionando")

id = 0
while True:
    s.listen(id)
    id += 1
    con, addr = s.accept()
    print("Connected", id)
    print('Connection address:', addr)

    con.send(bytes(uri.asString(), "UTF8"))

    connections.append(Th(con, id))
    connections[-1].start()

"""
async def roll(ctx):
    
    content = ctx.message.content
    indice = -1
    faceDados = []
    vezes = []
    multiplicadores = []

    while True:
        numero = re.search(r"\d+[.\|,]?\d*", content)
        if(numero is None):
            break

        if(content[numero.start()-1] == "d"):
            if(indice == -1): #primeira inserção
                indice += 1
                faceDados.append(math.trunc(float(numero[0].replace(",", "."))))
                vezes.append(1)
                multiplicadores.append("+0")
            elif(faceDados[indice] is None): #bloco já setado
                faceDados[indice] = math.trunc(float(numero[0].replace(",", ".")))
            else: #novo bloco
                indice += 1
                faceDados.append(math.trunc(float(numero[0].replace(",", "."))))
                vezes.append(1)
                multiplicadores.append("+0")

        elif(content[numero.start()-1] in ["+", "-", "*", "/", "x", "^", "%"]):
            multiplicador = content[numero.start()-1:numero.end()].replace(",", ".")
            if(multiplicador.endswith(".")):
                multiplicador = multiplicador[:-1]

            if (indice == -1):  # primeira inserção
                indice += 1
                faceDados.append(None)
                vezes.append(1)
                multiplicadores.append(multiplicador)
            elif (multiplicadores[indice] == "+0"):  # bloco já setado
                multiplicadores[indice] = multiplicador
            else:  # novo bloco
                indice += 1
                faceDados.append(None)
                vezes.append(1)
                multiplicadores.append(multiplicador)

        else:
            if (indice == -1):  # primeira inserção
                indice += 1
                faceDados.append(None)
                vezes.append(math.trunc(float(numero[0].replace(",", "."))))
                multiplicadores.append("+0")
            elif (vezes[indice] == 1):  # bloco já setado
                vezes[indice] = math.trunc(float(numero[0].replace(",", ".")))
            else:  # novo bloco
                indice += 1
                faceDados.append(None)
                vezes.append(math.trunc(float(numero[0].replace(",", "."))))
                multiplicadores.append("+0")

        content = content[numero.end():]

    ret = "Resultados para " + ctx.author.mention + ":\n"

    for i in range(len(faceDados)):
        d = faceDados[i]
        soma = 0
        if(multiplicadores[i] in ["+0", "-0", "*1", "x1", "/1", "^1"]):
            ret += "**d" + str(d) + "** ["
        else:
            ret += "**d" + str(d) + "** " + multiplicadores[i] + " ["
        for j in range(vezes[i]):
            if(d == 0):
                valor = 0
            else:
                valor = (random.randint(0, d * 10) % d) + 1

            if   (multiplicadores[i].startswith("+")):
                valor = round(float(valor) + float(multiplicadores[i][1:]))
            elif (multiplicadores[i].startswith("-")):
                valor = round(float(valor) - float(multiplicadores[i][1:]))
            elif (multiplicadores[i].startswith("*") or multiplicadores[i].startswith("x")):
                valor = round(float(valor) * float(multiplicadores[i][1:]))
            elif (multiplicadores[i].startswith("/")):
                valor = round(float(valor) / float(multiplicadores[i][1:]))
            elif (multiplicadores[i].startswith("^")):
                valor = round(float(valor) ** float(multiplicadores[i][1:]))
            elif (multiplicadores[i].startswith("%")):
                valor = round(float(valor) % float(multiplicadores[i][1:]))

            soma += valor
            ret += str(valor) + ", "
        ret = ret[:-2] + "]\n"
        if(vezes[i] != 1):
            ret += "Total: " + str(soma) + "\n"

    await ctx.send(ret)
    """




