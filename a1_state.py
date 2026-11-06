"""
Hinger Project
Coursework 001 for: CMP-5058A Artificial Intelligence

Module: a1_state.py

@author: B15 (100487471, 100464192, 100476374, 100464083)
@date:   23/10/2026
"""

# State represents one particular configuration of the Hinger board
# Each cell of grid holds the number of counters in that cell:
# If it is 0 then the cell is empty
# If it is more than 0 then the cell is active

class State:
    # Size of the Hinger board (5x5)
    size = 5 

    # -------------------------------------------------------------------
    # Task 1.1: Initialiser - This recives a 2D list grid as a parameter 
    # -------------------------------------------------------------------
    def __init__(self, grid):
        
        # Checks that the grid has the correct number of rows and columns
        assert len(grid) == State.size
        for row in grid:
            assert len(row) == State.size

        # This copies each row so even if the state changes the original list doesn't change
        self.grid = [row[:] for row in grid]

    # ----------------------------------------------------------------------------------------------------------
    # Task 1.2: String representation of the state - This gives the readable string representation of the state 
    # ----------------------------------------------------------------------------------------------------------
    def __str__(self):
    
        out = ''
        # This loops through the board one row at a time
        for row in self.grid:
            # It puts a space between each cell value and ends the row without any borders 
            out += ' '.join(str(cell) for cell in row) + '\n'
        return out

    # -------------------------------------------------------------------
    # Task 1.7: Additional Utility methods
    # -------------------------------------------------------------------
    
    #This returns a seperate copy of this state 
    def state_clone(self):
        return State(self.grid)

   #This compares two boards by looking at each cell 
    def __eq__(self, other):
        #If two states have the same value then they are equal
        for i in range(State.size):
            for j in range(State.size):
                if self.grid[i][j] != other.grid[i][j]:
                    return False
        return True

   #This converts letters into a row and column position but if a board letter isn't entered then it will return nothing 
    def letter_to_cell(self, letter):
        
        # The only board letters are single capital letters from A to Y
        if not isinstance(letter, str) or len(letter) != 1:
            return None
        if letter < 'A' or letter > 'Y':
            return None
        # A-Y is index 0-24
        index = ord(letter) - ord('A')
        # Each row has 5 cells so the divmod gives (row, column)
        return divmod(index, State.size)

    #This will convert the row and column position into its move letter according to the move-encoding scheme 
    def position_to_letter(self, row, col):
        return chr(ord('A') + row * State.size + col)

    #This returns back the list of all the postiions that are adjacent to the row and column 
    def adjacent_cells(self, row, col):
        result = []
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                # This skips the cell
                if dr == 0 and dc == 0:
                    continue
                r = row + dr
                c = col + dc
                # This only keeps the positions that are on the board
                if 0 <= r < State.size and 0 <= c < State.size:
                    result.append((r, c))
        return result

   #This checks if all the moves that are being made are legal 
    def is_legal(self, letter):
        pos = self.letter_to_cell(letter)
        if pos is None:
            return False
        row, col = pos
        return self.grid[row][col] > 0

    #This lists all of the legal letters A-Y
    def legal_moves(self):
        moves = []
        for row in range(State.size):
            for col in range(State.size):
                if self.grid[row][col] > 0:
                    moves.append(self.position_to_letter(row, col))
        return moves

   #This shows the number of active adjacent cells to the chosen cells at the time the move is made 
    def cost(self, letter):
        row, col = self.letter_to_cell(letter)
        count = 0
        for r, c in self.adjacent_cells(row, col):
            if self.grid[r][c] > 0:
                count += 1
        return count

   #This checks if a cell is a hinger by checking if it holds exactly one counter
   #If the counter is removed then the number of active regions increases 
    def is_hinger(self, row, col):
        #A hinger has to have only one counter
        if self.grid[row][col] != 1:
            return False
        #This counts the regions before the counter is removed
        before = self.numRegions()
        #This takes away a counter on a copy so this State isn't changed
        st = self.state_clone()
        st.grid[row][col] = 0
        #If the number of regions went up then it is a hinger
        return st.numRegions() > before

   #When there are no counters left then the board is finished 
    def is_game_over(self):
        return len(self.legal_moves()) == 0

    # ------------------------------------------------------------------------------
    # Task 1.3: move() recieves a letter that represents a move if it is legitimate
    # -------------------------------------------------------------------------------
    def move(self, letter):
        #This checks if the move is legitimate then it performs the corresponding action when it receives a letter A-Y
        if not self.is_legal(letter):
            return False
        row, col = self.letter_to_cell(letter)
        #This takes away a counter from the chosen cell unless the person chose Z which ends the game 
        self.grid[row][col] -= 1
        return True

    # -----------------------------------------------------------------------------------------------------------
    # Task 1.4: successors() generator - This uses a generator to make every state that is reachable in one move 
    # -----------------------------------------------------------------------------------------------------------
    def successors(self):
        for row in range(State.size):
            for col in range(State.size):
                #The counters can only be removed if the cells are active
                if self.grid[row][col] > 0:
                    #This copies the state so the original doesn't change 
                    st = self.state_clone()
                    st.grid[row][col] -= 1
                    #This gives back the successor successor and pauses until it needs the next one 
                    yield st

    # ---------------------------------------------------------------------------------------------------------
    # Task 1.5: numRegions() - This returns the number of active regions on the board using depth-first search 
    # ----------------------------------------------------------------------------------------------------------
    def numRegions(self):
        #These are the active cells that already belong to that region 
        visited = []
        regions = 0

        for row in range(State.size):
            for col in range(State.size):
                #If an active cell hasn't been visited then it starts a new region
                if self.grid[row][col] > 0 and (row, col) not in visited:
                    regions += 1
                    stack = [(row, col)]

                    #This visits every active cell that's connected to the start cell
                    while stack:
                        vertex = stack.pop()
                        if vertex not in visited:
                            visited.append(vertex)
                            #This adds the active adjacent cells to the stack
                            for r, c in self.adjacent_cells(vertex[0], vertex[1]):
                                if self.grid[r][c] > 0 and (r, c) not in visited:
                                    stack.append((r, c))
        return regions

    # -------------------------------------------------------------------------------------
    # Task 1.6: numHingers() - This returns the number of hinger cells in the current state 
    # ---------------------------------------------------------------------------------------
    def numHingers(self):
        count = 0
        for row in range(State.size):
            for col in range(State.size):
                if self.is_hinger(row, col):
                    count += 1
        return count

# -----------------------------------------------------------------------
# Task 1.8 : tester() - Theses are all the tests 
# -----------------------------------------------------------------------
def tester():
    sa = State([[1, 1, 0, 0, 1],
                [1, 1, 0, 0, 0],
                [0, 0, 1, 1, 1],
                [0, 0, 0, 1, 1],
                [0, 0, 0, 0, 1]])
    print("State s1:")
    print(sa)

    # ---- 1.8b: additional test cases ----
    print("Regions in s1 (expected 2):", sa.numRegions())
    print("Hingers in s1 (expected 2):", sa.numHingers())

    #Alice plays Y at (4,4): cost 2, no bonus
    print("Cost of Y (expected 2):", sa.cost('Y'))
    print("Is (4,4) a hinger (expected False):", sa.is_hinger(4, 4))
    sa.move('Y')
    print("State s2 after Y:")
    print(sa)

    #Bob plays M at (2,2): cost 3, bonus 100 because it is a hinger
    print("Cost of M (expected 3):", sa.cost('M'))
    print("Is (2,2) a hinger (expected True):", sa.is_hinger(2, 2))
    sa.move('M')
    print("State s3 after M:")
    print(sa)
    print("Regions in s3 (expected 3):", sa.numRegions())

    #The illegal moves have to be rejected and shouldn't change the board
    print("Move on empty cell M (expected False):", sa.move('M'))
    print("Move Z on the board (expected False):", sa.move('Z'))
    print("Move ? (expected False):", sa.move('?'))

    #If a cell has 2 counters and is active it can't be a hinger
    sb = State([[0, 0, 0, 0, 0],
                [0, 1, 2, 1, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0]])
    print("State sb:")
    print(sb)
    print("Hingers in sb (expected 0):", sb.numHingers())
    #H is at position (1,2) and it holds 1 counter 
    sb.move('H')
    print("Hingers in sb after H (expected 1):", sb.numHingers())

    #The successors() make one state for each active cell
    print("Successors of sb (expected 3):")
    for s in sb.successors():
        print(s)

    #If an board is empty then it has no regions, no hingers and no legal moves
    empty = State([[0] * 5 for _ in range(5)])
    print("Empty board regions (expected 0):", empty.numRegions())
    print("Empty board game over (expected True):", empty.is_game_over())


#This runs tester() only when the file is run directly not when it's imported
if __name__ == '__main__':
    tester()