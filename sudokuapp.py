from tkinter import *
import Solver
import random


class App(Tk):
    def __init__(self):
        Tk.__init__(self)

        self.state("zoomed")
        img = PhotoImage(file='sudokuicon.gif')
        self.tk.call('wm', 'iconphoto', self._w, img)
        self.geometry("900x800+0+0")

        # start with the sudoku "tab"
        self.frame = None
        self.change_frame(Sudoku)

    # method that changes to another frame (what is shown on screen)
    def change_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack(side='bottom')


# class that contains the commands that the user can call by pressing buttons
class Commands:
    def __init__(self, solver, canvas, information, sudokutype):
        self.solver = solver
        self.canvas = canvas
        self.information = information
        self.sudokutype = sudokutype

    # draws Sudoku on screen
    def draw_sudoku(self, array):
        self.canvas.delete("digits")
        for i in range(0, 9):
            for j in range(0, 9):
                if array[i][j] != 0:
                    y = 5 + i * 66.7 + 66.7 / 2
                    x = 5 + j * 66.7 + 66.7 / 2
                    self.canvas.create_text(x, y, text=array[i][j], tags="digits", font=("Arial", 30))

    # draws a sudoku that was solved on screen (with different colors for initial numbers and numbers that were added by
    # solving it
    def draw_solved_sudoku(self, arraystart, arrayend):
        self.canvas.delete("digits")
        for i in range(0, 9):
            for j in range(0, 9):
                color = "black" if arrayend[i][j] == arraystart[i][j] else "blue"
                y = 5 + i * 66.7 + 66.7 / 2
                x = 5 + j * 66.7 + 66.7 / 2
                self.canvas.create_text(x, y, text=arrayend[i][j], tags="digits", fill=color, font=("Arial", 30))

    # empties the sudoku board
    def empty_grid(self):
        self.solver.set_grid([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])

        self.draw_sudoku(array=self.solver.get_grid())
        self.information.config(text="emtpy " + self.sudokutype)

    # creates a sudoku with a random amount of hints (between 17 and 60) that is solvable
    def solvable_grid(self):
        self.solver.set_grid([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])

        hints = random.randint(17, 60)

        self.draw_sudoku(array=self.solver.generate_solvable_sudoku(array=self.solver.get_grid(), hints=hints))
        self.information.config(text=self.sudokutype + " with " + str(hints) + " hints")

    # solves the current sudoku
    def solve_grid(self):
        self.solver.set_backtrack(0)
        solvablegrid = []
        for i in range(0, 9):
            solvablegrid.append([])
            for j in range(0, 9):
                solvablegrid[i].append(self.solver.grid[i][j])
        if self.solver.solve_sudoku(array=self.solver.get_grid()):
            self.draw_solved_sudoku(solvablegrid, self.solver.get_grid())
            self.information.config(
                text="solved " + self.sudokutype + " with " + str(self.solver.get_backtrack()) + " backtracks")

    # creates a randomly created sudoku
    def completed_grid(self):
        self.solver.set_grid([
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0]
        ])
        if self.sudokutype == "HyperSudoku":
            if self.solver.generate_completed_hypersudoku(array=self.solver.get_grid()):
                self.draw_sudoku(array=self.solver.get_grid())
                self.information.config(text="randomly completed valid " + self.sudokutype)
        else:
            if self.solver.generate_completed_sudoku(array=self.solver.get_grid()):
                self.draw_sudoku(array=self.solver.get_grid())
                self.information.config(text="randomly completed valid " + self.sudokutype)


# frame_class for standard Sudokus, handles what is shown on screen on the Sudoku "tab"
class Sudoku(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        parent.title("Sudoku")

        # canvas that shows the Sudoku board
        self.sudokuGrid = PhotoImage(file="Sudokugrid.gif")
        canvas = Canvas(self, width=610, height=610)
        canvas.create_image(305, 305, image=self.sudokuGrid)
        canvas.pack(side='top')

        # buttons to change between frames
        button2 = Button(self, text="HyperSudoku", command=lambda: parent.change_frame(HyperSudoku), width=20)
        button2.pack(side='bottom')
        button1 = Button(self, text="XSudoku", command=lambda: parent.change_frame(XSudoku), width=20)
        button1.pack(side='bottom')

        # information text about the state the board is currently in / what user just did
        information = Label(self, text="")
        information.pack(side='bottom')

        # create Commands object with Sudoku parameters
        commands = Commands(solver=Solver.SudokuSolver(), canvas=canvas, information=information, sudokutype="Sudoku")

        # buttons to change the board
        completedbutton = Button(self, text="completed Sudoku", command=commands.completed_grid, width=20)
        completedbutton.pack(side='bottom')
        solvablebutton = Button(self, text="solvable Sudoku", command=commands.solvable_grid, width=20)
        solvablebutton.pack(side='bottom')
        solvebutton = Button(self, text="solve Sudoku", command=commands.solve_grid, width=20)
        solvebutton.pack(side='bottom')
        clearbutton = Button(self, text="empty Sudoku", command=commands.empty_grid, width=20)
        clearbutton.pack(side='bottom')

        # start with an empty board
        commands.empty_grid()


# frame_class for XSudokus, handles what is shown on screen on the XSudoku "tab"
class XSudoku(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        parent.title("XSudoku")

        # canvas that shows the XSudoku board
        self.sudokuGrid = PhotoImage(file="XSudokugrid.gif")
        canvas = Canvas(self, width=610, height=610)
        canvas.create_image(305, 305, image=self.sudokuGrid)
        canvas.pack(side='top')

        # buttons to change between frames
        button2 = Button(self, text="HyperSudoku", command=lambda: parent.change_frame(HyperSudoku), width=20)
        button2.pack(side='bottom')
        button1 = Button(self, text="Sudoku", command=lambda: parent.change_frame(Sudoku), width=20)
        button1.pack(side='bottom')

        # information text about the state the board is currently in / what user just did
        information = Label(self, text="")
        information.pack(side='bottom')

        # create Commands object with XSudoku parameters
        commands = Commands(solver=Solver.XSudokuSolver(), canvas=canvas, information=information, sudokutype="XSudoku")

        # buttons to change the board
        completedbutton = Button(self, text="completed XSudoku", command=commands.completed_grid, width=20)
        completedbutton.pack(side='bottom')
        solvablebutton = Button(self, text="solvable XSudoku", command=commands.solvable_grid, width=20)
        solvablebutton.pack(side='bottom')
        solvebutton = Button(self, text="solve XSudoku", command=commands.solve_grid, width=20)
        solvebutton.pack(side='bottom')
        clearbutton = Button(self, text="empty XSudoku", command=commands.empty_grid, width=20)
        clearbutton.pack(side='bottom')

        # start with an empty board
        commands.empty_grid()


# frame_class for HyperSudokus, handles what is shown on screen on the HyperSudoku "tab"
class HyperSudoku(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        parent.title("HyperSudoku")

        # canvas that shows the HyperSudoku board
        self.sudokuGrid = PhotoImage(file="HyperSudokugrid.gif")
        canvas = Canvas(self, width=610, height=610)
        canvas.create_image(305, 305, image=self.sudokuGrid)
        canvas.pack(side='top')

        # buttons to change between frames
        button2 = Button(self, text="XSudoku", command=lambda: parent.change_frame(XSudoku), width=20)
        button2.pack(side='bottom')
        button1 = Button(self, text="Sudoku", command=lambda: parent.change_frame(Sudoku), width=20)
        button1.pack(side='bottom')

        # information text about the state the board is currently in / what user just did
        information = Label(self, text="")
        information.pack(side='bottom')

        # create Commands object with HyperSudoku parameters
        commands = Commands(solver=Solver.HyperSudokuSolver(), canvas=canvas, information=information,
                            sudokutype="HyperSudoku")

        # buttons to change the board
        completedbutton = Button(self, text="completed HyperSudoku", command=commands.completed_grid, width=20)
        completedbutton.pack(side='bottom')
        solvablebutton = Button(self, text="solvable HyperSudoku", command=commands.solvable_grid, width=20)
        solvablebutton.pack(side='bottom')
        solvebutton = Button(self, text="solve HyperSudoku", command=commands.solve_grid, width=20)
        solvebutton.pack(side='bottom')
        clearbutton = Button(self, text="empty HyperSudoku", command=commands.empty_grid, width=20)
        clearbutton.pack(side='bottom')

        # start with an empty board
        commands.empty_grid()


app = App()
app.mainloop()
