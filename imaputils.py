from Command import *
from Packet import *
import random
import socket
from log import *
imap_server = ("192.168.1.82", 143)

class ImapConnection:
    def __init__(self, server):
        self.server = server
        self.session_uid = str(random.getrandbits(32))
        self.socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.packet_repo = PacketStorage(stream_uid=self.session_uid,block_size=1024)
        self.log = Log("log.txt")
        self.__stop = False
    def start(self):
        self.socket.connect(self.server)
        self.socket.settimeout(1)
        self.recv()
        self.send(LoginCmd("user0@tca.local","1qaz2wsx"))
        while not self.__stop:
            try:
                self.recv()
            except socket.timeout:
                pass
            except:
                traceback.print_exc(file=self.log.fd)

            try:
                self.send(self.construct_cmd())
            except socket.timeout:
                pass
            except:
                traceback.print_exc(file=self.log.fd)


    def construct_cmd(self):
        cmd=LogoutCmd()
        while isinstance(cmd,LogoutCmd):
            cmd=random.choice(ImapCommandSet.cmds)()
        return cmd

    def send(self,cmd):
        packet = Packet(source=Packet.FROM_CLIENT,data_cmd=cmd)
        packet.send(self.socket)
        packet.save(self.packet_repo)
        print packet.data

    def recv(self):
        msg = self.socket.recv(65535)
        packet = Packet(source=Packet.FROM_SERVER, data_cmd=msg)
        packet.save(self.packet_repo)
        print packet.data

def test():
    conn=ImapConnection(imap_server)
    conn.start()

if __name__ == "__main__":
    test()