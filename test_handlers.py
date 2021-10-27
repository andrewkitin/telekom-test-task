import pytest
from handlers import MessageHandler
import stream_worker as sw

@pytest.fixture()
def handler_setup():

    result = []
    class GoodMessageHandlerTest(MessageHandler):
        def update(self):
            result.append(True)
    
    class BadMessageHandlerTest(MessageHandler):
        def update(self):
            result.append(False)

    return sw.StreamWorker(GoodMessageHandlerTest, BadMessageHandlerTest), result

def test_time_checking(handler_setup):
    worker, result = handler_setup
    input_bad = b'0002 C1 24:13:02.877 00\r0002 C1 01:23:69.877 00\r0002 C1 01:13:02,877 00\r0002 C1 23:60:33.877 00\r'
    worker.update(input_bad)
    assert [False, False, False, False] == result
    result.clear()
    input_good = b'0002 C1 00:00:00.000 00\r0002 C1 23:59:59.999 00\r0002 C1 22:00:50.000 00\r'
    worker.update(input_good)
    assert [True, True, True] == result


def test_stream_stable(handler_setup):
    worker, result = handler_setup
    input = b'\r0002 C1 24:13:02.877 00 0002 C1 24:13:02.877 00\r\r0002 C1 13:13:02.800 00\r\r\r0002 C1 13:13:02.801 00\r\r0002\n C1\n 13:13:02\n.80\n2 00\n\r'*3
    worker.update(input)
    right = [True, True, True]*3
    right.extend([False]*3)
    assert right == result

def test_long_packet(handler_setup):
    worker, result = handler_setup
    input = b's'*65
    worker.update(input)
    input = b's'*200 + b'\r0002 C1 13:13:02.877 00\r'
    worker.update(input)
    assert [False, True, False] == result