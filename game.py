'''Library for interacting with 2048 server'''
import socket
from datetime import datetime
from typing import Tuple
import asyncio
import threading

SERVER_IP = "112.137.129.136"
SERVER_PORT = 1234
TOLERANCE = 0.100
L, R, U, D = "left", "right", "up", "down"

class Client:
    '''A client, representing a server session'''
    def __get_buffer(self):
        new_data = s

    def __init__(self, account_name: str, quiz_name: str,
                 ip: str = SERVER_IP, port: str = SERVER_PORT) -> None:
        '''Initializes the session with the specified account name and quiz name'''
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((SERVER_IP, SERVER_PORT))
        
        self.__raw_read()
        self.__raw_send(account_name)
        self.__raw_read()
        self.__raw_send(quiz_name)
        self.__raw_read()

    def __raw_read(self) -> None:
        '''Read the sent board from server'''
        self.__board = self.__sock.recv(1024).decode()


    def __raw_send(self, data: str) -> None:
        '''Send a message to the server. This should not be used externally'''
        self.__sock.send(data.encode())

    def move(self, move: str) -> str:
        '''Make a move. Returns the new board'''
        self.__raw_send(move)
        self.__raw_read()
        return self.__board
    
    def move_with_latency(self, move: str) -> Tuple[str, float]:
        '''Make move, and measure the latency'''
        start_time = datetime.now()
        self.move(move)
        end_time = datetime.now()
        return self.get_board(), (end_time - start_time).total_seconds()*1000

    def get_board(self) -> str:
        '''Returns the current board, in case you missed it.
        The first board should also be retrieved with this function'''
        return self.__board
