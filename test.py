'''Test code'''
import random
import game
account = input("ACCOUNT: ")
quiz = input("QUIZ NAME (1, 2, 3): ")

client = game.Client(account, quiz)
# Code chi choi 1 game.
# De choi duoc nhieu game, can phai kiem tra xem
# bang hien tai co phai ket thuc khong
while client.playing:
    data = client.get_state()
    if isinstance(data, game.Board):
        # Lay mot move bat ky
        move = game.MOVES[random.randint(0, 3)]
        # Make move
        print(f"{data.board}\n{move}")
        client.make_move(move)
    elif isinstance(data, game.Game):
        # Mot game da ket thuc
        print("Game ended")
    elif isinstance(data, game.Result):
        # Tro choi da ket thuc
        print("Session ended")
        break
