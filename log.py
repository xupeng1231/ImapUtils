import os
import time
import traceback

class Log:
    def __init__(self, file_name="log.txt"):
        self.__fd = open(file_name, "at")
        self.__fd.write("*"*20+time.strftime("%y-%m-%d %H:%M:%S")+"*"*20+"\n")

    def log(self,text):
        try:
            self.__fd.write("{}: {}\n".format(time.strftime("%y-%m-%d %H:%M:%S"), text))
        except:
            traceback.print_exc()

    @property
    def fd(self):
        self.__fd.write("{}: \n".format(time.strftime("%y-%m-%d %H:%M:%S")))
        return self.__fd

    def __del__(self):
        self.__fd.close()