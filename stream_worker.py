from enum import Enum
import re

from config import MAX_PACKET_LENGTH
from models import GoodPlayerMessage, UnknownMessage, BadPlayerMessage
from handlers import MessageHandler

from timeit import default_timer as timer
# 0002 C1 01:13:02.877 00[CR]
class StreamWorker:

    def __init__(self, success_handler: MessageHandler, bad_handlers: MessageHandler) -> None:
        self.__template = rb'\r(\d{4}) (\w{2}) (\d{2}):(\d{2}):(\d{2})[.](\d{3}) (\d{2})\r'
        self.success_handler = success_handler
        self.bad_handler = bad_handlers
        self.__buf: bytes = b'\r' # [CR]

    def __validate(self, msg: tuple):
        player_num, ch_id, hh, mm, ss, zhq, group = msg
        hh = hh.decode('utf-8')
        mm = mm.decode('utf-8')
        ss = ss.decode('utf-8')
        
        if (hh[0] == '2' and hh[1] > '3'):
            return False
        if mm[0] > '5': 
            return False
        if ss[0] > '5': 
            return False
        return True

    def find_matches(self):
        match = re.search(self.__template, self.__buf)
        while match:
            self.__buf = self.__buf[:match.start()+1] + self.__buf[match.end():]
            yield match
            match = re.search(self.__template, self.__buf)

    def __refresh_buffer(self):
        self.__buf = b'\r'

    def __update(self):

        for match in self.find_matches():
            msg = match.groups()
            if self.__validate(msg):
                self.success_handler.update(GoodPlayerMessage(*msg))
            else:
                self.bad_handler.update(BadPlayerMessage(*msg))
        
        
        idx = self.__buf.rfind(b'\r')
        if idx == -1:
            self.__refresh_buffer()
        
        splitted = self.__buf[:idx].split(b'\r')
        for split in splitted:
            if len(split):
                self.bad_handler.update(UnknownMessage(repr(split)))

        if len(self.__buf[idx:]) > MAX_PACKET_LENGTH:
            self.bad_handler.update(UnknownMessage(repr(self.__buf[idx:])))
            self.__refresh_buffer()
        self.__buf = self.__buf[idx:]
        
    def update(self, b_array: bytes):
        self.__buf += b_array.replace(b'\n',b'')
        self.__update()
    


