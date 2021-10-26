from abc import ABC, abstractmethod
from models import PlayerMessage, Message, BadPlayerMessage

class MessageHandler(ABC):

    @abstractmethod
    def update(self, msg:Message):
        pass

class GoodMessageHandler(MessageHandler):
    def __init__(self, log_filename) -> None:
        super().__init__()
        self.__log_filename = log_filename

    def __log_message(self, msg: PlayerMessage):
        with open(self.__log_filename, 'a') as f:
            f.write(msg.get_message_string())

    def update(self, msg: PlayerMessage):
        self.__log_message(msg)
        if msg.group == '00':
            print(msg.get_message_string())
        
class BadMessageHandler(MessageHandler):
    def __init__(self, log_filename) -> None:
        super().__init__()
        self.__log_filename = log_filename
    
    def update(self, msg: Message):
        with open(self.__log_filename, 'a') as f:
            f.write(msg.get_message_string())
