import asyncio
import config
import stream_worker as sw
from handlers import GoodMessageHandler, BadMessageHandler, MessageHandler


class RequestHandler:

    def __init__(self, data_handler_class: sw.StreamWorker, good_msg_handler_cls: MessageHandler, bad_msg_handle_cls: MessageHandler) -> None:
        self.data_handler_class = data_handler_class
        self.good_msg_handler_class = good_msg_handler_cls
        self.bad_msg_handler_class = bad_msg_handle_cls

        self.stream_writers = {}
        self.writers = {}
        self.readers = {}
        self.tasks = {}

    async def handle_loop(self):
        while True:
            for addr, reader in self.readers.items():
                if addr not in self.tasks.keys():
                    self.tasks[addr] = asyncio.create_task(reader.read(config.RECV_SIZE))
                else:
                    if self.tasks[addr].done() or self.tasks[addr].cancelled():
                        data = self.tasks[addr].result()
                        if len(data):
                            self.stream_writers[addr].update(data)
                        self.tasks[addr] = asyncio.create_task(reader.read(config.RECV_SIZE))
                    else:
                        # task on processing
                        pass
            await asyncio.sleep(0)

    async def handle_conn(self, reader, writer):
        addr = writer.get_extra_info('peername')
        if addr in self.tasks.keys():
            self.tasks[addr].cancel()
        self.writers[addr] = writer
        self.readers[addr] = reader
        self.stream_writers[addr] = self.data_handler_class(self.good_msg_handler_class('{}_good.log'.format(addr)), self.bad_msg_handler_class('{}_bad.log'.format(addr)))

async def main(request_handler: RequestHandler):
    server = await asyncio.start_server(
        request_handler.handle_conn, config.APP_HOST, config.APP_PORT)
    addrs = ', '.join(str(sock.getsockname()) for sock in server.sockets)
    print(f'Serving on {addrs}')
    async with server:
        await server.serve_forever()

if __name__ == "__main__":
    rh = RequestHandler(sw.StreamWorker, GoodMessageHandler, BadMessageHandler)
    loop = asyncio.get_event_loop()
    loop.create_task(main(rh))
    loop.create_task(rh.handle_loop())
    loop.run_forever()