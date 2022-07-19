'''Library for interacting with 2048 server'''
import socket
from time import sleep
from typing import Callable
from collections import deque
from threading import Thread, Event

SERVER_IP = "112.137.129.136"
SERVER_PORT = 1234
REFRESH_RATE = 0.05
DEFAULT_TIMEOUT = 10.0
DEFAULT_SLEEP = 0.1
SOCKET_BUFFER_SIZE = 1024


class MoveClass: # pylint: disable=too-few-public-methods
    '''Represent moves that can be made (left, up, right, down)'''
    L, U, R, D = "left", "up", "right", "down"
    ALL_MOVES = [L, U, R, D]

    def __getitem__(self, idx: int) -> str:
        '''Return moves based on index given (left, up, right, down).'''
        return self.ALL_MOVES[idx]
    
    def __iter__(self):
        for i in self.ALL_MOVES: yield i


MOVES = MoveClass()


class Board: # pylint: disable=too-few-public-methods
    '''Represents a state of the game board'''

    def __init__(self, data: str) -> None:
        '''Add the first row to the board'''
        self.board = []
        self.add_row(data)

    def add_row(self, data: str) -> None:
        '''Append rows to the board'''
        row = map(int, data.split())
        self.board.append(list(row))

    def full(self) -> bool:
        '''Returns whether the board is fully filled'''
        return len(self.board[0]) == len(self.board)


class Game: # pylint: disable=too-few-public-methods
    '''Represents the returned results about a game.
    Upon receiving this object, the current game should be considered ended.'''

    def __init__(self, data: str) -> None:
        '''Assigns the number of moves to the class'''
        self.move = data.split()[3]
        self.move = int(self.move)


class Result: # pylint: disable=too-few-public-methods
    '''Represents the returned results of the interaction.
    Upon receiving this object, the interaction should be considered closed.'''

    def __init__(self, data: str) -> None:
        '''Assigns the returned points to the class'''
        self.point = data.split()[1][0: -1]
        self.point = int(self.point)


class RepeatRun(Thread):
    '''Class to repeatedly run a function'''

    def run(self) -> None:
        '''Runs the loop'''
        while not self.__stopped.wait(REFRESH_RATE):
            self.__function()

    def __init__(self, function: Callable, stopped: Event) -> None:
        '''Specifies the function and stop trigger'''
        super().__init__()
        self.__function = function
        self.__stopped = stopped


class ClientBuffer(deque):
    '''The Buffer of a Client.
    Updates every few moments and push all data to a FIFO queue'''

    def __init__(self, sock: socket.socket) -> None:
        '''Initializes the loop and runs it'''
        super().__init__()
        self.__sock = sock
        self.__stopped = Event()
        self.__loop = RepeatRun(self.__get_buffer, self.__stopped)
        self.__loop.daemon = True
        self.api_exception = None

    def __append_line(self, line: str) -> None:
        '''Appends a line from buffer to the FIFO queue'''
        if "Invalid" in line:
            self.__stopped.set()
            self.api_exception = ValueError(
                f"You're dumb. The server responded with {line}")
        elif "ID" in line or "Identified" in line:
            return
        elif "Timed" in line:
            self.__stopped.set()
            self.api_exception = TimeoutError(
                f"You're too slow. The server responded with {line}")
        elif "Game" in line:
            self.append(Game(line))
        elif "Score" in line:
            self.append(Result(line))
            self.__stopped.set()
        else:
            if len(self) and isinstance(self[-1], Board) and not self[-1].full():
                self[-1].add_row(line)
            else:
                self.append(Board(line))

    def __get_buffer(self) -> None:
        '''Get the current buffer and flushes it to the FIFO queue.
        This function should be called every few moments.'''
        new_data = self.__sock.recv(SOCKET_BUFFER_SIZE).decode()
        if new_data == "":
            return
        for line in new_data.splitlines():
            self.__append_line(line)

    def start_looping(self) -> None:
        '''Starts the internal loop'''
        self.__loop.start()


class Client:
    '''A client, representing a server session'''

    def __raw_send(self, data: str) -> None:
        '''Send a message to the server. This should not be used externally'''
        self.__sock.send(f"{data}\n".encode())

    def __login(self):
        self.__raw_send(self.account)
        self.__raw_send(self.quiz)

    def __init__(self, account_name: str, quiz_name: str,
                 connect_ip: str = SERVER_IP, port: str = SERVER_PORT,
                 warn: bool = True) -> None:
        '''Initializes the session with the specified account name and quiz name.
        Be sure that you don't make the server sends more than 1024 characters per 50ms.
        If for some reason you do, edit the SOCKET_BUFFER_SIZE constant.
        The warn argument specifies whether to print a warning if the queue has >= 2 boards'''
        self.__sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.__sock.connect((connect_ip, port))
        self.playing = True

        self.account, self.quiz = account_name, quiz_name
        self.__login()

        self.__buffer = ClientBuffer(self.__sock)
        self.__buffer.start_looping()
        self.warn = warn

    def get_state(self) -> Board | Game | Result:
        '''Get the first state from the FIFO queue.'''
        steps = int(DEFAULT_TIMEOUT/DEFAULT_SLEEP)
        for _ in range(steps):
            if self.__buffer.api_exception is not None:
                raise self.__buffer.api_exception
            if not self.playing:
                raise IndexError("The game has finished")

            if len(self.__buffer):
                break
            sleep(DEFAULT_SLEEP)
        else:
            raise TimeoutError(
                f"Unable to retrieve any data after \
waiting for {steps*DEFAULT_SLEEP}s. Have you made any move?")
        if self.warn and len(self.__buffer) >= 2:
            if isinstance(self.__buffer[0], Board) and isinstance(self.__buffer[1], Board):
                raise RuntimeWarning('''You're making moves blindedly.
Make sure you don't try to make a move based on the ending board of a game.
To supress this, set the warn argument to False''')
        if isinstance(self.__buffer[0], Result):
            self.playing = False
        return self.__buffer.popleft()

    def make_move(self, data: str) -> None:
        '''Perform a move.'''
        self.__raw_send(data)
