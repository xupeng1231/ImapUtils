import os
import socket
import time
from Packet import *
cmd_tag=0


class Command:
    cmd=""
    def __init__(self, *args):
        self.args = args
    @property
    def cmd_str(self):
        return "c{} {} {}\r\n".format(str(cmd_tag),self.cmd, " ".join(self.args)).strip(" ")

class CapabilityCmd(Command):
    cmd="capability"

class NoopCmd(Command):
    cmd="noop"

class LogoutCmd(Command):
    cmd="logout"

class StarttlsCmd(Command):
    cmd="starttls"

class LoginCmd(Command):
    cmd="login"

class SelectCmd(Command):
    cmd="select"

class ExamineCmd(Command):
    cmd="examine"

class CreateCmd(Command):
    cmd="create"

class DeleteCmd(Command):
    cmd="delete"

class RenameCmd(Command):
    cmd="rename"

class SubscribeCmd(Command):
    cmd="subscribe"

class UnsubscribeCmd(Command):
    cmd="unsubscribe"

class ListCmd(Command):
    cmd="list"

class LsubCmd(Command):
    cmd="lsub"

class StatusCmd(Command):
    cmd="status"

class AppendCmd(Command):
    cmd="append"

class CheckCmd(Command):
    cmd="check"

class CloseCmd(Command):
    cmd="close"

class ExpungeCmd(Command):
    cmd="expunge"

class SearchCmd(Command):
    cmd="search"

class FetchCmd(Command):
    cmd="fetch"

class StoreCmd(Command):
    cmd="store"

class CopyCmd(Command):
    cmd="copy"

class UidCommand(Command):
    cmd="uid"


class ImapCommandSet:
    cmds=[CapabilityCmd, NoopCmd, LogoutCmd, StarttlsCmd, LoginCmd, SelectCmd, ExamineCmd, CreateCmd, DeleteCmd, RenameCmd,
          SubscribeCmd, UnsubscribeCmd, ListCmd, LsubCmd, StatusCmd, AppendCmd, CheckCmd, CloseCmd, ExpungeCmd, SearchCmd,
          FetchCmd, StoreCmd, CopyCmd, UidCommand]
# s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
# s.connect(("192.168.1.82",143))
# s.settimeout(3)
# while True:
#     res=s.recv(65536)
#     print ": "+res


