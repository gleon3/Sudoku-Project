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


class Sudoku(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        sudoku = Solver.SudokuSolver()

        parent.title("Sudoku")
        self.sudokuGitter = PhotoImage(file="Sudokugrid.gif")
        canvas = Canvas(self, width=610, height=610)
        canvas.pack(side='top')
        canvas.create_image(302,302, image=self.sudokuGitter)

        button2 = Button(self, text="HyperSudoku", command=lambda: parent.ändere_fenster(HyperSudoku), width=20)
        button2.pack(side='bottom')
        button1 = Button(self, text="XSudoku", command=lambda: parent.ändere_fenster(XSudoku), width=20)
        button1.pack(side='bottom')

        def zeichneSudoku(array):
            canvas.delete("Zahlen")
            for i in range(0, 9):
                for j in range(0, 9):
                    if array[i][j] != 0:
                        y = i * 67 + 67 / 2
                        x = j * 67 + 67 / 2
                        canvas.create_text(x, y, text=array[i][j], tags="Zahlen", font=("Arial", 30))

        def zeichneGelöstesSudoku(arraystart, arrayend):
            canvas.delete("Zahlen")
            for i in range(0, 9):
                for j in range(0, 9):
                    color = "black" if arrayend[i][j] == arraystart[i][j] else "blue"
                    # if arrayend[i][j] != 0:
                    y = i * 67 + 67 / 2
                    x = j * 67 + 67 / 2
                    canvas.create_text(x, y, text=arrayend[i][j], tags="Zahlen", fill=color, font=("Arial", 30))

        def leereGrid():
            sudoku.grid = [
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

            zeichneSudoku(array=sudoku.grid)
            information.config(text="leeres Sudokufeld")

        def spielbaresGrid():
            sudoku.grid = [
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

            hinweise = random.randint(30, 55)
            sudoku.generiereSudoku(array=sudoku.grid, hinweise=hinweise)
            information.config(text="Sudoku mit " + str(hinweise) + " Hinweisen")
            zeichneSudoku(array=sudoku.grid)

        def löseGrid():
            sudoku.backtrack = 0
            lösbaresgrid = []
            for i in range(0, 9):
                lösbaresgrid.append([])
                for j in range(0, 9):
                    lösbaresgrid[i].append(sudoku.grid[i][j])
            if sudoku.sudokuLösen(array=sudoku.grid):
                zeichneGelöstesSudoku(lösbaresgrid, sudoku.grid)
                information.config(text="Sudoku gelöst mit " + str(sudoku.backtrack) + " Backtracks")

        def neuesGrid():
            sudoku.shuffleAnzahl = 0
            sudoku.grid = [
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
            if sudoku.generiereVollständigesSudoku(array=sudoku.grid):
                zeichneSudoku(array=sudoku.grid)
                information.config(text="zufälliges gülitges Sudoku")

        information = Label(self, text="")
        leereGrid()
        information.pack(side='bottom')
        randomButton = Button(self, text="zufälliges Sudoku", command=neuesGrid, width=20)
        randomButton.pack(side='bottom')
        lösButton = Button(self, text="löse Sudoku", command=löseGrid, width=20)
        lösButton.pack(side='bottom')
        spielbarButton = Button(self, text="lösbares Sudoku", command=spielbaresGrid, width=20)
        spielbarButton.pack(side='bottom')
        clearButton = Button(self, text="leeres Sudoku", command=leereGrid, width=20)
        clearButton.pack(side='bottom')


class XSudoku(Frame):

    def __init__(self, parent):
        Frame.__init__(self, parent)

        xsudoku = Solver.XSudokuSolver();

        parent.title("XSudoku")
        self.sudokuGitter = PhotoImage(file="XSudokugrid.gif")
        canvas = Canvas(self, width=610, height=610)
        canvas.pack(side='top')
        canvas.create_image(302,302, image=self.sudokuGitter)

        button2 = Button(self, text="HyperSudoku", command=lambda: parent.ändere_fenster(HyperSudoku), width=20)
        button2.pack(side='bottom')
        button1 = Button(self, text = "Sudoku", command=lambda: parent.ändere_fenster(Sudoku), width=20)
        button1.pack(side='bottom')

        def zeichneSudoku(array):
            canvas.delete("Zahlen")
            for i in range(0, 9):
                for j in range(0, 9):
                    if array[i][j] != 0:
                        y = i * 67 + 67 / 2
                        x = j * 67 + 67 / 2
                        canvas.create_text(x, y, text=array[i][j], tags="Zahlen", font=("Arial", 30))

        def zeichneGelöstesSudoku(arraystart, arrayend):
            canvas.delete("Zahlen")
            for i in range(0, 9):
                for j in range(0, 9):
                    color = "black" if arrayend[i][j] == arraystart[i][j] else "blue"
                    # if arrayend[i][j] != 0:
                    y = i * 67 + 67 / 2
                    x = j * 67 + 67 / 2
                    canvas.create_text(x, y, text=arrayend[i][j], tags="Zahlen", fill=color, font=("Arial", 30))

        def leereGrid():
            xsudoku.grid = [
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

            zeichneSudoku(array=xsudoku.grid)
            information.config(text="leeres Sudokufeld")

        def spielbaresGrid():
            xsudoku.shuffleAnzahl = 0
            xsudoku.grid = [
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

            hinweise = random.randint(35, 60)
            xsudoku.generiereSudoku(array=xsudoku.grid, hinweise=hinweise)
            information.config(text="Sudoku mit " + str(hinweise) + " Hinweisen")
            zeichneSudoku(array=xsudoku.grid)

        def löseGrid():
            xsudoku.backtrack = 0
            lösbaresgrid = []
            for i in range(0, 9):
                lösbaresgrid.append([])
                for j in range(0, 9):
                    lösbaresgrid[i].append(xsudoku.grid[i][j])
            if xsudoku.sudokuLösen(array=xsudoku.grid):
                zeichneGelöstesSudoku(lösbaresgrid, xsudoku.grid)
                information.config(text="Sudoku gelöst mit " + str(xsudoku.backtrack) + " Backtracks")

        def neuesGrid():
            xsudoku.shuffleAnzahl = 0
            xsudoku.grid = [
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
            if xsudoku.generiereVollständigesSudoku(array=xsudoku.grid):
                zeichneSudoku(array=xsudoku.grid)
                information.config(text="zufälliges gülitges Sudoku")

        information = Label(self, text="")
        leereGrid()
        information.pack(side='bottom')
        randomButton = Button(self, text="zufälliges Sudoku", command=neuesGrid, width=20)
        randomButton.pack(side='bottom')
        lösButton = Button(self, text="löse Sudoku", command=löseGrid, width=20)
        lösButton.pack(side='bottom')
        spielbarButton = Button(self, text="lösbares Sudoku", command=spielbaresGrid, width=20)
        spielbarButton.pack(side='bottom')
        clearButton = Button(self, text="leeres Sudoku", command=leereGrid, width=20)
        clearButton.pack(side='bottom')


class HyperSudoku(Frame):
    def __init__(self, parent):
        Frame.__init__(self, parent)

        hypersudoku = Solver.HyperSudokuSolver();

        parent.title("HyperSudoku")
        self.sudokuGitter = PhotoImage(file="HyperSudokugrid.gif")
        canvas = Canvas(self, width=610, height=610)
        canvas.pack(side='top')
        canvas.create_image(302, 302, image=self.sudokuGitter)

        button2 = Button(self, text="XSudoku", command=lambda: parent.ändere_fenster(XSudoku), width=20)
        button2.pack(side='bottom')
        button1 = Button(self, text="Sudoku", command=lambda: parent.ändere_fenster(Sudoku), width=20)
        button1.pack(side='bottom')

        def zeichneSudoku(array):
            canvas.delete("Zahlen")
            for i in range(0, 9):
                for j in range(0, 9):
                    if array[i][j] != 0:
                        y = i * 67 + 67 / 2
                        x = j * 67 + 67 / 2
                        canvas.create_text(x, y, text=array[i][j], tags="Zahlen", font=("Arial", 30))

        def zeichneGelöstesSudoku(arraystart, arrayend):
            canvas.delete("Zahlen")
            for i in range(0, 9):
                for j in range(0, 9):
                    color = "black" if arrayend[i][j] == arraystart[i][j] else "blue"
                    # if arrayend[i][j] != 0:
                    y = i * 67 + 67 / 2
                    x = j * 67 + 67 / 2
                    canvas.create_text(x, y, text=arrayend[i][j], tags="Zahlen", fill=color, font=("Arial", 30))

        def leereGrid():
            hypersudoku.grid = [
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

            zeichneSudoku(array=hypersudoku.grid)
            information.config(text="leeres Sudokufeld")

        def spielbaresGrid():
            hypersudoku.grid = [
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

            hinweise = random.randint(35, 60)
            hypersudoku.generiereSudoku(array=hypersudoku.grid, hinweise=hinweise)
            information.config(text="Sudoku mit " + str(hinweise) + " Hinweisen")
            zeichneSudoku(array=hypersudoku.grid)

        def löseGrid():
            hypersudoku.backtrack = 0
            lösbaresgrid = []
            for i in range(0, 9):
                lösbaresgrid.append([])
                for j in range(0, 9):
                    lösbaresgrid[i].append(hypersudoku.grid[i][j])
            if hypersudoku.sudokuLösen(array=hypersudoku.grid):
                zeichneGelöstesSudoku(lösbaresgrid, hypersudoku.grid)
                information.config(text="Sudoku gelöst mit " + str(hypersudoku.backtrack) + " Backtracks")

        def neuesGrid():
            hypersudoku.grid = [
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
            if hypersudoku.generiereVollständigesHyperSudoku(array=hypersudoku.grid):
                zeichneSudoku(array=hypersudoku.grid)
                information.config(text="zufälliges gülitges Sudoku")

        information = Label(self, text="")
        leereGrid()
        information.pack(side='bottom')
        randomButton = Button(self, text="zufälliges Sudoku", command=neuesGrid, width=20)
        randomButton.pack(side='bottom')
        lösButton = Button(self, text="löse Sudoku", command=löseGrid, width=20)
        lösButton.pack(side='bottom')
        spielbarButton = Button(self, text="lösbares Sudoku", command=spielbaresGrid, width=20)
        spielbarButton.pack(side='bottom')
        clearButton = Button(self, text="leeres Sudoku", command=leereGrid, width=20)
        clearButton.pack(side='bottom')


app = App()
app.mainloop()
