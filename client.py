import socket
import time
import threading

def func():
    pass

class BaseClient:
    def __init__(self, timeout:int=10, buffer:int=1024):
        self.__socket = None
        self.__address = None
        self.__timeout = timeout
        self.__buffer = buffer

    def connect(self, address, family:int, typ:int, proto:int):
        self.__address = address
        self.__socket = socket.socket(family, typ, proto)
        self.__socket.settimeout(self.__timeout)
        self.__socket.connect(self.__address)

    def send(self, message:str=""):
        #文字列送信方式
        #print('send_th')
        self.__socket.send(message.encode('utf-8'))
        message_recv = self.__socket.recv(self.__buffer).decode('utf-8')
        self.received(message_recv)
        

    def send_th(self, message:str="") -> None:
        print('send:'+message)
        th = threading.Thread(target = self.send_th, args = ([message]))
        print(th)
        th.start()

    def send_sample(self, message:str="") -> None:
        flag = False
        while True:
            if message == "":
                message_send = input("> ")
            else:
                message_send=message
                flag = True
            #文字列送信方式
            self.__socket.send(message_send.encode('utf-8'))
            #バイナリ送信方式
            #self.__socket.send(message_send)
            message_recv = self.__socket.recv(self.__buffer).decode('utf-8')
            self.received(message_recv)
            return
            #if flag:
            #    break
    
    def close(self):    
        try:
            self.__socket.shutdown(socket.SHUT_RDWR)
            self.__socket.close()
        except:
            pass

    def received(self, message:str):
        print(message)

class InetClient(BaseClient):
    def __init__(self, host:str="127.0.0.1", port:int=8080) -> None:
        self.server=(host,port)
        super().__init__(timeout=60, buffer=1024)
        super().connect(self.server, socket.AF_INET, socket.SOCK_STREAM, 0)


def play_msg(msg):
    cli = InetClient(host="pizero2")
    cli.send(msg)
    cli.close()


def play():
    cli = InetClient(host="pizero2")
    cli.send('c001') #プログラムチェンジ 
    cli.send('903e7f') #Note ON
    time.sleep(0.5)
    cli.send('90407f') #Note ON
    time.sleep(2)
    cli.send('803e7f') #Note OFF
    cli.send('80407f') #Note OFF
    cli.close()


if __name__=="__main__":
    #cli = InetClient(host="pizero2")
    #play()
    th = threading.Thread(target = play)
    #print(th)
    th.start()
    print('playend')
    #cli.close()
