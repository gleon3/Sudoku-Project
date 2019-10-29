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

        self.frame = None
        self.change_window(Sudoku)

    def change_window(self, window_class):
        new_window = window_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_window
        self.frame.pack(side='bottom')


class Commands:
    def __init__(self, solver, canvas, information, sudokutype):
        self.solver = solver
        self.canvas = canvas
        self.information = information
        self.sudokutype = sudokutype

    def draw_sudoku(self, array):
        self.canvas.delete("digits")
        for i in range(0, 9):
            for j in range(0, 9):
                if array[i][j] != 0:
                    y = 5 + i * 66.7 + 66.7 / 2
                    x = 5 + j * 66.7 + 66.7 / 2
                    self.canvas.create_text(x, y, text=array[i][j], tags="digits", font=("Arial", 30))

    def draw_solved_sudoku(self, arraystart, arrayend):
        self.canvas.delete("digits")
        for i in range(0, 9):
            for j in range(0, 9):
                color = "black" if arrayend[i][j] == arraystart[i][j] else "blue"
                y = 5 + i * 66.7 + 66.7 / 2
                x = 5 + j * 66.7 + 66.7 / 2
                self.canvas.create_text(x, y, text=arrayend[i][j], tags="digits", fill=color, font=("Arial", 30))

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

    def solve_grid(self):
        self.solver.set_backtrack(0)
        solvablegrid = []
        for i in range(0, 9):
            solvablegrid.append([])
            for j in range(0, 9):
                solvablegrid[i].append(self.solver.grid[i][j])
        if self.solver.solve_sudoku(array=self.solver.get_grid()):
            self.draw_solved_sudoku(solvablegrid, self.solver.get_grid())
            self.information.config(text="solved "+ self.sudokutype + " with " + str(self.solver.get_backtrack()) + " backtracks")

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


class Sudoku(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        parent.title("Sudoku")

        self.sudokuGrid = PhotoImage(file="Sudokugrid.gif")
        self.canvas = Canvas(self, width=610, height=610)
        self.canvas.create_image(305, 305, image=self.sudokuGrid)
        self.canvas.pack(side='top')

        button2 = Button(self, text="HyperSudoku", command=lambda: parent.change_window(HyperSudoku), width=20)
        button2.pack(side='bottom')
        button1 = Button(self, text="XSudoku", command=lambda: parent.change_window(XSudoku), width=20)
        button1.pack(side='bottom')

        self.information = Label(self, text="")
        self.information.pack(side='bottom')

        commands = Commands(solver=Solver.SudokuSolver(), canvas=self.canvas, information=self.information,
                            sudokutype="Sudoku")

        self.completedButton = Button(self, text="completed Sudoku", command=commands.completed_grid, width=20)
        self.completedButton.pack(side='bottom')
        self.solvableButton = Button(self, text="solvable Sudoku", command=commands.solvable_grid, width=20)
        self.solvableButton.pack(side='bottom')
        self.solveButton = Button(self, text="solve Sudoku", command=commands.solve_grid, width=20)
        self.solveButton.pack(side='bottom')
        self.clearButton = Button(self, text="empty Sudoku", command=commands.empty_grid, width=20)
        self.clearButton.pack(side='bottom')

        commands.empty_grid()


class XSudoku(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        parent.title("XSudoku")

        self.sudokuGrid = PhotoImage(file="XSudokugrid.gif")
        self.canvas = Canvas(self, width=610, height=610)
        self.canvas.create_image(305, 305, image=self.sudokuGrid)
        self.canvas.pack(side='top')

        button2 = Button(self, text="HyperSudoku", command=lambda: parent.change_window(HyperSudoku), width=20)
        button2.pack(side='bottom')
        button1 = Button(self, text="Sudoku", command=lambda: parent.change_window(Sudoku), width=20)
        button1.pack(side='bottom')

        self.information = Label(self, text="")
        self.information.pack(side='bottom')

        commands = Commands(solver=Solver.XSudokuSolver(), canvas=self.canvas, information=self.information,
                            sudokutype="XSudoku")

        self.completedButton = Button(self, text="completed XSudoku", command=commands.completed_grid, width=20)
        self.completedButton.pack(side='bottom')
        self.solvableButton = Button(self, text="solvable XSudoku", command=commands.solvable_grid, width=20)
        self.solvableButton.pack(side='bottom')
        self.solveButton = Button(self, text="solve XSudoku", command=commands.solve_grid, width=20)
        self.solveButton.pack(side='bottom')
        self.clearButton = Button(self, text="empty XSudoku", command=commands.empty_grid, width=20)
        self.clearButton.pack(side='bottom')

        commands.empty_grid()


class HyperSudoku(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        parent.title("HyperSudoku")

        self.sudokuGrid = PhotoImage(file="HyperSudokugrid.gif")
        self.canvas = Canvas(self, width=610, height=610)
        self.canvas.create_image(305, 305, image=self.sudokuGrid)
        self.canvas.pack(side='top')

        button2 = Button(self, text="XSudoku", command=lambda: parent.change_window(XSudoku), width=20)
        button2.pack(side='bottom')
        button1 = Button(self, text="Sudoku", command=lambda: parent.change_window(Sudoku), width=20)
        button1.pack(side='bottom')

        self.information = Label(self, text="")
        self.information.pack(side='bottom')

        commands = Commands(solver=Solver.HyperSudokuSolver(), canvas=self.canvas, information=self.information,
                            sudokutype="HyperSudoku")

        self.completedButton = Button(self, text="completed HyperSudoku", command=commands.completed_grid, width=20)
        self.completedButton.pack(side='bottom')
        self.solvableButton = Button(self, text="solvable HyperSudoku", command=commands.solvable_grid, width=20)
        self.solvableButton.pack(side='bottom')
        self.solveButton = Button(self, text="solve HyperSudoku", command=commands.solve_grid, width=20)
        self.solveButton.pack(side='bottom')
        self.clearButton = Button(self, text="empty HyperSudoku", command=commands.empty_grid, width=20)
        self.clearButton.pack(side='bottom')

        commands.empty_grid()


app = App()
app.mainloop()
