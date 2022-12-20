import sys, random
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
        self.gameWord = "привет"
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



    def getRandomWord(self):
        with open('words.txt', 'r') as file:
            words_file = file.read()
            words = list(map(str, words_file.split()))
            self.gameWord = random.choice(words)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    ex.show()
    sys.exit(app.exec())
