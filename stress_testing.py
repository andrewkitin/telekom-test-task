import socket
import threading
import multiprocessing

def send_record():
    #header = b'0002 C1 01:13:02.877 00\r'
    #header = b'0002 C1 01:13:02.877 00\r'*30
    header = b'\rasdgfasbdasbsd\r0002 C1 01:13:02.877 00\rasgasfgasglkasdjb\r0002 C1 01:13:02.877 00\rkjaklgjaslgndasklvnolabvnjarb\r0002 C1 01:13:02.877 00\r'
    #header = b'0002 C1 01:13:02.877 00\r'
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect(('localhost', 9998))
    for i in range(1000):
        sock.send(header)

if __name__ == "__main__":
    number_of_threads = 10
    for i in range(number_of_threads):
        thread = threading.Thread(target=send_record)
        thread.start()
