from engine.config import Config
from engine.utils import *

def play():
    config = Config()
    winner = None
    while winner == None:
        show(config)
        start, dest = ask()
        if config.try_play(start,dest):
            winner,_ = config.winner()
        else:
            print("Invalid move, please replay")
    show(config)
    show_winner(winner)

if __name__ == "__main__":
    play()
