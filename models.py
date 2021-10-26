from abc import ABC, abstractmethod
from dataclasses import dataclass

class Message(ABC):

    @abstractmethod
    def get_message_string(self):
        pass

@dataclass
class UnknownMessage(Message):
    message: str

    def get_message_string(self):
        return 'Unknown message: {}\n'.format(self.message)

@dataclass
class PlayerMessage(Message):
    player_num: str
    ch_id: str
    hh: str
    mm: str
    ss: str
    zhq: str
    group: str

@dataclass
class GoodPlayerMessage(PlayerMessage):
    
    def get_message_string(self):
        return 'Player, number {} get in at channel {} at {}:{}:{}.{}\n'.format(self.player_num, self.ch_id, self.hh, self.mm, self.ss, self.zhq[0])


@dataclass
class BadPlayerMessage(PlayerMessage):

    def get_message_string(self):
        return 'Non-valid record.\nFields:player_num={}, ch_id={}, hh={}, mm={}, ss={}, zhq={}, group={} \n'.format(self.player_num, self.ch_id, self.hh, self.mm, self.ss, self.zhq, self.group)