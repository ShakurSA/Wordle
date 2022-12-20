import sys, random

import PyQt6.sip
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class Game(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "Wordle"
        self.left = 50
        self.top = 50
        self.width = 600
        self.height = 500
        self.currentRow = 0
        self.gameWord = "ножка"
        self.defaultUI()

    def defaultUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        #self.getRandomWord()
        grid = QGridLayout()
        grid.setRowMinimumHeight(0, 30)
        grid.setRowMinimumHeight(7, 30)
        grid.setColumnMinimumWidth(0, 30)
        grid.setColumnMinimumWidth(6, 30)
        self.setStyleSheet("""
        background: 'white';
        """)
        self.setLayout(grid)
        self.titleLabel = QLabel("5 букв")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
        font-size: 40px;
        font-weight: bold;
        margin: 30px 30px 30px 30px;
        """)
        grid.addWidget(self.titleLabel, 0, 0, 1, 7)

        self.gameBoxes = [[] for x in range(5)]

        positions = [(i + 1, j + 1) for i in range(5) for j in range(5)]
        for i, position in enumerate(positions):
            self.gameBoxes[position[0]-1].append(QLineEdit())
            grid.addWidget(self.gameBoxes[position[0]-1][position[1]-1],*position)

        for i, row in enumerate(self.gameBoxes):
            for gameBox in row:
                gameBox.setMaxLength(1)
                gameBox.setAlignment(Qt.AlignmentFlag.AlignCenter)
                gameBox.setMinimumWidth(85)
                gameBox.setMinimumHeight(85)
                gameBox.setStyleSheet("""
                border: 2px solid '#000000';
                font-size: 30px;
                margin: 10px 10px 10px 10px;
                background: 'white';  
                """)
                if i != self.currentRow:
                    gameBox.setReadOnly(True)
                    gameBox.setStyleSheet("""
                    border: 2px solid '#000000';
                    font-size: 30px;
                    margin: 10px 10px 10px 10px;
                    background: 'light grey';  
                    """)

        #User message
        self.userMessage = QLabel(" ")
        self.userMessage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.userMessage.setStyleSheet("""
        font-size: 16px
        """)
        grid.addWidget(self.userMessage, 7, 0, 1, 7)

        # button_reset
        self.buttonReset = QPushButton("Играть снова")
        self.buttonReset.setStyleSheet("""
        *{
        border: 2px solid '#000000';
        font-weight: bold;
        font-size: 20px;
        margin: 0px 0px 30px 0px;
        color: 'black';
        background: 'red';
        }
        *:hover{
        background: 'dark red';
        color: 'white';
        }
        """)
        self.buttonReset.clicked.connect(self.buttonResetClicked)
        grid.addWidget(self.buttonReset, 8, 2, 1, 3)
        self.buttonReset.hide()

        # button_guess
        self.buttonGuess = QPushButton("Ответить")
        self.buttonGuess.setStyleSheet("""
                *{
                border: 2px solid '#000000';
                font-weight: bold;
                font-size: 20px;
                margin: 0px 0px 30px 0px;
                color: 'black';
                background: 'light green';
                }
                *:hover{
                background: 'dark green';
                color: 'white';
                }
                """)
        self.buttonGuess.clicked.connect(self.buttonGuessClicked)
        grid.addWidget(self.buttonGuess, 8, 2, 1, 3)


    def getRandomWord(self):
        with open('words.txt', 'r') as file:
            words_file = file.read()
            words = list(map(str, words_file.split()))
            self.gameWord = random.choice(words)

    def buttonResetClicked(self):
        self.getRandomWord()
        self.currentRow = 0
        self.userMessage = " "
        for i, row in enumerate(self.gameBoxes):
            for box in row:
                box.setStyleSheet("""
                border: 2px solid '#000000';
                font-size: 30px;
                margin: 10px 10px 10px 10px;
                background: 'white';
                """)
                box.setReadOnly(False)
                box.setText('')
                if i != self.currentRow:
                    box.setReadOnly(True)
                    box.setStyleSheet("""
                    border: 2px solid '#000000';
                    font-size: 30px;
                    margin: 10px 10px 10px 10px;
                    background: 'light grey';
                    """)
        self.buttonSwap()



    def buttonGuessClicked(self):
        if self.checkInputsValid() == False:
            self.userMessage.setText("Вводите только русские буквы!")
            self.userMessage.repaint()
        elif self.checkWin() == False:
            self.userMessage.setText(" ")
            self.userMessage.repaint()
            if self.currentRow < 4:
                self.colourActiveRow()
                self.activateNextRow()
            else:
                self.colourActiveRow()
                self.gameOver()

    def gameOver(self):
        self.userMessage.setText(f"Вы проиграли:( Слово {self.gameWord}")
        self.userMessage.repaint()
        self.buttonSwap()

    def activateNextRow(self):
        for i in range(5):
            self.gameBoxes[self.currentRow+1][i].setStyleSheet("""
            border: 2px solid '#000000';
                font-size: 30px;
                margin: 10px 10px 10px 10px;
                background: 'white';
            """)
            self.gameBoxes[self.currentRow + 1][i].setReadOnly(False)
        self.currentRow += 1


    def colourActiveRow(self):
        for i in range(5):
            self.gameBoxes[self.currentRow][i].setReadOnly(True)
            boxVal = self.gameBoxes[self.currentRow][i].text().lower()
            if boxVal == self.gameWord[i]:
                self.gameBoxes[self.currentRow][i].setStyleSheet("""
                border: 2px solid '#000000';
                font-size: 30px;
                background: 'green';
                margin: 10px 10px 10px;
                """)

            elif boxVal in self.gameWord:
                self.gameBoxes[self.currentRow][i].setStyleSheet("""
                border: 2px solid '#000000';
                font-size: 30px;
                background: 'yellow';
                margin: 10px 10px 10px;
                """)

            else:
                self.gameBoxes[self.currentRow][i].setStyleSheet("""
                border: 2px solid '#000000';
                font-size: 30px;
                background: 'dark grey';
                margin: 10px 10px 10px;
                """)

    def checkWin(self):
        currentRowWord = ""
        win = False
        for i in self.gameBoxes[self.currentRow]:
            currentRowWord += i.text()
        if currentRowWord == self.gameWord:
            win = True
            for i in self.gameBoxes[self.currentRow]:
                i.setStyleSheet("""
                border: 2px solid '#000000';
                font-size: 30px;
                background: 'green';
                margin: 10px 10px 10px;
                """)
                i.setReadOnly(True)
            self.userMessage.setText('ПОБЕДА!')
            self.userMessage.repaint()
            self.buttonSwap()
        return win

    def buttonSwap(self):
        if self.buttonGuess.isVisible():
            self.buttonGuess.hide()
            self.buttonReset.show()
        else:
            self.buttonReset.hide()
            self.buttonGuess.show()


    def checkInputsValid(self, alphabet=set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')):
        valid = True
        for i in self.gameBoxes[self.currentRow]:
            if i.text().lower() not in alphabet:
                valid = False
        return valid




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    ex.show()
    sys.exit(app.exec())
