"""
Hinger Project
Coursework 001 for: CMP-5058A Artificial Intelligence

Module: a2_agent.py

@author: B15 (100487471, 100464192, 100476374, 100464083)
@date:   05/11/2026
"""

import math
import random
import time
from a1_state import State


# -----------------------------------------------------------------------
# Task 2.6: Node used by Monte Carlo Tree Search
# -----------------------------------------------------------------------
class Node:

    def __init__(self, state, parent=None, letter=None, agent_turn=True, score=0):
        self.state = state              #State of the board 
        self.parent = parent            #This is the previous position in the tree, it passes the simulation results back up
        self.letter = letter            #This is the move that led to this node
        self.agent_turn = agent_turn    #If it is the agents turn then it will be true
        self.score = score              #the score is the agent score minus the opponent score so far 
        self.children = []              
        self.untried = state.legal_moves()  
        self.visits = 0                 #Looks at how many simulations passed through
        self.wins = 0.0                 #This stores the total result of the simulations

class Agent:

    # -------------------------------------------------------------------
    # Task 2.1: Initialiser - setting up the agent 
    # -------------------------------------------------------------------
    def __init__(self, name='B15'):
        self.name = name
        #The playing strategies this agent can use
        self.modes = ['minimax', 'alphabeta', 'mcts']
        self.search_depth = 3
        #Number of states examined in the last search
        self.nodes_count = 0
        #Number of simulations Monte Carlo runs for each move
        self.mtcs_runs = 300

    # -------------------------------------------------------------------
    # Task 2.2: String representation of the agent
    # -------------------------------------------------------------------
    def __str__(self):
        return f"Agent {self.name} (modes: {', '.join(self.modes)})"

    # -------------------------------------------------------------------
    # Task 2.3: next_move() - returns a legal move letter or None
    # -------------------------------------------------------------------
    def next_move(self, state, mode='alphabeta'):
        #Makes sure to only ask for one of the agent's strategies
        assert mode in self.modes

        #If there are no active cells then no move can be made 
        if state.is_game_over():
            return None

        if mode == 'minimax':
            return self.best_minimax_move(state)
        if mode == 'alphabeta':
            return self.best_alphabeta_move(state)
        return self.mcts_move(state)

    # -------------------------------------------------------------------
    # Task 2.4: Additional variables and Supporting methods
    # -------------------------------------------------------------------

    #This works out how many points a move is worth to the player making it
    def move_value(self, state, letter):
        row, col = state.letter_to_cell(letter)
        hinger_bonus = 0
            #player gets a 100 point bonus if the cell is a hinger minus the points of the move
        if state.is_hinger(row, col):
            hinger_bonus = 100
        return hinger_bonus - state.cost(letter)

    #Minimax score is agent's points - opponent's points
    #The agent tries to make it as big as possible and the opponent as small as possible
    def minimax(self, state, depth, max_turn, score):
        self.nodes_count += 1

        #Stops when the depth limit is reached or if there are no counters left
        if depth == 0 or state.is_game_over():
            return score

        if max_turn:
            #The agent starts with the lowest possible value
            best_score = -float('inf')
            for letter in state.legal_moves():
                point_gain = self.move_value(state, letter)
                #Copies the board so the move can be tried without changing the original
                new_state = state.state_clone()
                new_state.move(letter)
                #The agent's points are added then it's the opponent's turn
                value = self.minimax(new_state, depth - 1, False, score + point_gain)
                best_score = max(best_score, value)
            return best_score

        else:
            #The opponent starts with the highest possible value
            best_score = float('inf')
            for letter in state.legal_moves():
                point_gain = self.move_value(state, letter)
                new_state = state.state_clone()
                new_state.move(letter)
                #The opponent's points are taken away then it's the agent's turn
                value = self.minimax(new_state, depth - 1, True, score - point_gain)
                best_score = min(best_score, value)
            return best_score

    #Tries every move at the top of the tree and returns the best one
    def best_minimax_move(self, state):
        self.nodes_count = 0
        best_score = -float('inf')
        best_move = None

        for letter in state.legal_moves():
            point_gain = self.move_value(state, letter)
            new_state = state.state_clone()
            new_state.move(letter)
            value = self.minimax(new_state, self.search_depth - 1, False, point_gain)
            #This keeps the move with the highest value
            if value > best_score:
                best_score = value
                best_move = letter

        return best_move


    #alpha is the best value the agent is guaranteed so far
    #beta is the best value the opponent is guaranteed so far
    def alphabeta(self, state, depth, alpha, beta, max_turn, score):
        self.nodes_count += 1

        if depth == 0 or state.is_game_over():
            return score

        if max_turn:
            best_score = -float('inf')
            for letter in state.legal_moves():
                point_gain = self.move_value(state, letter)
                new_state = state.state_clone()
                new_state.move(letter)
                value = self.alphabeta(new_state, depth - 1, alpha, beta, False, score + point_gain)
                best_score = max(best_score, value)
                #Updates the best value the agent can guarantee
                alpha = max(alpha, best_score)
                if beta <= alpha:
                    break
            return best_score

        else:
            best_score = float('inf')
            for letter in state.legal_moves():
                point_gain = self.move_value(state, letter)
                new_state = state.state_clone()
                new_state.move(letter)
                value = self.alphabeta(new_state, depth - 1, alpha, beta, True, score - point_gain)
                best_score = min(best_score, value)
                #Updates the best value the opponent can guarantee
                beta = min(beta, best_score)
                if beta <= alpha:
                    break
            return best_score

    #Tries every move at the top of the tree and returns the best one using alpha-beta
    def best_alphabeta_move(self, state):
        self.nodes_count = 0
        best_score = -float('inf')
        best_move = None
        alpha = -float('inf')
        beta = float('inf')

        for letter in state.legal_moves():
            point_gain = self.move_value(state, letter)
            new_state = state.state_clone()
            new_state.move(letter)
            value = self.alphabeta(new_state, self.search_depth - 1, alpha, beta, False, point_gain)
            if value > best_score:
                best_score = value
                best_move = letter
            #The best value found so far becomes the new lower bound
            alpha = max(alpha, best_score)

        return best_move

    # -------------------------------------------------------------------
    # Task 2.6: Monte Carlo Tree Search
    # -------------------------------------------------------------------

    #Chooses which child to explore using the UCB1 formula
    def select_child(self, node):
        best_value = -float('inf')
        best_child = None
        for child in node.children:
            avg_child_result = child.wins / child.visits
            #When it's the opponent's turn the opponent picks what is worst for the agent
            if not node.agent_turn:
                #the average looks at how well this move has done so far and favours moves that have won
                avg_child_result = 1 - avg_child_result
            explore = math.sqrt(2) * math.sqrt(math.log(node.visits) / child.visits)
            if avg_child_result + explore > best_value:
                best_value = avg_child_result + explore
                best_child = child
        return best_child

    #Plays random moves until the board is empty and returns the result for the agent
    #1 = win
    #0.5 = draw 
    #0 = loss
    def random_move(self, node):
        state = node.state.state_clone()
        agent_turn = node.agent_turn
        score = node.score

        while not state.is_game_over():
            letter = random.choice(state.legal_moves())
            point_gain = self.move_value(state, letter)
            if agent_turn:
                score += point_gain
            else:
                score -= point_gain
            state.move(letter)
            agent_turn = not agent_turn

        if score > 0:
            return 1
        if score == 0:
            return 0.5
        return 0

    #Runs the four monte carlo steps multiple times and returns the most visited move
    def mcts_move(self, state):
        root_node = Node(state.state_clone())

        for _ in range(self.mtcs_runs):
            node = root_node

            #SELECTION: goes down the tree while every move has been tried
            while not node.untried and node.children:
                node = self.select_child(node)

            #EXPANSION: adds one untried move as a new child
            if node.untried:
                letter = random.choice(node.untried)
                node.untried.remove(letter)
                point_gain = self.move_value(node.state, letter)
                if node.agent_turn:
                    score = node.score + point_gain
                else:
                    score = node.score - point_gain
                new_state = node.state.state_clone()
                new_state.move(letter)
                child = Node(new_state, node, letter, not node.agent_turn, score)
                node.children.append(child)
                node = child

            #SIMULATION: plays the rest of the game randomly
            result = self.random_move(node)

            #BACKPROPGATION: updates every node on the path back to the root
            while node is not None:
                node.visits += 1
                node.wins += result
                node = node.parent

        #The move that was explored the most is the most reliable choice
        best_child = max(root_node.children, key=lambda child: child.visits)
        return best_child.letter


# -----------------------------------------------------------------------
# Task 2.5: tester() - These are all the tests 
# -----------------------------------------------------------------------
def tester():
    agent = Agent()
    print(agent)

    print("Name (expected B15):", agent.name)
    print("Has minimax and alphabeta (expected True):",
          'minimax' in agent.modes and 'alphabeta' in agent.modes)

    print(Agent('Bob'))

    sample_board = State([[1, 1, 0, 0, 1],
                [1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1],
                [0, 0, 0, 0, 1]])
    print("State s1:")
    print(sample_board)

    #Minimax and alpha-beta should choose the same move but alpha-beta should examine less states and take less time
    for mode in ['minimax', 'alphabeta']:
        start_time = time.perf_counter()
        move = agent.next_move(sample_board, mode)
        end_time = time.perf_counter()
        print(f"{mode}: move {move}, states examined {agent.nodes}, "
              f"time {end_time - start_time:.4f} s, legal {sample_board.is_legal(move)}")

    move = agent.next_move(sample_board, 'mcts')
    print("mcts: move", move, "legal (expected True):", sample_board.is_legal(move))

    #Searching shouldn't change the board
    print("Board unchanged after searching (expected True):",
          sample_board == State([[1, 1, 0, 0, 1],
                       [1, 1, 0, 0, 0],
                       [0, 0, 1, 1, 1],
                       [0, 0, 0, 1, 1],
                       [0, 0, 0, 0, 1]]))

    #If a hinger is available the agent should take the 100 point bonus
    #The middle cell H is the only hinger
    hinger_board = State([[0, 0, 0, 0, 0],
                [0, 1, 1, 1, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]])
    print("State hinger_board:")
    print(hinger_board)
    for mode in agent.modes:
        print(f"{mode} move on hinger board (expected H):", agent.next_move(hinger_board, mode))

    #the agent has to play it as there is only 1 counter left 
    last_counter = State([[0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 1]])
    print("Only move on last counter (expected Y):", agent.next_move(last_counter))

    #No moves are possible as there are no active cells 
    empty_board = State([[0] * 5 for _ in range(5)])
    print("Move on empty board (expected None):", agent.next_move(empty_board))

    # Full board: shows how much time alpha-beta saves compared with minimax
    full_board = State([[1] * 5 for _ in range(5)])
    for mode in ['minimax', 'alphabeta']:
        start_time = time.perf_counter()
        move = agent.next_move(full_board, mode)
        end_time = time.perf_counter()
        print(f"Full board {mode}: move {move}, states examined {agent.nodes}, "
              f"time {end_time - start_time:.4f} s")


# This runs tester() only when the file is run directly not when it is imported
if __name__ == '__main__':
    tester()