from enum import Enum
import re
from models import GoodPlayerMessage, PlayerMessage, UnknownMessage, BadPlayerMessage
from handlers import GoodMessageHandler, BadMessageHandler
# 0002 C1 01:13:02.877 00[CR]
class StreamWorker:

    def __init__(self, success_handler: GoodMessageHandler, bad_handlers: BadMessageHandler) -> None:
        self.__template = rb'\r(\d{4}) (\w{2}) (\d{2}):(\d{2}):(\d{2}).(\d{3}) (\d{2})\r'
        self.success_handler = success_handler
        self.bad_handler = bad_handlers
        self.__buf = b'\r' # [CR]

    def __validate(self, msg: tuple):
        player_num, ch_id, hh, mm, ss, zhq, group = msg
        hh = hh.decode('utf-8')
        mm = mm.decode('utf-8')
        ss = ss.decode('utf-8')
        
        if hh[0] > '2' > hh[1] > '4':
            return False
        if mm[0] > '6': 
            return False
        if ss[0] > '6': 
            return False
        return True

    def __update(self):
        match = re.search(self.__template, self.__buf)
        while match:
            msg = match.groups()
            if self.__validate(msg):
                self.success_handler.update(GoodPlayerMessage(*msg))
            else:
                self.bad_handler.update(BadPlayerMessage(*msg))

            self.__buf = self.__buf[:match.start() + 1] + self.__buf[match.end():]
            match = re.search(self.__template, self.__buf)

        idx = self.__buf.rfind(b'\r')
        if len(self.__buf[:idx]):
            self.bad_handler.update(UnknownMessage(repr(self.__buf[:idx])))
        self.__buf = self.__buf[idx:]

    def update(self, b_array: bytes):
        self.__buf += b_array[:-1]
        self.__update()
    


