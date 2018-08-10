import time
import os
import Command
import cPickle as pickle
import threading

PACKETS_DIR="packets"
if not os.path.exists(PACKETS_DIR):
    os.makedirs(PACKETS_DIR)

# source
# time
# data
class Packet:
    FROM_CLIENT = 0
    FROM_SERVER = 1
    def __init__(self, source, data_cmd):
        self.source = source
        self.time = time.time()
        if isinstance(data_cmd,Command.Command):
            self.data = data_cmd.cmd_str
        else:
            self.data = data_cmd

    def send(self, s):
        s.sendall(self.data)
        self.time = time.time()
        Command.cmd_tag+=1

    def save(self, repo):
        repo.store(self)

class PacketBlock:
    def __init__(self,stream_uid):
        self.stream_uid=stream_uid
        self.packets=[]
        self.size=0

    def save(self):
        if self.size == 0:
            return True
        file_name="{}-{}-{}".format(str(self.stream_uid),str(self.start_time),str(self.end_time))
        file_path=os.path.join(PACKETS_DIR, file_name)
        with open(file_path,"wb") as f:
            pickle.dump(self, f)
        return file_name

    def append(self,packet):
        self.packets.append(packet)
        self.size+=len(packet.data)

    @property
    def start_time(self):
        if len(self.packets) == 0:
            return -1
        else:
            return self.packets[0].time

    @property
    def end_time(self):
        if len(self.packets) == 0:
            return -1
        else:
            return self.packets[-1].time


class PacketStorage:
    def __init__(self, stream_uid, block_size=20971520):  # 1024*1024*20
        self.stream_uid=stream_uid
        self.block_size=block_size
        self.block = PacketBlock(stream_uid)
    def store(self, packet):
        self.block.append(packet)
        if self.block.size >= self.block_size:
            t = threading.Thread(target=self.block.save)
            t.start()
            self.block = PacketBlock(stream_uid=self.stream_uid)

    def __del__(self):
        self.block.save()

