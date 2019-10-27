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
        self.ändere_fenster(Sudoku)

    def ändere_fenster(self, fenster_klasse):
        neues_fenster = fenster_klasse(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = neues_fenster
        self.frame.pack(side='bottom')


class Commands:
    def __init__(self, solver):
        self.solver = solver

        self.information = Label(self, text="")

        self.canvas = Canvas(self, width=610, height=610)

        self.randomButton = Button(self, text="zufälliges Sudoku", command=self.neuesGrid, width=20)
        self.lösButton = Button(self, text="löse Sudoku", command=self.löseGrid, width=20)
        self.spielbarButton = Button(self, text="lösbares Sudoku", command=self.spielbaresGrid, width=20)
        self.clearButton = Button(self, text="leeres Sudoku", command=self.leereGrid, width=20)

    def zeichneSudoku(self, array):
        self.canvas.delete("Zahlen")
        for i in range(0, 9):
            for j in range(0, 9):
                if array[i][j] != 0:
                    y = 5 + i * 66.7 + 66.7 / 2
                    x = 5 + j * 66.7 + 66.7 / 2
                    self.canvas.create_text(x, y, text=array[i][j], tags="Zahlen", font=("Arial", 30))

    def zeichneGelöstesSudoku(self, arraystart, arrayend):
        self.canvas.delete("Zahlen")
        for i in range(0, 9):
            for j in range(0, 9):
                color = "black" if arrayend[i][j] == arraystart[i][j] else "blue"
                y = 5 + i * 66.7 + 66.7 / 2
                x = 5 + j * 66.7 + 66.7 / 2
                self.canvas.create_text(x, y, text=arrayend[i][j], tags="Zahlen", fill=color, font=("Arial", 30))

    def leereGrid(self):
        self.solver.setGrid([
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

        self.zeichneSudoku(array=self.solver.getGrid())
        self.information.config(text="leeres Sudokufeld")

    def spielbaresGrid(self):
        self.solver.setGrid([
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

        hinweise = random.randint(17, 60)
        
        self.zeichneSudoku(array=self.solver.generiereSudoku(array=self.solver.getGrid(), hinweise=hinweise))
        self.information.config(text="Sudoku mit " + str(hinweise) + " Hinweisen")

    def löseGrid(self):
        self.solver.setBacktrack(0)
        lösbaresgrid = []
        for i in range(0, 9):
            lösbaresgrid.append([])
            for j in range(0, 9):
                lösbaresgrid[i].append(self.solver.grid[i][j])
        if self.solver.sudokuLösen(array=self.solver.getGrid()):
            self.zeichneGelöstesSudoku(lösbaresgrid, self.solver.getGrid())
            self.information.config(text="Sudoku gelöst mit " + str(self.solver.getBacktrack()) + " Backtracks")

    def neuesGrid(self):
        self.solver.setGrid([
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
        if self.solver.generiereVollständigesSudoku(array=self.solver.getGrid()):
            self.zeichneSudoku(array=self.solver.getGrid())
            self.information.config(text="zufälliges gülitges Sudoku")


class Sudoku(Frame, Commands):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        Commands.__init__(self, Solver.SudokuSolver())

        parent.title("Sudoku")

        self.sudokuGitter = PhotoImage(file="Sudokugrid.gif")
        self.canvas.create_image(305, 305, image=self.sudokuGitter)
        self.canvas.pack(side='top')

        self.leereGrid()

        button2 = Button(self, text="HyperSudoku", command=lambda: parent.ändere_fenster(HyperSudoku), width=20)
        button2.pack(side='bottom')
        button1 = Button(self, text="XSudoku", command=lambda: parent.ändere_fenster(XSudoku), width=20)
        button1.pack(side='bottom')

        self.information.pack(side='bottom')

        self.randomButton.pack(side='bottom')
        self.spielbarButton.pack(side='bottom')
        self.lösButton.pack(side='bottom')
        self.clearButton.pack(side='bottom')


class XSudoku(Frame, Commands):

    def __init__(self, parent):
        Frame.__init__(self, parent)
        Commands.__init__(self, Solver.XSudokuSolver())

        parent.title("XSudoku")

        self.sudokuGitter = PhotoImage(file="XSudokugrid.gif")
        self.canvas.create_image(305, 305, image=self.sudokuGitter)
        self.canvas.pack(side='top')

        self.leereGrid()

        button2 = Button(self, text="HyperSudoku", command=lambda: parent.ändere_fenster(HyperSudoku), width=20)
        button2.pack(side='bottom')
        button1 = Button(self, text="Sudoku", command=lambda: parent.ändere_fenster(Sudoku), width=20)
        button1.pack(side='bottom')

        self.information.pack(side='bottom')

        self.randomButton.pack(side='bottom')
        self.spielbarButton.pack(side='bottom')
        self.lösButton.pack(side='bottom')
        self.clearButton.pack(side='bottom')


class HyperSudoku(Frame, Commands):
    def __init__(self, parent):
        Frame.__init__(self, parent)
        Commands.__init__(self, Solver.HyperSudokuSolver())

        parent.title("HyperSudoku")

        self.sudokuGitter = PhotoImage(file="HyperSudokugrid.gif")
        self.canvas.create_image(305, 305, image=self.sudokuGitter)
        self.canvas.pack(side='top')

        self.leereGrid()

        button2 = Button(self, text="XSudoku", command=lambda: parent.ändere_fenster(XSudoku), width=20)
        button2.pack(side='bottom')
        button1 = Button(self, text="Sudoku", command=lambda: parent.ändere_fenster(Sudoku), width=20)
        button1.pack(side='bottom')

        self.information.pack(side='bottom')

        self.randomButton.pack(side='bottom')
        self.spielbarButton.pack(side='bottom')
        self.lösButton.pack(side='bottom')
        self.clearButton.pack(side='bottom')

    def neuesGrid(self):
        self.solver.setGrid([
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
        if self.solver.generiereVollständigesHyperSudoku(array=self.solver.getGrid()):
            self.zeichneSudoku(array=self.solver.getGrid())
            self.information.config(text="zufälliges gülitges Sudoku")


app = App()
app.mainloop()
