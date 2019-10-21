import math
import random
import copy
from chess.engine.config import Config
from chess.engine.utils import *
from chess.bot.neural_network import *

# Represents Monte Carlo Tree Search Node, defined by a game configuration.
class Node:
    def __init__(self, config, edge = None, winner = None):
        self.config = config
        self.in_edge = edge
        self.edges = []
        self.winner = winner

    # Return the edge that maximises PUCT score.
    def get_best_edge(self,c):
        num = 0
        for edge in self.edges:
            num += edge.N
        num = c * math.sqrt(num)
        max_puct = - math.inf
        best_edge = None
        for edge in self.edges:
            u = num*edge.P/float(1+edge.N)
            puct = edge.Q + u
            if puct > max_puct:
                max_puct = puct
                best_edge = edge
        return best_edge

    # Add noise to the probabilites to improve exploration.
    def add_dirichlet_noise(self,alpha):
        n = len(self.edges)
        alphas = np.full(n,alpha)
        noise = np.random.dirichlet(alphas)
        for i in range(n):
            self.edges[i].P = self.edges[i].P*0.75 + noise[i]*0.25

# Represents Monte Carlo Tree Search Edge, defined by a game configuration and a movement.
class Edge:
    def __init__(self,in_node,move,proba):
        self.in_node = in_node
        self.config = in_node.config
        self.move = move
        self.out_node = None
        self.N = 0
        self.W = 0
        self.Q = 0
        self.P = proba

# Implements Monte Carlo Tree Search.
class MCTS:
    def __init__(self,config):
        self.model = build_model()
        self.c = 4 # exploring parameter
        self.root = self.create_root(config)
        self.temperature = 1

    def create_root(self, config):
        winner, moves = config.winner()
        root = Node(config,winner=winner)
        value, policy_network = self.model.predict(np.array([encode(config)]))
        for move in moves:
            root.edges.append(Edge(root,move,policy_network[0][move.number(revert=not(root.config.player))]))
        root.add_dirichlet_noise(0.3)
        return root

    # Run search for a given game configuration.
    def search(self,config):
        n = 1
        while n < 400:
            obj, terminal = self.select()
            if terminal:
                node = obj
                value = node.winner
            else:
                edge = obj
                node, value = self.expand_evaluate(edge)
            self.back_propagate(node,value)
            n += 1

    # Update the root then return the mcts policy and the best move.
    def get_mcts_policy(self):
        normalize_denom = 0
        n_max = -math.inf
        # compute the N max to avoid exp overflow
        for edge in self.root.edges:
            if edge.N > n_max:
                n_max = edge.N
        for edge in self.root.edges:
            normalize_denom += np.exp((edge.N-n_max)/self.temperature)
        policy = np.zeros(4032)
        maxi = - math.inf
        best = None
        for edge in self.root.edges:
            value = np.exp((edge.N-n_max)/self.temperature)
            if value > maxi:
                maxi = value
                best = edge
            policy[edge.move.number(revert=not(self.root.config.player))] = value/normalize_denom
        self.root = best.out_node
        self.root.add_dirichlet_noise(0.3)
        # Delete upper tree
        self.root.in_edge = None
        return policy, best.move

    # Return a terminal edge or a terminal node.
    def select(self):
        node = self.root
        edge = None
        while node != None:
            edge = node.get_best_edge(self.c)
            if edge == None: # ie node is terminal
                return node, True
            node = edge.out_node
        return edge, False

    # Create a new node and its outcomming edges
    def expand_evaluate(self,edge):
        config = copy.deepcopy(edge.config)
        config.apply_move(edge.move,True)
        winner, moves = config.winner()
        new = Node(edge = edge, config = config, winner = winner)
        edge.out_node = new
        if new.winner == None:
            value, policy_network = self.model.predict(np.array([encode(new.config)]))
            value = value[0][0]
            for move in moves:
                new.edges.append(Edge(new,move,policy_network[0][move.number(revert=not(new.config.player))]))
        else:
            value = new.winner
        return new, value

    # Back propagate the value of the expanded node among the visited edges.
    def back_propagate(self,node,value):
        while node.in_edge != None:
            edge = node.in_edge
            edge.N += 1
            if edge.config.player:
                edge.W += value
            else:
                edge.W -= value
            edge.Q = edge.W/float(edge.N)
            node = edge.in_node
