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

print("/w <nick>\n/m <msg>: whisper to nick")
print("/roll <repetições>* <dado> <buff/nerf>* : Joga um <dado>")
print("/help roll: para mais detalhes")
print("/e: exit")

inp = input("Digite mensagens:\n")

while True:
    if(inp == "/e"):
        receiver.running = False
        s.close()
        raise Exception("FECHA")

    elif(inp.startswith("/w")):
        st = "/w"
        for i in range(2, len(inp)):
            if (inp[i] == '/' and inp[i + 1] == 'm'):
                st += "/m " + name + ": " + inp[i + 2::]
                s.send(bytes(st, "UTF8"))
                break
            else:
                st += inp[i]

    elif(inp.startswith("/roll")):
        result = proxy.roll(inp, name)
        print(result)
        s.send(bytes(result, "UTF8"))

    elif(inp.startswith("/help")):
        if("roll" in inp):
            print("Roll help")
            str = "'.roll <repetições>* <dado> <buff/nerf>*' : Joga um <dado>\n" \
                  "Pode-se jogar diversos dados em apenas um comando, basta repetir\n" \
                  "o parâmetro <dado> quantas vezes quiser. Podendo, para cada <dado>,\n" \
                  "especificar o numero de <repetições> e/ou seu respectivo <buff/nerf>\n" \
                  "Exemplos: '.roll d2' '.roll 2 d6' '.roll d10 4' '.roll d4 -1'\n" \
                  "'.roll 3 d20 +2' '.roll 2 d4 d6 5 3 d10 *1.2'\n" \
                  "Dica: pode-se escrever '.roll 3x d6 -2, 2x d20 +3' para facilitar o entendimento\n\n" \
                  "*Parâmetros*\n" \
                  "<dado> : Um <dado> é definido por 'dX' onde 'X' é um numero inteiro,\n" \
                  "correspondente a quantidade de lados do dado\n" \
                  "<repetições> *Opcional: Número de vezes que se pretende lançar o dado.\n" \
                  "Caso seja omitido será considerado 1\n" \
                  "<buff/nerf> *Opcional: Caso precise mudar o resultado do dado de alguma\n" \
                  "maneira, para buffar ou nerfar a ação do jogador, pode usar um 'oX' onde 'o'\n" \
                  "é um operador matemático(operadores suportados: [+, -, *, x, /, ^, %])\n" \
                  "e 'X' um numero real(casas decimais são aceitas).\n" \
                  "Caso seja omitido será considerado um lançamento normal\n\n"
            print(str)

    else:
        s.send(bytes(name + ": " + inp, "UTF8"))

    inp = input()
