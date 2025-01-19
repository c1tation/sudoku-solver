from sudoku_reader import Sudoku_reader
import random
from board import Board

class SudokuBoard(Board):
    def __init__(self, nums):
        super().__init__(nums)
        self.elements = [] # Holds the elements: boxes, rows, columns
        self._set_up_nums(nums)
        self._set_up_elems()
    
    def _set_up_nums(self, nums):
        # Set up the squares on the board (ints into Square objects)
        self.nums = [[Square(nums[i][j]) for j in range(self.n_rows)] for i in range(self.n_cols)]
        pass

    def _set_up_elems(self): # Creates the boxes, rows and column elements:
        # Rows:
        for i in range(self.n_rows):
            self.elements.append(Element())
            for j in range(self.n_cols):
                self.elements[-1].add_square((j, i))
                self.nums[j][i].elements.append(len(self.elements) - 1)

        # Cols:
        for j in range(self.n_cols):
            self.elements.append(Element())
            for i in range(self.n_rows):
                self.elements[-1].add_square((j, i))
                self.nums[j][i].elements.append(len(self.elements) - 1)

        # Boxes:
        for i in range(3):
            for j in range(3):
                self.elements.append(Element())
                for y in range(3):
                    for x in range(3):
                        self.elements[-1].add_square((x + i * 3, y + j * 3))
                        self.nums[x + i * 3][y + j * 3].elements.append(len(self.elements) - 1)
        pass
    
    def lowest_entropy(self, x, y, low): # Compares two squares, the currently found lowest entropy square and the square at (x, y)
        p_low = len(self.nums[low[0]][low[1]].possibilities) # Current lowest entropy square
        p_current = len(self.nums[x][y].possibilities) # Square being checked
        # Switch low if new square has lower entropy:
        if p_current < p_low or p_low == 0: # low may start on an already filled square with 0 possibilities, we want it to switch from this to an empty square regardless of entropy.
            low = (x, y)
        return low

    def entropy(self): # Creates the wave function. Finds all possibilities for every square.
        low = (0, 0) # Start assuming lowest entropy square is top left corner, this is because it must start somewhere on the board
        mistake = False
        for x in range(self.n_cols):
            for y in range(self.n_rows):
                square = self.nums[x][y]
                if square.number: # Skips to next square if current square is filled
                    continue
                square.possibilities = [i for i in range(1, 10) if square.is_legal(i, self.elements, self.nums)] # Lists possibilities for the square
                if not square.possibilities: # If there are no possibilities, a mistake has been made. No point in continuing this function.
                    mistake = True
                    return low, mistake
                low = self.lowest_entropy(x, y, low) # Compares low and the current square
        return low, mistake
    
    def observe(self, current): # Collapses the wave function, fills the current square
        square = self.nums[current[0]][current[1]]
        if square.number: # If square is already filled, the board is complete and we avoid overwriting anything by returning this information
            return True
        square.set_number(random.choice(square.possibilities)) # A number is chosen

    def new_attempt(self): # Resets the board
        for row in self.nums:
            for square in row:
                square.reset()
    
    def solve(self): # Solve using wave function collapse algorithm
        solved, mistake = False, False
        while not solved:
            least_possible, mistake = self.entropy() # Find the lowest entropy square
            if mistake: # Start over if a dead end is reached
                self.new_attempt()
                print('a mistake was made, starting over...')
                continue
            solved = self.observe(least_possible) # Collapses the wave function and checks if the board is solved
    
    def check_solved(self): # Checks if the board is solved. Currently unused but worth keeping for bugfixing etc.
        # Checks rows, columns and boxes for rule violations:
        for element in self.elements:
            # Creates a set of all numbers in element:
            numbers = {self.nums[s[0]][s[1]].number for s in element.squares} 
            numbers.discard(0) # 0 should not be counted as this represents an empty square
            if len(numbers) != 9: # Not solved if any set does not have 9 unique numbers
                return False
        return True

class Element: # Boxes, rows, columns
    def __init__(self) -> None:
        self.squares = [] # List of squares contained in the element
    
    def add_square(self, square): # Shortcut for adding a square to the element during _set_up_elems()
        self.squares.append(square)
    
    def contains_value(self, value, squares): # Checks whether or not a number is in the current element
        for s in self.squares:
            if squares[s[0]][s[1]].number == value:
                return True
        return False
    
    def __str__(self) -> str:
        return str(self.squares)

        
class Square:
    def __init__(self, number) -> None:
        self.number = number
        self.locked = False
        if self.number: # Prefilled squares are locked and cannot be changed
            self.locked = True
        self.elements = [] # List of elements the square is contained within
        self.possibilities = [] # Possibilities for the square, square entropy
    
    def is_legal(self, value, elements, squares): # Checks whether a number can be placed in the square
        if self.locked: # Prefilled squares cannot be filled (Perhaps an unnecessary check but no time to look into)
            return False
        for i_element in self.elements: # i_element is an index for elements list taken in from sudokuboard class
            current_element = elements[i_element]
            if current_element.contains_value(value, squares): # If the number already exists within current row, box or column, it cannot be placed here
                return False
        return True
    
    def set_number(self, value): # Sets the number in the square, resets possibilities
        self.number = value
        self.possibilities = []

    def reset(self): # Resets the square to its starting condition
        if not self.locked:
            self.number = 0
            self.possibilities = []

    def __str__(self) -> str:
        return str(self.number)


if __name__ == "__main__":
    # IMPORTANT !!!: Change file path if necessary !!!!!
    reader = Sudoku_reader("sudoku_100.csv")
    # Read text above if the program does not run
    solved = 0
    while True:
        next_board = reader.next_board()
        board = SudokuBoard(next_board)
        print(board) # Board before solving
        board.solve() # Solve the board
        solved += 1
        print(board) # Board after solving
        print("Nr solved: ", solved)