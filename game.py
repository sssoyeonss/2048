'''Library for interacting with 2048 server'''
import socket
from collections import deque
from time import sleep
from typing import Callable
from threading import Thread, Event

SERVER_IP = "112.137.129.136"
SERVER_PORT = 1234
REFRESH_RATE = 0.05
L, R, U, D = "left", "right", "up", "down"


class Board:
    def __init__(self, data: str) -> None:
        self.board = []
        self.add_row(data)

    def add_row(self, data: str) -> None:
        row = map(int, data.split())
        self.board.append(list(row))


class Game:
    def __init__(self, data: str) -> None:
        self.move = data.split()[3]
        self.move = int(self.move)


class Result:
    def __init__(self, data: str) -> None:
        self.point = data.split()[1][0: -1]
        self.point = int(self.point)


class RepeatRun(Thread):
    def run(self):
        while not self.__stopped.wait(REFRESH_RATE):
            self.__function()

    def __init__(self, function: Callable, stopped: Event) -> None:
        super().__init__()
        self.__function = function
        self.__stopped = stopped


class ClientBuffer(deque):
    def __init__(self, sock: socket.socket) -> None:
        super().__init__()
        self.__sock = sock
        self.__stopped = Event()
        self.__loop = RepeatRun(self.__get_buffer, self.__stopped)

    def __append_line(self, line: str) -> None:
        if "ID" in line or "Identified" in line:
            return
        elif "Invalid" in line:
            raise ValueError(f"You're dumb. The server responded with {line}")
        elif "Timed" in line:
            raise TimeoutError(f"You're too slow. The server responded with {line}")
        elif "Game" in line:
            self.append(Game(line))
        elif "Score" in line:
            self.append(Result(line))
            self.__stopped.set()
        else:
            if self.__len__() and isinstance(self.__getitem__(-1), Board):
                self.__getitem__(-1).add_row(line)
            else:
                self.append(Board(line))

    def __get_buffer(self):
        new_data = self.__sock.recv(1024).decode()
        if new_data == "": return
        for line in new_data.splitlines():
            self.__append_line(line)

    def start_looping(self):
        self.__loop.start()


class Client:
    '''A client, representing a server session'''

    def __raw_send(self, data: str) -> None:
        '''Send a message to the server. This should not be used externally'''
        self.__sock.send(data.encode())

    def __login(self):
        self.__raw_send(self.account)
        self.__raw_send(self.quiz)

    def __init__(self, account_name: str, quiz_name: str,
                 ip: str = SERVER_IP, port: str = SERVER_PORT) -> None:
        '''Initializes the session with the specified account name and quiz name'''
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((SERVER_IP, SERVER_PORT))
        self.playing = True

        self.account, self.quiz = account_name, quiz_name
        self.__login()

        self.__buffer = ClientBuffer(self.__sock)
        self.__buffer.start_looping()

    def get_state(self) -> Board | Game | Result:
        if not self.playing:
            raise IndexError("The game has finished")
        while len(self.__buffer) == 0:
            print("Waiting")
            sleep(0.5)
        if isinstance(self.__buffer[0], Result):
            self.playing = False
        return self.__buffer.popleft()

    def make_move(self, move: str) -> None:
        self.__raw_send(move)
