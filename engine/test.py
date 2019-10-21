from chess.engine.config import Config
from chess.engine.utils import *
import csv

# Play around 6k check mate games to test chess engine.
# Draws have been tested locally because of resignation within draw games.
def test():
    config = Config()
    with open('chess/engine/games.csv', newline='') as games:
        reader = csv.DictReader(games)
        nb = 0
        for row in reader:
            nb += 1
            moves = row['moves'].split()
            i = 0
            over = None
            if row['victory_status'] == 'mate' and nb > 0:
                while over == None:
                    start, dest, prom_not_queen = ask_test(moves[i])
                    # auto promotion in queen so others are not handled
                    if prom_not_queen:
                        over = 0
                    elif config.try_play(start,dest):
                        # show(config)
                        over,_ = config.winner()
                    else:
                        sys.exit("fail at move :  " + moves[i])
                    i += 1
                config.reset()
test()
