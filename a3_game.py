"""
Hinger Project
Coursework 001 for: CMP-5058A Artificial Intelligence

Module: a3_game.py

@author: B15 (100487471, 100464192, 100476374, 100464083)
@date:   23/11/2026
"""

from a1_state import State
from a2_agent import Agent


# -----------------------------------------------------------------------
# play() - This simulates a full game of Hinger between two players
# agentA and agentB are Agent objects, or None for a human player
# -----------------------------------------------------------------------
def play(state, agentA, agentB):

    # -------------------------------------------------------------------
    # Task 3.1: Setting up the players so they can take turns
    # -------------------------------------------------------------------
    agents = [agentA, agentB]
    names = []
    for i in range(2):
        # A human player has no name so they get called Human A or Human B
        if agents[i] is None:
            names.append('Human ' + 'AB'[i])
        else:
            names.append(agents[i].name)

    # Both players start with 100 points
    scores = [100, 100]

    # agentA moves first so the turn starts at index 0
    turn = 0

    print("Starting board:")
    print(state)

    # This keeps playing while there are still counters on the board
    while not state.is_game_over():
        current_agent = agents[turn]
        # The other player is always the opposite index (0 -> 1, 1 -> 0)
        other = 1 - turn
        print(f"{names[turn]}'s turn")

        # A human types their move and an agent works it out itself
        if current_agent is None:
            move = input("Enter a move (A-Y, or Z to end the game): ").strip().upper()
        else:
            move = current_agent.next_move(state)
        print(f"{names[turn]} plays {move}")

        # ---------------------------------------------------------------
        # Task 3.2: Z means the player declares the end of the game
        # This is checked before move() because move('Z') returns False
        # and it should not be counted as an illegal move
        # ---------------------------------------------------------------
        if move == 'Z':
            print(f"{names[turn]} declared the end of the game with Z and loses.")
            print(f"{names[other]} wins with {scores[other]} points.")
            return names[other], scores[other]

        # ---------------------------------------------------------------
        # Task 3.3: Illegal moves - an empty cell, a cell that doesn't
        # exist, or anything that isn't a letter (e.g. None) ends the game
        # is_legal() returns False for all of these so nothing crashes
        # ---------------------------------------------------------------
        if not state.is_legal(move):
            print(f"{move} is an illegal move, so {names[turn]} loses.")
            print(f"{names[other]} wins with {scores[other]} points.")
            return names[other], scores[other]

        # The cost and hinger bonus are worked out BEFORE the move is made
        # because the brief says they are taken at the time of the move
        row, col = state.letter_to_cell(move)
        cost = state.cost(move)
        bonus = 0
        if state.is_hinger(row, col):
            bonus = 100
        scores[turn] = scores[turn] - cost + bonus

        # Now the counter is actually removed from the board
        state.move(move)

        print(f"Cost: {cost}, hinger bonus: {bonus}")
        print(f"Scores: {names[0]} = {scores[0]}, {names[1]} = {scores[1]}")
        print(state)

        # Switch to the other player
        turn = other

    # -------------------------------------------------------------------
    # Task 3.2: The game is over because all counters have been removed
    # The player with the higher score wins, equal scores is a draw
    # -------------------------------------------------------------------
    print("All counters have been removed.")
    print(f"Final scores: {names[0]} = {scores[0]}, {names[1]} = {scores[1]}")
    if scores[0] > scores[1]:
        print(f"{names[0]} wins.")
        return names[0], scores[0]
    if scores[1] > scores[0]:
        print(f"{names[1]} wins.")
        return names[1], scores[1]
    print("The game is a draw.")
    return None


# -----------------------------------------------------------------------
# Task 3a: tester() - These are all the tests
# -----------------------------------------------------------------------
def tester():

    # This is a small fake player that plays a fixed list of moves in order
    # It lets us force illegal moves, Z, and exact move sequences
    class ScriptedPlayer:
        def __init__(self, name, moves):
            self.name = name
            self.moves = moves

        def next_move(self, state):
            # Gives back the next move from the list and removes it
            return self.moves.pop(0)

    # This makes a fresh copy of State s1 from Figure 1.1 for each test
    def make_s1():
        return State([[1, 1, 0, 0, 1],
                      [1, 1, 0, 0, 0],
                      [0, 0, 1, 1, 1],
                      [0, 0, 0, 1, 1],
                      [0, 0, 0, 0, 1]])

    # 1. Agent vs Agent on s1
    print("=== Test 1: Agent vs Agent on s1 ===")
    result = play(make_s1(), Agent(), Agent('Bob'))
    print("Agent vs Agent result:", result)
    print()

    # 2. Playing on an empty cell - C is (0,2) which is 0 in s1
    print("=== Test 2: Illegal move on an empty cell ===")
    result = play(make_s1(), ScriptedPlayer('Cheater', ['C']), Agent('Bob'))
    print("Illegal move (expected winner Bob):", result)
    print()

    # 3. Playing a letter that isn't on the board
    print("=== Test 3: Invalid letter ===")
    result = play(make_s1(), ScriptedPlayer('Cheater', ['?']), Agent('Bob'))
    print("Invalid letter (expected winner Bob):", result)
    print()

    # 4. Declaring Z - B15 moves first, then the stub plays Z and loses
    print("=== Test 4: Player declares Z ===")
    result = play(make_s1(), Agent(), ScriptedPlayer('Quitter', ['Z']))
    print("Z declared (expected winner B15):", result)
    print()

    # 5. Draw - two isolated single counters, each costs 0 and neither is a hinger
    print("=== Test 5: Draw ===")
    draw_state = State([[1, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 0],
                        [0, 0, 0, 0, 1]])
    result = play(draw_state, Agent(), Agent('Bob'))
    print("Draw (expected None):", result)
    print()

    # 6. Correct scoring using the Figure 1.1 sequence
    # Alice plays Y (cost 2, no bonus) so her score should be 100 - 2 = 98
    # Bob then plays Z so Alice wins and her score is returned
    print("=== Test 6a: Scoring for Y ===")
    result = play(make_s1(), ScriptedPlayer('Alice', ['Y']),
                  ScriptedPlayer('Bob', ['Z']))
    print("Alice after Y (expected ('Alice', 98)):", result)
    print()

    # Alice plays Y, Bob plays M (cost 3, hinger +100) so Bob has 100 + 100 - 3 = 197
    # Alice then plays Z so Bob wins and his score is returned
    print("=== Test 6b: Scoring for M ===")
    result = play(make_s1(), ScriptedPlayer('Alice', ['Y', 'Z']),
                  ScriptedPlayer('Bob', ['M']))
    print("Bob after M (expected ('Bob', 197)):", result)
    print()

    # 7. An agent that gives back None should lose, not crash the game
    print("=== Test 7: Agent returns None ===")
    result = play(make_s1(), ScriptedPlayer('Broken', [None]), Agent('Bob'))
    print("None move (expected winner Bob):", result)


# This runs tester() only when the file is run directly not when it's imported
if __name__ == '__main__':
    tester()

# Example of a human playing against an agent (not run automatically):
# play(State([[1, 1, 0, 0, 1], [1, 1, 0, 0, 0], [0, 0, 1, 1, 1], [0, 0, 0, 1, 1], [0, 0, 0, 0, 1]]), None, Agent())
