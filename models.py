from abc import ABC, abstractmethod
from dataclasses import astuple, dataclass, fields

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
    player_num: bytes
    ch_id: bytes
    hh: bytes
    mm: bytes
    ss: bytes
    zhq: bytes
    group: bytes

@dataclass
class GoodPlayerMessage(PlayerMessage):
    
    def get_message_string(self):
        try:
            decoded = [field.decode('utf-8') for field in astuple(self)]
        except Exception as err:
            print('Try to decode good player record: ', err)
            print('Fields:player_num={}, ch_id={}, hh={}, mm={}, ss={}, zhq={}, group={} \n'.format(*astuple(self)))

        return 'Player, number {0} get in at channel {1} at {2}:{3}:{4}.{5[0]}\n'.format(*decoded)


@dataclass
class BadPlayerMessage(PlayerMessage):

    def get_message_string(self):
        return 'Non-valid record.\nFields:player_num={}, ch_id={}, hh={}, mm={}, ss={}, zhq={}, group={} \n'.format(*astuple(self))