import time
from os import path
import ssl
from socket import socket, AF_INET, SOCK_DGRAM
from logging import basicConfig, DEBUG
basicConfig(level=DEBUG)  # set now for dtls import code
from dtls import do_patch
do_patch()

cert_path = path.join(path.abspath(path.dirname(__file__)), "certs")
s = ssl.wrap_socket(socket(AF_INET, SOCK_DGRAM), cert_reqs=ssl.CERT_NONE, ca_certs=path.join(cert_path, "ca-cert.pem"))
s.connect(('127.0.0.1', 4444))

time.sleep(2)

s.send('Hi there long message\n'.encode())
time.sleep(1)
s.send('Hi 1\n'.encode())
s.send('Hi 2\n'.encode())
s.send('Hi 3\n'.encode())
print(s.recv().decode())
#s.send('aaabbb'.encode())
#print(s.recv().decode())
s = s.unwrap()
s.close()

pass

