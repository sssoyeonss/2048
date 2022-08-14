'''Test code'''
import random
import game
from minimax_ import Maximize
from Grid_ import Grid
from expectimax_ import Maximize_
account = input("ACCOUNT: ")
quiz = input("QUIZ NAME (1, 2, 3): ")

client = game.Client(account, quiz)
# Code chi choi 1 game.
# De choi duoc nhieu game, can phai kiem tra xem
# bang hien tai co phai ket thuc khong
dir = ["left", "up", "right", "down"]
cnt = 0

while client.playing:
    data = client.get_state()
    if isinstance(data, game.Board):
        move = Maximize_(Grid(data.board), 4)[0]
        '''
        move = 3
        if Grid(data.board).moveLeft() == bestChild:
            move = 0
        elif Grid(data.board).moveUp() == bestChild:
            move = 1
        elif Grid(data.board).moveRight() == bestChild:
            move = 2
        '''    
        cnt += 1
        print(f"Move {cnt}:")
        # Make move
        print(f"{data.board}\n{dir[move]}")
        client.make_move(dir[move])
    elif isinstance(data, game.Game):
        # Mot game da ket thuc
        print("Game ended")
    elif isinstance(data, game.Result):
        # Tro choi da ket thuc
        print("Session ended")
        break
