import numpy as np
from engine.config import Config
from bot.mcts import MCTS
from engine.config import Config
from engine.utils import *

def train():
    config = Config()
    while True:
        print("NEW GAME")
        winner = None
        mcts = MCTS(config)
        train_configs = []
        target_policys = []
        target_values = []
        while winner == None:
            mcts.search(config)
            policy, best_move = mcts.get_mcts_policy()
            prepare_training(config,policy,train_configs,target_policys,target_values)
            config.apply_move(best_move,True)
            show(config)
            winner, _ = config.winner()
        objgraph.show_most_common_types()
        target_values = np.array(target_values)*winner
        train_configs = np.array(train_configs)
        target_policys = np.array(target_policys)
        mcts.model.fit(train_configs,[target_values,target_policys],epochs=1,batch_size=4,shuffle=True)
        mcts.model.save("bot/chess_model.h5")
        config.reset()

def prepare_training(config,policy,train_configs,target_policys,target_values):
    train_configs.append(encode(config))
    target_policys.append(policy)
    target_values.append(int(config.player) - int(not(config.player)))

if __name__ == "__main__":
    train()
