"""
A quick Monte Carlo Tree Search implementation.  
For more details on MCTS see See http://pubs.doc.ic.ac.uk/survey-mcts-methods/survey-mcts-methods.pdf

The State is just a game where you have NUM_TURNS and at turn i you can make
a choice from [-2,2,3,-3]*i and this add to an accumulated value.  
The goal is for the accumulated value to be as close to 0 as possible.

The game is not very interesting but it allows one to study MCTS which is.  
Some features of the example by design are that moves do not commute and early mistakes are more costly.  

In particular there are two models of best child that one can use 
"""
import random
import hashlib
import math
from common.util.log import logger
class State:
    NUM_TURNS = 10
    GOAL = 0
    MOVES = [2, -2, 3, -3]
    MAX_VALUE = (5.0 * (NUM_TURNS - 1) * NUM_TURNS) / 2
    num_moves = len(MOVES)

    def __init__(self, value=0, moves=None, turn=NUM_TURNS):
        if moves is None:
            moves = []
        self.value = value
        self.turn = turn
        self.moves = moves

    def next_state(self):
        next_move = random.choice([x * self.turn for x in self.MOVES])
        next = State(self.value + next_move, self.moves + [next_move], self.turn - 1)
        return next

    def terminal(self):
        if self.turn == 0:
            return True
        return False

    def reward(self):
        r = 1.0 - (abs(self.value - self.GOAL) / self.MAX_VALUE)
        return r

    def __hash__(self):
        return int(hashlib.md5(str(self.moves).encode('utf-8')).hexdigest(), 16)

    def __eq__(self, other):
        if hash(self) == hash(other):
            return True
        return False

    def __repr__(self):
        s = "Value: %d; Moves: %s" % (self.value, self.moves)
        return s
class Node:
    def __init__(self, state, parent=None):
        self.visits = 1
        self.reward = 0.0
        self.state = state
        self.children = []
        self.parent = parent

    def add_child(self, child_state):
        child = Node(child_state, self)
        self.children.append(child)

    def update(self, reward):
        self.reward += reward
        self.visits += 1

    def fully_expanded(self):
        if len(self.children) == self.state.num_moves:
            return True
        return False

    def __repr__(self):
        s = "Node; children: %d; visits: %d; reward: %f" % (len(self.children), self.visits, self.reward)
        return s
def expand(node):
    tried_children = [c.state for c in node.children]
    new_state = node.state.next_state()
    while new_state in tried_children:
        new_state = node.state.next_state()
    node.add_child(new_state)
    return node.children[-1]
def best_child(node, scalar):
    best_score = 0.0
    best_children = []
    for c in node.children:
        exploit = c.reward / c.visits
        explore = math.sqrt(2.0 * math.log(node.visits) / float(c.visits))
        score = exploit + scalar * explore
        if score == best_score:
            best_children.append(c)
        if score > best_score:
            best_children = [c]
            best_score = score
    if len(best_children) == 0:
        logger.warning("OOPS: no best child found, probably fatal")
    return random.choice(best_children)
def tree_policy(node):
    while not node.state.terminal():
        if len(node.children) == 0:
            return expand(node)
        elif random.uniform(0, 1) < .5:
            node = best_child(node, SCALAR)
        else:
            if not node.fully_expanded():
                return expand(node)
            else:
                node = best_child(node, SCALAR)
    return node
def uct_search(budget, root):
    for iter in range(int(budget)):
        if iter % 10000 == 9999:
            logger.info("simulation: %d" % iter)
            logger.info(root)
        front = tree_policy(root)
        reward = default_policy(front.state)
        backup(front, reward)
    return best_child(root, 0)
def default_policy(state):
    while not state.terminal():
        state = state.next_state()
    return state.reward()

def backup(node, reward):
    while node is not None:
        node.visits += 1
        node.reward += reward
        node = node.parent
    return

if __name__ == "__main__":
    levels = 1
    num_sims = 500
    current_node = Node(State())
    for l in range(levels):
        current_node = uct_search(num_sims / (l + 1), current_node)
        print("level %d" % l)
        print("Num Children: %d" % len(current_node.children))
        for i, c in enumerate(current_node.children):
            print(i, c)
        print("Best Child: %s" % current_node.state, np.sum(current_node.state.moves))

        print("--------------------------------")
    root = current_node
    while root.parent is not None:
        root = root.parent
    print(root)
    print(current_node)
