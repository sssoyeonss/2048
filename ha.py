import socket
from random import randint
from time import sleep

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect(("112.137.129.136", 1234))

def read():
    msg = s.recv(1024).decode()
    print(msg)
    return msg

msg = read()
s.send("B05".encode())

msg = read()
s.send("1".encode())

msg = read()

while msg:
    r = int(input())
    if r == 0: s.send("up".encode())
    if r == 1: s.send("down".encode())
    if r == 2: s.send("left".encode())
    if r == 3: s.send("right".encode())
    msg = read()
    
