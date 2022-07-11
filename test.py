import game
import random
account = input("ACCOUNT: ")
quiz = input("QUIZ NAME (1, 2, 3): ")

client = game.Client(account, quiz)
with open("log.txt", "w") as log:
    while client.playing:
        data = client.get_state()
        if isinstance(data, game.Board):
            move = game.MOVES[random.randint(0, 3)]
            log.write(f"{data.board}\n{move}\n")
            print(f"{data.board}\n{move}")

        elif isinstance(data, game.Game):
            log.write(f"Game ended. Move: {data.move}\n")
            print("Game ended")

        elif isinstance(data, game.Result):
            log.write(F"Session ended. Points: {data.point}")
            print("Session ended")
            break
