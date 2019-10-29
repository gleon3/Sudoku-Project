import random

"""
conditions that have to be fulfilled in Sudoku:
1. each of the 9 rows has to contain all of the digits from 1 to 9.
2. each of the 9 columns has to contain all of the digits from 1 to 9.
3. each of the 9 3x3-subgrids has to contain all of the digits from 1 to 9.
"""


# class that contains the functionalities to solve and generate Sudokus
class SudokuSolver:
    def __init__(self):
        self.grid = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ]
        self.possibilities = [
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
        ]
        self.solutionCount = 0
        self.backtrack = 0

    def get_solution_count(self):
        return self.solutionCount

    def get_backtrack(self):
        return self.backtrack

    def get_grid(self):
        return self.grid

    def get_possibilities(self):
        return self.possibilities

    def set_solution_count(self, solutioncount):
        self.solutionCount = solutioncount

    def set_backtrack(self, backtrack):
        self.backtrack = backtrack

    def set_grid(self, grid):
        self.grid = grid

    def set_possibilities(self, possibilities):
        self.possibilities = possibilities

    # method to print out array (sudoku grid) user-friendly
    def print_sudoku(self, array):
        print("\n".join(" ".join(str(cell) for cell in line) for line in array))

    # method to find possible candidates for array (sudoku grid) for each cell
    def find_possibilities(self, array):
        self.possibilities = [
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
            [[], [], [], [], [], [], [], [], []],
        ]

        for i in range(0, 9):
            for j in range(0, 9):
                for m in range(1, 10):
                    if array[i][j] == 0:
                        if self.check_cell(array, i, j, m):
                            self.possibilities[i][j].append(m)

    # method to find empty cell with least possible candidates for an array (sudoku grid),
    # returns the row and column if empty cell was found, returns None otherwise
    def find_empty(self, array):
        self.find_possibilities(array)

        lowestlength = 10

        for i in range(0, 9):
            for j in range(0, 9):
                if array[i][j] == 0 and len(self.possibilities[i][j]) < lowestlength:
                    lowestlength = len(self.possibilities[i][j])
                    row, column = i, j

        if lowestlength != 10:
            return row, column
        else:
            return None

    # method to check if a cell (row, column) of an array (sudoku grid) fulfills sudoku conditions listed above for
    # given input
    # returns True if it is and False otherwise
    def check_cell(self, array, row, column, _input):

        # check if input fulfills row condition (1.) -> if not return False
        for i in range(0, 9):
            if array[row][i] == _input:
                return False
        # check if input fulfills column condition (2.) -> if not return False
        for i in range(0, 9):
            if array[i][column] == _input:
                return False
        # check if input fulfills subgrid condition (3.) -> if not return False
        for i in range(0, 3):
            for j in range(0, 3):
                if array[(row - row % 3) + i][(column - column % 3) + j] == _input:
                    return False
        # if input fulfills all conditions then return True
        return True

    # method that solves sudoku (represented by array)
    # returns True if first solution was found, if no solution was found returns False
    def solve_sudoku(self, array):

        # if no empty cell was found, then return True, which means sudoku is solved,
        # otherwise save row and column of the empty cell
        if not self.find_empty(array):
            return True
        else:
            row, column = self.find_empty(array)

        #
        for i in self.possibilities[row][column]:
            #  falls check_cell True ausgibt, d.h i an Stelle des leeren feldes verletzt Sudoku-Regeln nicht,
            #  setze leeres Feld = i
            if self.check_cell(array, row, column, i):
                array[row][column] = i

                #  falls rekursion zu einem Ende kommt, d.h kein leeres feld mehr gefunden ist, dann ist sudoku gelöst
                if self.solve_sudoku(array):
                    return True

                #  setze ursprüngliches leeres feld wieder auf leer
                array[row][column] = 0
        #  alle Zahlen für leeres Feld probiert und keine erfüllt die Sudoku-Regeln, d.h gehe zurück zu Feld, wo das
        #  Lösen noch möglich war
        self.backtrack += 1
        return False

    #  Funktion, die True zurückgibt, wenn es mehr als eine Lösung gibt
    def has_multiple_solutions(self, array):
        #  wenn kein leeres Feld gefunden wurde, dann ist das Sudoku gelöst
        if not self.find_empty(array):
            self.solutionCount += 1
            return True
        #  sonst gib row und column des Feldes
        else:
            row, column = self.find_empty(array)

        for i in self.possibilities[row][column]:
            #  falls check_cell True ausgibt, d.h i an Stelle des leeren feldes verletzt Sudoku-Regeln nicht,
            #  setze leeres Feld = i
            if self.check_cell(array, row, column, i):
                array[row][column] = i

                #  falls rekursion zu einem Ende kommt, d.h kein leeres feld mehr gefunden ist, dann ist sudoku gelöst,
                #  also erhöht sich solutionCount um 1
                if self.has_multiple_solutions(array):
                    if self.solutionCount >= 2:
                        return True

                #  setze ursprüngliches leeres feld wieder auf leer
                array[row][column] = 0
        #  alle Zahlen für leeres Feld probiert und keine erfüllt die Sudoku-Regeln, d.h gehe zurück zu Feld, wo das
        #  Lösen noch möglich war
        return False

    # method that generates a randomly completed sudoku (represented by array)
    # returns True if a sudoku was generated
    def generate_completed_sudoku(self, array):

        #  wenn kein leeres Feld gefunden wurde, dann ist das Sudoku gelöst
        if not self.find_empty(array):
            return True
        #  sonst gib row und column des Feldes
        else:
            row, column = self.find_empty(array)
            shuffleliste = self.possibilities[row][column]
            random.shuffle(shuffleliste)

        for i in shuffleliste:
            #  falls check_cell True ausgibt, d.h i an Stelle des leeren feldes verletzt Sudoku-Regeln nicht,
            #  setze leeres Feld = i
            if self.check_cell(array, row, column, i):
                array[row][column] = i

                #  falls rekursion zu einem Ende kommt, d.h kein leeres feld mehr gefunden ist, dann ist sudoku gelöst, also
                #  wurde ein vollständiges Sudoku erstellt
                if self.generate_completed_sudoku(array):
                    #  gibt True aus, wenn vollständiges Sudoku erstellt wurde
                    return True

                #  setze ursprüngliches leeres feld wieder auf leer
                array[row][column] = 0
        #  alle Zahlen für leeres Feld probiert und keine erfüllt die Sudoku-Regeln, d.h gehe zurück zu Feld, wo das
        #  Lösen noch möglich war
        return False

    # method that generates a solvable sudoku (represented by array) with given hints
    # returns the array that was generated
    def generate_solvable_sudoku(self, array, hints):

        # cells to remove are total cells (81) - hints
        remove = 81 - hints

        # generates completed sudoku
        if self.generate_completed_sudoku(array):
            # do until enough cells are removed (until there are given hints cells left)
            while remove > 0:
                # choose random cell that is not yet removed
                row = random.randint(0, 8)
                column = random.randint(0, 8)
                while array[row][column] == 0:
                    row = random.randint(0, 8)
                    column = random.randint(0, 8)
                array[row][column] = 0
                remove -= 1

        return array

    # method that generates a uniquely solvable sudoku (represented by array) with given hints
    # returns the array that was generated
    def generate_unique_sudoku(self, array, hints):

        # cells to remove are total cells (81) - hints
        remove = 81 - hints

        # generates completed sudoku
        if self.generate_completed_sudoku(array):
            # do until enough cells are removed (until there are given hints cells left)
            while remove > 0:
                # choose random cell that is not yet removed
                row = random.randint(0, 8)
                column = random.randint(0, 8)
                while array[row][column] == 0:
                    row = random.randint(0, 8)
                    column = random.randint(0, 8)
                # remember value of removed cell in case sudoku has more than one solution if cell is emptied
                remember = array[row][column]
                array[row][column] = 0
                remove -= 1

                # copy array as has_multiple_solutions has side effects, it changes the array parameter
                arraycopy = []
                for i in range(0, 9):
                    arraycopy.append([])
                    for j in range(0, 9):
                        arraycopy[i].append(array[i][j])

                self.solutionCount = 0

                # if sudoku has multiple solutions, put initial value in empty field and increase remove by one as
                # no cell was removed in that case
                if self.has_multiple_solutions(arraycopy):
                    array[row][column] = remember
                    remove += 1

        return array

    def grid_is_valid(self, array):
        for i in range(0, 9):
            if not self.row_is_valid(array, i):
                return False
            if not self.column_is_valid(array, i):
                return False
        for i in range(0, 7, 3):
            for j in range(0, 7, 3):
                if not self.box_is_valid(array, i, j):
                    return False

        return True

    def row_is_valid(self, array, row):
        elements = []
        for i in range(0, 9):
            elements.append(array[row][i])
        elements.sort()
        if elements == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return True
        else:
            return False

    def column_is_valid(self, array, column):
        elements = []
        for i in range(0, 9):
            elements.append(array[i][column])
        elements.sort()
        if elements == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return True
        else:
            return False

    def box_is_valid(self, array, row, column):
        elements = []
        for i in range(0, 3):
            for j in range(0, 3):
                elements.append(array[(row - row % 3) + i][(column - column % 3) + j])
        elements.sort()
        if elements == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return True
        else:
            return False


"""
conditions that have to be fulfilled in XSudoku:
1. each of the 9 rows has to contain all of the digits from 1 to 9.
2. each of the 9 columns has to contain all of the digits from 1 to 9.
3. each of the 9 3x3-subgrids has to contain all of the digits from 1 to 9.
4. both of the main diagonals has to contain all of the digits from 1 to 9.
"""


# class that contains the functionalities to solve and generate XSudokus, inherits most functionalities from
# SudokuSolver
class XSudokuSolver(SudokuSolver):
    def __init__(self):
        SudokuSolver.__init__(self)

    # method to check if a cell (row, column) of an array (sudoku grid) fulfills xsudoku conditions listed above for
    # given input
    # returns True if it is and False otherwise
    def check_cell(self, array, row, column, _input):

        # check if input fulfills row condition (1.) -> if not return False
        for i in range(0, 9):
            if array[row][i] == _input:
                return False
        # check if input fulfills column condition (2.) -> if not return False
        for i in range(0, 9):
            if array[i][column] == _input:
                return False
        # check if input fulfills subgrid condition (3.) -> if not return False
        for i in range(0, 3):
            for j in range(0, 3):
                if array[(row - row % 3) + i][(column - column % 3) + j] == _input:
                    return False
        # check if input fulfills main diagonal condition (4.) -> if not return False
        # upper main diagonal
        if row == column:
            for i in range(0, 9):
                if array[i][i] == _input:
                    return False
        # bottom main diagonal
        if row + column == 8:
            for i in range(0, 9):
                if array[8 - i][i] == _input:
                    return False
        # if input fulfills all conditions then return True
        return True

    def grid_is_valid(self, array):
        for i in range(0, 9):
            if not self.row_is_valid(array, i):
                return False
            if not self.column_is_valid(array, i):
                return False
        for i in range(0, 7, 3):
            for j in range(0, 7, 3):
                if not self.box_is_valid(array, i, j):
                    return False

        if not self.diagonals_are_valid(array):
            return False

        return True

    def diagonals_are_valid(self, array):
        elements = []
        for i in range(0, 9):
            elements.append(array[i][i])
            elements.append(array[i][8 - i])
        elements.sort()
        if elements == [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]:
            return True
        else:
            return False


"""
conditions that have to be fulfilled in Sudoku:
1. each of the 9 rows has to contain all of the digits from 1 to 9.
2. each of the 9 columns has to contain all of the digits from 1 to 9.
3. each of the 9 3x3-subgrids has to contain all of the digits from 1 to 9.
4. each of the 4 additional interior 3x3 subgrids has to contain all of the digits from 1 to 9.
"""


# class that contains the functionalities to solve and generate HyperSudokus, inherits most functionalities from
# SudokuSolver
class HyperSudokuSolver(SudokuSolver):
    def __init__(self):
        SudokuSolver.__init__(self)

    # method to check if a cell (row, column) of an array (sudoku grid) fulfills hypersudoku conditions listed above for
    # given input
    # returns True if it is and False otherwise
    def check_cell(self, array, row, column, _input):

        # check if input fulfills row condition (1.) -> if not return False
        for i in range(0, 9):
            if array[row][i] == _input:
                return False
        # check if input fulfills column condition (2.) -> if not return False
        for i in range(0, 9):
            if array[i][column] == _input:
                return False
        # check if input fulfills subgrid condition (3.) -> if not return False
        for i in range(0, 3):
            for j in range(0, 3):
                if array[(row - row % 3) + i][(column - column % 3) + j] == _input:
                    return False
        # check if input fullfills additional suubgrid condition (4.) -> if not return False
        # additional subgrid top left
        if 1 <= row <= 3 and 1 <= column <= 3:
            for i in range(3):
                for j in range(3):
                    if array[row - row + 1 + i][column - column + 1 + j] == _input:
                        return False
        # additional subgrid top right
        if 1 <= row <= 3 and 5 <= column <= 7:
            for i in range(3):
                for j in range(3):
                    if array[row - row + 1 + i][column - (column + 1) % 3 + j] == _input:
                        return False
        # additional subgrid bottom left
        if 5 <= row <= 7 and 1 <= column <= 3:
            for i in range(3):
                for j in range(3):
                    if array[row - (row + 1) % 3 + i][column - column + 1 + j] == _input:
                        return False
        # additional subgrid bottom right
        if 5 <= row <= 7 and 5 <= column <= 7:
            for i in range(3):
                for j in range(3):
                    if array[row - (row + 1) % 3 + i][column - (column + 1) % 3 + j] == _input:
                        return False
        # if input fulfills all conditions then return True
        return True

    # method that generates top left subgrid and bottom left additional subgrid randomly
    # returns the generated array
    def generate_squares(self, array):
        liste = [1, 2, 3, 4, 5, 6, 7, 8, 9]

        # generates top left subgrid randomly
        c = 0
        random.shuffle(liste)
        for i in range(0, 3):
            for j in range(0, 3):
                array[i][j] = liste[c]
                c += 1

        # generates bottom left additional subgrid randomly
        c = 0
        random.shuffle(liste)
        for i in range(5, 8):
            for j in range(5, 8):
                array[i][j] = liste[c]
                c += 1

        return array

    # method that generates a randomly completed hypersudoku (represented by array)
    # returns True if a sudoku was generated
    def generate_completed_hypersudoku(self, array):
        if self.generate_completed_sudoku(self.generate_squares(array)):
            return True
        else:
            return False

    # method that generates a solvable hypersudoku (represented by array) with given hints
    # returns the array that was generated
    def generate_solvable_sudoku(self, array, hints):

        # cells to remove are total cells (81) - hints
        remove = 81 - hints

        # generates completed hypersudoku
        if self.generate_completed_hypersudoku(array):
            # do until enough cells are removed (until there are given hints cells left)
            while remove > 0:
                # choose random cell that is not yet removed
                row = random.randint(0, 8)
                column = random.randint(0, 8)
                while array[row][column] == 0:
                    row = random.randint(0, 8)
                    column = random.randint(0, 8)
                array[row][column] = 0
                remove -= 1

        return array

    # method that generates a uniquely solvable hypersudoku (represented by array) with given hints
    # returns the array that was generated
    def generate_unique_sudoku(self, array, hints):

        # cells to remove are total cells (81) - hints
        remove = 81 - hints

        # generates completed hypersudoku
        if self.generate_completed_hypersudoku(array):
            # do until enough cells are removed (until there are given hints cells left)
            while remove > 0:
                # choose random cell that is not yet removed
                row = random.randint(0, 8)
                column = random.randint(0, 8)
                while array[row][column] == 0:
                    row = random.randint(0, 8)
                    column = random.randint(0, 8)
                # remember value of removed cell in case hypersudoku has more than one solution if cell is emptied
                remember = array[row][column]
                array[row][column] = 0
                remove -= 1

                # copy array as has_multiple_solutions has side effects, it changes the array parameter
                arraycopy = []
                for i in range(0, 9):
                    arraycopy.append([])
                    for j in range(0, 9):
                        arraycopy[i].append(array[i][j])

                self.solutionCount = 0

                # if hypersudoku has multiple solutions, put initial value in empty field and increase remove by one as
                # no cell was removed in that case
                if self.has_multiple_solutions(arraycopy):
                    array[row][column] = remember
                    remove += 1

        return array

    def grid_is_valid(self, array):
        for i in range(0, 9):
            if not self.row_is_valid(array, i):
                return False
            if not self.column_is_valid(array, i):
                return False
        for i in range(0, 7, 3):
            for j in range(0, 7, 3):
                if not self.box_is_valid(array, i, j):
                    return False

        for i in range(1, 6, 4):
            for j in range(1, 6, 4):
                if not self.additional_box_is_valid(array, i, j):
                    return False

        return True

    def additional_box_is_valid(self, array, row, column):
        elements = []
        # additional subgrid top left
        if 1 <= row <= 3 and 1 <= column <= 3:
            for i in range(3):
                for j in range(3):
                    elements.append(array[row - row + 1 + i][column - column + 1 + j])
        # additional subgrid top right
        if 1 <= row <= 3 and 5 <= column <= 7:
            for i in range(3):
                for j in range(3):
                    elements.append(array[row - row + 1 + i][column - (column + 1) % 3 + j])
        # additional subgrid bottom left
        if 5 <= row <= 7 and 1 <= column <= 3:
            for i in range(3):
                for j in range(3):
                    elements.append(array[row - (row + 1) % 3 + i][column - column + 1 + j])
        # additional subgrid bottom right
        if 5 <= row <= 7 and 5 <= column <= 7:
            for i in range(3):
                for j in range(3):
                    elements.append(array[row - (row + 1) % 3 + i][column - (column + 1) % 3 + j])

        elements.sort()
        if elements == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return True
        else:
            return False
