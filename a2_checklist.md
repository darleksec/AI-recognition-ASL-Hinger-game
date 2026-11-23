# a2_agent.py: checklist of what can and can't be changed


## 🔒 DO NOT CHANGE (required by the brief or used by other files)

| Item | Line | Why |
|---|---|---|
| `class Agent` | 33 | The brief names the class `Agent`, and a3 imports it |
| `__init__(self, name='B15')` (param `name`, default `'B15'`) | 38 | Brief 2.1: one parameter `name`, default = group name |
| `self.name` | 39 | Brief: instance variable must be called `name` |
| `self.modes` | 41 | Brief: instance variable must be called `modes` |
| `'minimax'`, `'alphabeta'` strings in modes | 41 | Brief: these exact elements are required |
| `__str__` | 51 | Brief 2.2 (you can reword the text it returns) |
| `next_move(self, state, mode=...)` (name and params) | 57 | Brief 2.3. a3_game.py:53 calls `next_move(state)` and relies on the default |
| `return None` when the game is over | 63 | Brief 2.3 |
| `def tester()` + `if __name__ == '__main__':` | 278, 350 | Brief 2.5 |
| `bonus = 100` | 81 | Game rule (hinger bonus, confirmed in the a1 tester), not a tuning value |
| State method calls (`legal_moves`, `state_clone`, `move`, `is_game_over`, `is_hinger`, `cost`, `letter_to_cell`, `is_legal`) | throughout | These are a1's API. Renaming them here breaks the code |
| `from a1_state import State` | 14 | Required import |

🔒 Default `mode='alphabeta'` (line 57): **keep it.** Alpha-beta is the group's chosen best strategy (it gives the same result as minimax, examines fewer states, and is deterministic).
⚠️ `'mcts'` (line 41) can be renamed, but you must also change it at line 69 (implicit fallback) and lines 304 and 324 in the tester.

---

## ✏️ VARIABLES YOU CAN CHANGE

### Tunable values (affect behaviour; mention in your report)
- [ ] `self.depth = 3` (L42): search depth for minimax and alpha-beta
- [ ] `self.iterations = 300` (L46): MCTS simulations per move
- [ ] `math.sqrt(2)` (L207): UCB1 exploration constant
- [ ] `1 / 0.5 / 0` rollout results (L229–233): win/draw/loss values

### Instance attribute names (rename everywhere they appear)
- [ ] `self.depth` (L42, 128, 185)
- [ ] `self.nodes` (L44, 87, 120, 140, 175; tester L301, 345)
- [ ] `self.iterations` (L46, 239)

### Node class (L20–31; all your own design under 2.4/2.6)
- [ ] class name `Node` (also used at L237, 257)
- [ ] `state`, `parent`, `letter`, `agent_turn`, `score` (constructor params and attributes)
- [ ] `children`, `untried`, `visits`, `wins`

### Helper method names (internal, brief 2.4; rename the call sites too)
- [ ] `move_gain` (L76; used at L97, 110, 125, 148, 162, 182, 221, 250)
- [ ] `minimax` / `minimax_move` (L86, 119; called at L66, 102, 114, 128)
- [ ] `alphabeta` / `alphabeta_move` (L139, 174; called at L68, 151, 165, 185)
- [ ] `select_child` (L199, 244), `rollout` (L214, 262), `mcts_move` (L236, 69)

### Local variables
- [ ] `move_gain`: `row`, `col`, `bonus`
- [ ] `minimax`: `maximizing`, `best_score`, `gain`, `new_state`, `value`
- [ ] `minimax_move`: `best_score`, `best_move`
- [ ] `alphabeta`: `alpha`, `beta` (standard names, so keeping them is recommended), `best_score`, `gain`, `new_state`, `value`
- [ ] `alphabeta_move`: `best_score`, `best_move`, `alpha`, `beta`
- [ ] `select_child`: `best_value`, `best_child`, `average`, `explore`
- [ ] `rollout`: `state`, `agent_turn`, `score`
- [ ] `mcts_move`: `root`, `node`, `letter`, `gain`, `score`, `new_state`, `child`, `result`, `best_child`
- [ ] loop variable `letter` (used in every method)

### tester() (L278–346)
- [ ] `agent`, `sa`, `sb`, `sc`, `empty`, `full`, `move`, `mode`, `start_time`, `end_time`
- [ ] test board layouts and the `'Bob'` name (you can add or replace scenarios. Keep the expected-value comments correct)

---

## 💬 COMMENTS (rewrite in your own words)

### Header / sections
- [ ] L1–9 module docstring (keep the module name and authors)
- [ ] L18 `Task 2.6: Node used by Monte Carlo Tree Search`
- [ ] L36 `Task 2.1: Initialiser - setting up the agent`
- [ ] L49 `Task 2.2: String representation of the agent`
- [ ] L55 `Task 2.3: next_move() - returns a legal move letter or None`
- [ ] L72 `Task 2.4: Additional variables and Supporting methods`
- [ ] L195 `Task 2.6: Monte Carlo Tree Search`
- [ ] L276 `Task 2.5: tester() - These are all the tests`

### Node
- [ ] L23 `State of the board`
- [ ] L24 `This is the node this one was reached from`
- [ ] L25 `This is the move that led to this node`
- [ ] L26 `If it is the agents turn then it will be true`
- [ ] L27 `the score is the agent score minus the opponent score so far`
- [ ] L28 *(no comment on `children`, so consider adding one)*
- [ ] L30 `Looks at how many simulations passed through`
- [ ] L31 `This stores the total result of the simulations`

### Agent init / next_move
- [ ] L40 `The playing strategies this agent can use`
- [ ] L42 *(no comment on `depth`, so consider adding one)*
- [ ] L43 `Number of states examined in the last search`
- [ ] L45 `Number of simulations MCTS runs for each move`
- [ ] L58 `Makes sure to only ask for one of the agent's strategies`
- [ ] L61 `If there are no active cells then no move can be made`

### move_gain
- [ ] L75 `This works out how many points a move is worth to the player making it`
- [ ] L79 `100 bonus if the cell is a hinger minus the cost of the move` (also fix its indentation)

### minimax
- [ ] L84 `Minimax score is agent's points - opponent's points`
- [ ] L85 `The agent tries to make it as big as possible and the opponent as small as possible`
- [ ] L89 `Stops when the depth limit is reached or if there are no counters left`
- [ ] L94 `The agent starts with the lowest possible value`
- [ ] L98 `Copies the board so the move can be tried without changing the original`
- [ ] L101 `The agent's points are added then it's the opponent's turn`
- [ ] L107 `The opponent starts with the highest possible value`
- [ ] L113 `The opponent's points are taken awaya then...` (**typo: "awaya"**)
- [ ] L118 `Tries every move at the top of the tree and returns the best one`
- [ ] L129 `This keeps the move with the highest value`

### alphabeta
- [ ] L137 `alpha is the best value the agent is guaranteed so far`
- [ ] L138 `beta is the best value the opponent is guaranteed so far`
- [ ] L153 `Updates the best value the agent can guarantee`
- [ ] L167 `Updates the best value the opponent can guarantee`
- [ ] L173 `Tries every move at the top of the tree and returns the best one using alpha-beta`
- [ ] L189 `The best value found so far becomes the new lower bound`

### MCTS
- [ ] L198 `Chooses which child to explore using the UCB1 formula`
- [ ] L204 `When it's the opponent's turn the opponent picks what is worst for the agent`
- [ ] L213 `Plays random moves until the board is empty and returns the result...`
- [ ] L235 `Runs the four MCTS steps multiple times and returns the most visited move`
- [ ] L242 `SELECTION: goes down the tree while every move has been tried`
- [ ] L246 `EXPANSION: adds one untried move as a new child`
- [ ] L261 `SIMULATION: plays the rest of the game randomly`
- [ ] L264 `BACKPROPGATION: ...` (**typo: "BACKPROPAGATION"**)
- [ ] L270 `The move that was explored the most is the most reliable choice`

### tester
- [ ] L296 `Minimax and alpha-beta should choose the same move but alpha-beta should examine less states...` ("fewer states")
- [ ] L307 `Searching shouldn't change the board`
- [ ] L315 `If a hinger is available the agent should take the 100 point bonus`
- [ ] L316 `The middle cell H is the only hinger`
- [ ] L327 `the agent has to play it as there is only 1 counter left`
- [ ] L335 `No moves are possible as there are no active cells`
- [ ] L339 `Full board: shows how much alpha-beta saves compared with minimax`
- [ ] L349 `This runs tester() only when the file is run directly not when it is imported`

---

