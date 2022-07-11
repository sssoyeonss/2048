import game
import random
account = input("ACCOUNT: ")
quiz = input("QUIZ NAME (1, 2, 3): ")

client = game.Client(account, quiz)

while True:
    print(f"BOARD\n{client.get_board()}")
    # i = input("MOVE (L, R, U, D): ").upper()
    i = random.choice("LRUD")
    if i == "L":
        client.move(game.L)
    elif i == "R":
        client.move(game.R)
    elif i == "U":
        client.move(game.U)
    elif i == "D":
        client.move(game.D)
    else:
        print("Invalid move. Move again")
