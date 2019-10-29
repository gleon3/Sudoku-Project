import random

"""
Regeln, die beim Sudoku erfüllt sein müssen:
1. Jede der 9 Reihen muss alle Zahlen von 1 bis 9 haben.
2. Jede der 9 Spalten muss alle Zahlen von 1 bis 9 haben.
3. Jedes der 9 3x3 Teilfelder muss alle Zahlen von 1 bis 9 haben.
"""


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
        self.possibilities =[
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
        self.lösungsAnzahl = 0
        self.backtrack = 0
        
    def getLösungsAnzahl(self):
        return self.lösungsAnzahl

    def getBacktrack(self):
        return self.backtrack

    def getGrid(self):
        return self.grid

    def getPossibilities(self):
        return self.possibilities

    def setLösungsAnzahl(self, lösungsAnzahl):
        self.lösungsAnzahl = lösungsAnzahl
        
    def setBacktrack(self, backtrack):
        self.backtrack = backtrack

    def setGrid(self, grid):
        self.grid = grid

    def setPossibilities(self, possibilities):
        self.possibilities = possibilities

    # Funktion, die array(Sudoku-Gitter) geordnet als 9x9 Feld ausgibt
    def printSudoku(self, array):
        print("\n".join(" ".join(str(cell) for cell in line) for line in array))

    def findeMöglichkeiten(self, array):
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
                        if self.überprüfeFeld(array, i, j, m):
                            self.possibilities[i][j].append(m)
                    else:
                        self.possibilities[i][j] = []

    # Funktion, das leere Feld mit den wenigsten möglichen einsetzungen in array(Sudoku-Gitter) findet
    def findeLeer(self, array):
        self.findeMöglichkeiten(array)

        lowestLength = 10

        for i in range(0, 9):
            for j in range(0,9):
                if array[i][j] ==0 and len(self.possibilities[i][j]) < lowestLength:
                    lowestLength = len(self.possibilities[i][j])
                    reihe, spalte = i, j

        if lowestLength != 10:
            return reihe, spalte
        else:
            return None

    #  Funktion, um oben genannte Bedingungen für bestimmtes array(was Sudoku-Gitter repräsentiert), Feld(Reihe, Spalte) und
    #  Eingabe zu überprüfen und gibt Wahrheitwert aus, der zeigt, ob die eingabe-Zahl, die Sudoku Regeln erfüllt
    def überprüfeFeld(self, array, reihe, spalte, eingabe):

        #  überprüfe, ob eingabe-Zahl, die Reihenregel (1.) erfüllt -> falls nicht gib False aus
        for i in range(0, 9):
            if array[reihe][i] == eingabe:
                return False
        #  überprüfe, ob eingabe-Zahl, die Spaltenregel (2.) erfüllt -> falls nicht gib False aus
        for i in range(0, 9):
            if array[i][spalte] == eingabe:
                return False
        #  überprüfe, ob eingabe-Zahl, die Teilfelder-Regel (3.) erfüllt -> falls nicht gib False aus
        for i in range(0, 3):
            for j in range(0, 3):
                if array[(reihe - reihe % 3) + i][(spalte - spalte % 3) + j] == eingabe:
                    return False
        return True

    #  Funktion, die das Sudoku(als Array dargestellt) löst, falls es mehr als eine Lösung gibt wird die zweite Lösung
    #  ausgegeben, die der Algorithmus findet
    def sudokuLösen(self, array):

        #  wenn kein leeres Feld gefunden wurde, dann ist das Sudoku gelöst
        if not self.findeLeer(array):
            return True
        #  sonst gib reihe und spalte des Feldes
        else:
            reihe, spalte = self.findeLeer(array)

        for i in self.possibilities[reihe][spalte]:
            #  falls überprüfeFeld True ausgibt, d.h i an Stelle des leeren feldes verletzt Sudoku-Regeln nicht,
            #  setze leeres Feld = i
            if self.überprüfeFeld(array, reihe, spalte, i):
                array[reihe][spalte] = i

                #  falls rekursion zu einem Ende kommt, d.h kein leeres feld mehr gefunden ist, dann ist sudoku gelöst
                if self.sudokuLösen(array):
                    return True

                #  setze ursprüngliches leeres feld wieder auf leer
                array[reihe][spalte] = 0
        #  alle Zahlen für leeres Feld probiert und keine erfüllt die Sudoku-Regeln, d.h gehe zurück zu Feld, wo das
        #  Lösen noch möglich war
        self.backtrack += 1
        return False

    #  Funktion, die True zurückgibt, wenn es mehr als eine Lösung gibt
    def mehrereLösungen(self, array):
        #  wenn kein leeres Feld gefunden wurde, dann ist das Sudoku gelöst
        if not self.findeLeer(array):
            self.lösungsAnzahl += 1
            return True
        #  sonst gib reihe und spalte des Feldes
        else:
            reihe, spalte = self.findeLeer(array)

        for i in self.possibilities[reihe][spalte]:
            #  falls überprüfeFeld True ausgibt, d.h i an Stelle des leeren feldes verletzt Sudoku-Regeln nicht,
            #  setze leeres Feld = i
            if self.überprüfeFeld(array, reihe, spalte, i):
                array[reihe][spalte] = i

                #  falls rekursion zu einem Ende kommt, d.h kein leeres feld mehr gefunden ist, dann ist sudoku gelöst,
                #  also erhöht sich lösungsAnzahl um 1
                if self.mehrereLösungen(array):
                    if self.lösungsAnzahl >= 2:
                        return True

                #  setze ursprüngliches leeres feld wieder auf leer
                array[reihe][spalte] = 0
        #  alle Zahlen für leeres Feld probiert und keine erfüllt die Sudoku-Regeln, d.h gehe zurück zu Feld, wo das
        #  Lösen noch möglich war
        return False

    #  Funktion, um vollständig ausgefülltes Sudoku zu generieren
    def generiereVollständigesSudoku(self, array):

        #  wenn kein leeres Feld gefunden wurde, dann ist das Sudoku gelöst
        if not self.findeLeer(array):
            return True
        #  sonst gib reihe und spalte des Feldes
        else:
            reihe, spalte = self.findeLeer(array)
            shuffleListe = self.possibilities[reihe][spalte]
            random.shuffle(shuffleListe)

        for i in shuffleListe:
            #  falls überprüfeFeld True ausgibt, d.h i an Stelle des leeren feldes verletzt Sudoku-Regeln nicht,
            #  setze leeres Feld = i
            if self.überprüfeFeld(array, reihe, spalte, i):
                array[reihe][spalte] = i

                #  falls rekursion zu einem Ende kommt, d.h kein leeres feld mehr gefunden ist, dann ist sudoku gelöst, also
                #  wurde ein vollständiges Sudoku erstellt
                if self.generiereVollständigesSudoku(array):
                    #  gibt True aus, wenn vollständiges Sudoku erstellt wurde
                    return True

                #  setze ursprüngliches leeres feld wieder auf leer
                array[reihe][spalte] = 0
        #  alle Zahlen für leeres Feld probiert und keine erfüllt die Sudoku-Regeln, d.h gehe zurück zu Feld, wo das
        #  Lösen noch möglich war
        return False

    #  generiert lösbares Sudoku mit gegebenen hinweisen
    def generiereSudoku(self, array, hinweise):

        entferne = 81 - hinweise

        #  erstelle zufälliges gültiges Sudoku
        if self.generiereVollständigesSudoku(array):
            #  Felder, die entfernt werden sollen
            while entferne > 0:
                #  wähle zufälliges Feld, das noch nicht leer ist
                reihe = random.randint(0, 8)
                spalte = random.randint(0, 8)
                while array[reihe][spalte] == 0:
                    reihe = random.randint(0, 8)
                    spalte = random.randint(0, 8)
                array[reihe][spalte] = 0
                entferne -= 1

        return array

    #  generiert eindeutig lösbares Sudoku mit gegebenen hinweisen
    def generiereEindutigesSudoku(self, array, hinweise):

        entferne = 81 - hinweise

        #  erstelle zufälliges gültiges Sudoku
        if self.generiereVollständigesSudoku(array):
            #  Felder, die entfernt werden sollen
            while entferne > 0:
                #  wähle zufälliges Feld, das noch nicht leer ist
                reihe = random.randint(0, 8)
                spalte = random.randint(0, 8)
                while array[reihe][spalte] == 0:
                    reihe = random.randint(0, 8)
                    spalte = random.randint(0, 8)
                #  merke den Wert des Feldes, falls das Sudoku mehr als eine Lösung hat, wenn man das Feld leert
                merke = array[reihe][spalte]
                array[reihe][spalte] = 0
                entferne -= 1

                #  kopiere array und zähle Lösungen
                kopieArray = []
                for i in range(0, 9):
                    kopieArray.append([])
                    for j in range(0, 9):
                        kopieArray[i].append(array[i][j])

                self.lösungsAnzahl = 0

                #  wenn die Anzahl der Lösungen größer ist als 1, dann setze ursprünglichen Wert in leeres Feld
                if self.mehrereLösungen(kopieArray):
                    array[reihe][spalte] = merke
                    entferne += 1

        return array

    def gridValid(self, array):
        for i in range(0, 9):
            if not self.rowValid(array, i):
                return False
            if not self.columnValid(array, i):
                return False
        for i in range(0, 7, 3):
            for j in range(0, 7, 3):
                if not self.boxValid(array, i, j):
                    return False

        return True

    def rowValid(self, array, row):
        elements = []
        for i in range(0, 9):
            elements.append(array[row][i])
        elements.sort()
        if elements == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return True
        else:
            return False

    def columnValid(self, array, column):
        elements = []
        for i in range(0, 9):
            elements.append(array[i][column])
        elements.sort()
        if elements == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return True
        else:
            return False

    def boxValid(self, array, reihe, spalte):
        elements = []
        for i in range(0, 3):
            for j in range(0, 3):
                elements.append(array[(reihe - reihe % 3) + i][(spalte - spalte % 3) + j])
        elements.sort()
        if elements == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return True
        else:
            return False


"""
Bedingungen, die beim XSudoku erfüllt sein müssen:
1. Jede der 9 Reihen muss alle Zahlen von 1 bis 9 haben.
2. Jede der 9 Spalten muss alle Zahlen von 1 bis 9 haben.
3. Jedes der 9 3x3 Teilfelder muss alle Zahlen von 1 bis 9 haben.
4. Jede der Hauptdiagonalen muss alle Zahlen von 1 bis 9 haben.
"""


class XSudokuSolver(SudokuSolver):
    def __init__(self):
        SudokuSolver.__init__(self)

    #  Funktion, um oben genannte Bedingungen für bestimmtes array(was Sudoku-Gitter repräsentiert), Feld(Reihe, Spalte)
    #  und Eingabe zu überprüfen und gibt Wahrheitwert aus, der zeigt, ob die eingabe-Zahl, die XSudoku Regeln erfüllt
    def überprüfeFeld(self, array, reihe, spalte, eingabe):

        #  überprüfe, ob eingabe-Zahl, die Reihenregel (1.)  -> falls nicht gib False aus
        for i in range(0, 9):
            if array[reihe][i] == eingabe:
                return False
        #  überprüfe, ob eingabe-Zahl, die Spaltenregel erfüllt (2.) -> falls nicht gib False aus
        for i in range(0, 9):
            if array[i][spalte] == eingabe:
                return False
        #  überprüfe, ob eingabe-Zahl, die Teilfelder-Regel erfüllt (3.) -> falls nicht gib False aus
        for i in range(0, 3):
            for j in range(0, 3):
                if array[(reihe - reihe % 3) + i][(spalte - spalte % 3) + j] == eingabe:
                    return False
        #  überprüfe, ob eingabe-Zahl, die Hauptdiagonalen-Regel erfüllt -> falls nicht gib False aus
        #  obere Diagonale
        if reihe == spalte:
            for i in range(0, 9):
                if array[i][i] == eingabe:
                    return False
        #  untere Diagonale
        if reihe + spalte == 8:
            for i in range(0, 9):
                if array[8 - i][i] == eingabe:
                    return False
        #  Falls Eingabe alle Regeln erfüllt, gib True aus
        return True

    def gridValid(self, array):
        for i in range(0, 9):
            if not self.rowValid(array, i):
                return False
            if not self.columnValid(array, i):
                return False
        for i in range(0, 7, 3):
            for j in range(0, 7, 3):
                if not self.boxValid(array, i, j):
                    return False

        if not self.diagonalsValid(array):
            return False

        return True

    def diagonalsValid(self, array):
        elements = []
        for i in range(0, 9):
            elements.append(array[i][i])
            elements.append(array[i][8-i])
        elements.sort()
        if elements == [1, 1, 2, 2, 3, 3, 4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 9, 9]:
            return True
        else:
            return False


"""
Bedingungen, die beim Hyper Sudoku erfüllt sein müssen:
1. Jede der 9 Reihen muss alle Zahlen von 1 bis 9 haben.
2. Jede der 9 Spalten muss alle Zahlen von 1 bis 9 haben.
3. Jedes der 9 3x3 Teilfelder muss alle Zahlen von 1 bis 9 haben.
4. Jedes der 4 extra 3x3 Teilfelder muss alle Zahlen von 1 bis 9 haben
"""


class HyperSudokuSolver(SudokuSolver):
    def __init__(self):
        SudokuSolver.__init__(self)

    #  Funktion, um oben genannte Bedingungen für bestimmtes array(was Sudoku-Gitter repräsentiert), Feld(Reihe, Spalte)
    #  und Eingabe zu überprüfen und gibt Wahrheitwert aus, der zeigt, ob die eingabe-Zahl, die HyperSudoku Regeln
    #  erfüllt
    def überprüfeFeld(self, array, reihe, spalte, eingabe):

        #  überprüfe, ob eingabe-Zahl, die Reihenregel erfüllt (1.) -> falls nicht gib False aus
        for i in range(0, 9):
            if array[reihe][i] == eingabe:
                return False
        #  überprüfe, ob eingabe-Zahl, die Spaltenregel erfüllt (2.) -> falls nicht gib False aus
        for i in range(0, 9):
            if array[i][spalte] == eingabe:
                return False
        #  überprüfe, ob eingabe-Zahl, die Teilfelder-Regel erfüllt (3.) -> falls nicht gib False aus
        for i in range(0, 3):
            for j in range(0, 3):
                if array[(reihe - reihe % 3) + i][(spalte - spalte % 3) + j] == eingabe:
                    return False
        #  überpüfe, ob eingabe-Zahl, die extra Teilfelder-Regel (4.) erfüllt -> falls nicht gib False aus
        #  überprüfe Teilfeld obenlinks
        if 1 <= reihe <= 3 and 1 <= spalte <= 3:
            for i in range(3):
                for j in range(3):
                    if array[reihe - reihe + 1 + i][spalte - spalte + 1 + j] == eingabe:
                        return False
        #  überprüfe Teilfeld obenrechts
        if 1 <= reihe <= 3 and 5 <= spalte <= 7:
            for i in range(3):
                for j in range(3):
                    if array[reihe - reihe + 1 + i][spalte - (spalte + 1) % 3 + j] == eingabe:
                        return False
        #  überprüfe Teilfeld untenlinks
        if 5 <= reihe <= 7 and 1 <= spalte <= 3:
            for i in range(3):
                for j in range(3):
                    if array[reihe - (reihe + 1) % 3 + i][spalte - spalte + 1 + j] == eingabe:
                        return False
        #  überprüfe Teilfeld untenrechts
        if 5 <= reihe <= 7 and 5 <= spalte <= 7:
            for i in range(3):
                for j in range(3):
                    if array[reihe - (reihe + 1) % 3 + i][spalte - (spalte + 1) % 3 + j] == eingabe:
                        return False
        return True

    def generiereSquares(self, array):
        liste=[1,2,3,4,5,6,7,8,9]

        c = 0
        random.shuffle(liste)
        for i in range(0, 3):
            for j in range(0, 3):
                array[i][j] = liste[c]
                c += 1

        c = 0
        random.shuffle(liste)
        for i in range(5, 8):
            for j in range(5, 8):
                array[i][j] = liste[c]
                c+=1

    #  Funktion, um vollständig ausgefülltes Sudoku zu generieren
    def generiereVollständigesHyperSudoku(self, array):
        self.generiereSquares(array)
        if self.generiereVollständigesSudoku(array):
            return True
        else:
            return False

    #  generiert lösbares Sudoku mit gegebenen hinweisen
    def generiereSudoku(self, array, hinweise):

        entferne = 81 - hinweise

        #  erstelle zufälliges gültiges Sudoku
        if self.generiereVollständigesHyperSudoku(array):
            #  Felder, die entfernt werden sollen
            while entferne > 0:
                #  wähle zufälliges Feld, das noch nicht leer ist
                reihe = random.randint(0, 8)
                spalte = random.randint(0, 8)
                while array[reihe][spalte] == 0:
                    reihe = random.randint(0, 8)
                    spalte = random.randint(0, 8)
                array[reihe][spalte] = 0
                entferne -= 1

        return array

    #  generiert eindeutig lösbares Sudoku mit gegebenen hinweisen
    def generiereEindeutigesSudoku(self, array, hinweise):

        entferne = 81 - hinweise

        #  erstelle zufälliges gültiges Sudoku
        if self.generiereVollständigesHyperSudoku(array):
            #  Felder, die entfernt werden sollen
            while entferne > 0:
                #  wähle zufälliges Feld, das noch nicht leer ist
                reihe = random.randint(0, 8)
                spalte = random.randint(0, 8)
                while array[reihe][spalte] == 0:
                    reihe = random.randint(0, 8)
                    spalte = random.randint(0, 8)
                #  merke den Wert des Feldes, falls das Sudoku mehr als eine Lösung hat, wenn man das Feld leert
                merke = array[reihe][spalte]
                array[reihe][spalte] = 0
                entferne -= 1

                #  kopiere array und zähle Lösungen
                kopieArray = []
                for i in range(0, 9):
                    kopieArray.append([])
                    for j in range(0, 9):
                        kopieArray[i].append(array[i][j])

                self.lösungsAnzahl = 0

                #  wenn die Anzahl der Lösungen größer ist als 1, dann setze ursprünglichen Wert in leeres Feld
                if self.mehrereLösungen(kopieArray):
                    array[reihe][spalte] = merke
                    entferne += 1

        return array

    def gridValid(self, array):
        for i in range(0, 9):
            if not self.rowValid(array, i):
                return False
            if not self.columnValid(array, i):
                return False
        for i in range(0, 7, 3):
            for j in range(0, 7, 3):
                if not self.boxValid(array, i, j):
                    return False

        for i in range(1, 6, 4):
            for j in range(1, 6, 4):
                if not self.extraBoxValid(array, i, j):
                    return False

        return True

    def extraBoxValid(self, array, reihe, spalte):
        elements = []
        #  überprüfe Teilfeld obenlinks
        if 1 <= reihe <= 3 and 1 <= spalte <= 3:
            for i in range(3):
                for j in range(3):
                    elements.append(array[reihe - reihe + 1 + i][spalte - spalte + 1 + j])
        #  überprüfe Teilfeld obenrechts
        if 1 <= reihe <= 3 and 5 <= spalte <= 7:
            for i in range(3):
                for j in range(3):
                    elements.append(array[reihe - reihe + 1 + i][spalte - (spalte + 1) % 3 + j])
        #  überprüfe Teilfeld untenlinks
        if 5 <= reihe <= 7 and 1 <= spalte <= 3:
            for i in range(3):
                for j in range(3):
                    elements.append(array[reihe - (reihe + 1) % 3 + i][spalte - spalte + 1 + j])
        #  überprüfe Teilfeld untenrechts
        if 5 <= reihe <= 7 and 5 <= spalte <= 7:
            for i in range(3):
                for j in range(3):
                    elements.append(array[reihe - (reihe + 1) % 3 + i][spalte - (spalte + 1) % 3 + j])

        elements.sort()
        if elements == [1, 2, 3, 4, 5, 6, 7, 8, 9]:
            return True
        else:
            return False


solv = SudokuSolver()
if solv.generiereVollständigesSudoku(solv.grid):
    solv.printSudoku(solv.grid)
    print(solv.gridValid(solv.grid))