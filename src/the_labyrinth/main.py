import sys
import math

from enum import Enum

# Maze format
# The character # represents a wall
# the letter . represents a hollow space
# the letter T represents your starting position
# the letter C represents the control room
# the character ? represents a cell that you have not scanned yet


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class SolutionNode:
    TOTAL_COLUMNS = -1
    TOTAL_ROWS = -1

    def __init__(self,
                 current_row: int,
                 current_column: int,
                 action_taken: Direction,
                 board: list = None,
                 parent=None):
        self.current_row = current_row
        self.current_column = current_column
        self.board = board
        self.action_taken = action_taken
        self.parent = parent
        self.fingerprint = self.get_fingerprint()
        self.has_been_visited = False
        self.element_in_position = board[self.current_row][self.current_column]

        if SolutionNode.TOTAL_ROWS == -1:
            SolutionNode.TOTAL_ROWS = len(board)

        if SolutionNode.TOTAL_COLUMNS == -1:
            SolutionNode.TOTAL_COLUMNS = len(board[0])

        # We'll wait until the node is visited in order to calculate the possible movements
        self._possible_movements = []

    def get_fingerprint(self):
        return f"{str(self.current_row)} {str(self.current_column)} {str(self.action_taken.value)}"

    def get_possible_movements(self) -> list:
        if self._possible_movements:
            return self._possible_movements

        legal_moves = []

        # UP
        if self.current_row != 0 and self.board[self.current_row - 1][self.current_column] == ".":
            up = SolutionNode(self.current_row - 1, self.current_column, Direction.UP, parent=self)
            legal_moves.append(up)

        # DOWN
        if self.current_row != SolutionNode.TOTAL_ROWS - 1 \
                and self.board[self.current_row + 1][self.current_column] == ".":
            down = SolutionNode(self.current_row + 1, self.current_column, Direction.DOWN, parent=self)
            legal_moves.append(down)

        # LEFT
        if self.current_column != 0 and self.board[self.current_row][self.current_column - 1] == ".":
            left = SolutionNode(self.current_row, self.current_column - 1, Direction.UP, parent=self)
            legal_moves.append(left)

        # RIGHT
        if self.current_row != SolutionNode.TOTAL_COLUMNS - 1 \
                and self.board[self.current_row][self.current_column + 1] == ".":
            right = SolutionNode(self.current_row, self.current_column + 1, Direction.DOWN, parent=self)
            legal_moves.append(right)

        sorted(legal_moves, key=lambda x: x.action_taken == self.action_taken)

        self._possible_movements = legal_moves
        return legal_moves

    def get_reverse_action(self):
        if self.action_taken == Direction.UP:
            return Direction.DOWN
        elif self.action_taken == Direction.DOWN:
            return Direction.UP
        elif self.action_taken == Direction.LEFT:
            return Direction.RIGHT
        else:
            return Direction.LEFT



# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# r: number of rows.
# c: number of columns.
# a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
# r, c, a = [int(i) for i in input().split()]

import sys
import math

from enum import Enum


class Direction(Enum):
    UP = "UP"
    DOWN = "DOWN"
    LEFT = "LEFT"
    RIGHT = "RIGHT"


class SolutionNode:
    TOTAL_COLUMNS = -1
    TOTAL_ROWS = -1

    def __init__(self,
                 current_row: int,
                 current_column: int,
                 action_taken: Direction,
                 board: list = None,
                 parent=None):
        self.current_row = current_row
        self.current_column = current_column
        self.board = board
        self.action_taken = action_taken
        self.parent = parent
        self.has_been_visited = False

        # We'll wait until the node is visited in order to calculate the possible movements
        self._possible_movements = []

    def get_fingerprint(self):
        return f"{str(self.current_row)} {str(self.current_column)} {str(self.action_taken.value)}"

    def get_possible_movements(self) -> list:
        if self._possible_movements:
            return self._possible_movements

        legal_moves = []

        # UP
        if self.current_row != 0 and self.board[self.current_row - 1][self.current_column] != "#":
            up = SolutionNode(self.current_row - 1, self.current_column, Direction.UP, parent=self)
            legal_moves.append(up)
            print(f"UP is possible because {self.board[self.current_row - 1][self.current_column]}", file=sys.stderr)

        # DOWN
        if self.current_row != SolutionNode.TOTAL_ROWS - 1 \
                and self.board[self.current_row + 1][self.current_column] != "#":
            down = SolutionNode(self.current_row + 1, self.current_column, Direction.DOWN, parent=self)
            legal_moves.append(down)
            print(f"DOWN is possible because {self.board[self.current_row + 1][self.current_column]}", file=sys.stderr)

        # LEFT
        if self.current_column != 0 and self.board[self.current_row][self.current_column - 1] != "#":
            left = SolutionNode(self.current_row, self.current_column - 1, Direction.LEFT, parent=self)
            legal_moves.append(left)
            print(f"LEFT is possible because {self.board[self.current_row][self.current_column - 1]}", file=sys.stderr)

        # RIGHT
        if self.current_column != SolutionNode.TOTAL_COLUMNS - 1 \
                and self.board[self.current_row][self.current_column + 1] != "#":
            right = SolutionNode(self.current_row, self.current_column + 1, Direction.RIGHT, parent=self)
            legal_moves.append(right)
            print(f"RIGHT is possible because {self.board[self.current_row][self.current_column + 1]}", file=sys.stderr)

        sorted(legal_moves, key=lambda x: x.action_taken == self.action_taken)

        self._possible_movements = legal_moves
        return legal_moves

    def get_reverse_action(self):
        if self.action_taken == Direction.UP:
            return Direction.DOWN
        elif self.action_taken == Direction.DOWN:
            return Direction.UP
        elif self.action_taken == Direction.LEFT:
            return Direction.RIGHT
        else:
            return Direction.LEFT

    def get_element_in_position(self):
        if self.board:
            return self.board[self.current_row][self.current_column]
        else:
            return None


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

# r: number of rows.
# c: number of columns.
# a: number of rounds between the time the alarm countdown is activated and the time the alarm goes off.
r, c, a = [int(i) for i in input().split()]
first_turn = True
initial_r = -1
initial_c = -1
SolutionNode.TOTAL_ROWS = r
SolutionNode.TOTAL_COLUMNS = c

stack = []
visited = set()
going_back = False

# game loop
while True:
    # kr: row where Kirk is located.
    # kc: column where Kirk is located.
    kr, kc = [int(i) for i in input().split()]

    labyrinth = []
    for i in range(r):
        row = input()  # C of the characters in '#.TC?' (i.e. one line of the ASCII maze).
        labyrinth.append(list(row))

    if first_turn:
        initial_r = kr
        initial_c = kc
        first_turn = False
        root = SolutionNode(kr, kc, None, labyrinth)
        possible_movement = root.get_possible_movements()[0]
        root.action_taken = possible_movement.action_taken
        stack.append(root)

    current_node = stack.pop()
    current_node.board = labyrinth
    current_node.current_row = kr
    current_node.current_column = kc

    if going_back:
        stack.append(current_node.parent)
        print(current_node.get_reverse_action().value)
        continue

    if current_node.get_element_in_position() == "C":
        stack.clear()
        stack.append(current_node.parent)
        going_back = True
        print(current_node.get_reverse_action().value)
        continue

    for possible_movement in current_node.get_possible_movements()[::-1]:
        if possible_movement.get_fingerprint() not in visited and not possible_movement.has_been_visited:
            stack.append(possible_movement)
            print(f"Adding {possible_movement.get_fingerprint()}", file=sys.stderr)

    visited.add(current_node.get_fingerprint())
    current_node.has_been_visited = True

    if current_node.action_taken.value:
        print(current_node.action_taken.value)
        print(current_node.action_taken.value, file=sys.stderr)

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr)

    # Kirk's next move (UP DOWN LEFT or RIGHT).
