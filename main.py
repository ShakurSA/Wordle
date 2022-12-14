import socket
import sys, random
import threading

import PyQt6.sip
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
from PyQt6.QtCore import *


class Game(QWidget):
    def __init__(self):
        super().__init__()
        # создание сокета и подключение клиента к серверу
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect(('127.0.0.1', 2455))

        self.title = "Wordle"
        self.left = 50
        self.top = 50
        self.width = 600
        self.height = 500
        self.currentRow = 0
        self.gameWord = ""
        self.defaultUI()

    def defaultUI(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setWindowTitle(self.title)
        self.getRandomWord()
        # отправка загадонного слова на сервер
        self.client.send(self.gameWord.encode('koi8-r'))

        # создание и запуск потоков
        receive_thread = threading.Thread(target=self.receive)
        receive_thread.start()

        grid = QGridLayout()
        grid.setRowMinimumHeight(0, 30)
        grid.setRowMinimumHeight(7, 30)
        grid.setColumnMinimumWidth(0, 30)
        grid.setColumnMinimumWidth(6, 30)
        self.setStyleSheet("""
        background: 'white';
        """)
        self.setLayout(grid)
        self.titleLabel = QLabel("5 БУКВ")
        self.titleLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setStyleSheet("""
        font-size: 40px;
        font-weight: bold;
        margin: 0px 30px 30px 30px;
        """)
        grid.addWidget(self.titleLabel, 0, 0, 1, 7)


        self.gameBoxes = [[] for x in range(5)]

        positions = [(i + 1, j + 1) for i in range(5) for j in range(5)]
        for i, position in enumerate(positions):
            self.gameBoxes[position[0] - 1].append(QLineEdit())
            grid.addWidget(self.gameBoxes[position[0] - 1][position[1] - 1], *position)

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



        # User message
        self.userMessage = QLabel(" ")
        self.userMessage.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.userMessage.setStyleSheet("""
        font-size: 16px
        """)
        grid.addWidget(self.userMessage, 7, 0, 1, 7)


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
        self.buttonGuess.clicked.connect(self.send_on_server)
        grid.addWidget(self.buttonGuess, 8, 2, 1, 3)



    def send_on_server(self):
        currentRowWord = ''
        for i in self.gameBoxes[self.currentRow]:
            currentRowWord += i.text().lower()
        message = currentRowWord
        self.client.send(message.encode('koi8-r'))

    def receive(self):
        while True:
            try:
                message = self.client.recv(1024).decode('koi8-r')
                if message != 'СЛОВО':
                    self.buttonGuessClicked(message)


            except:
                self.userMessage.setText("Error! Reload app")
                self.client.close()
                break

    def getRandomWord(self):
        with open('words.txt', 'r') as file:
            words_file = file.read()
            words = list(map(str, words_file.split()))
            self.gameWord = random.choice(words)




    def buttonGuessClicked(self, message):
        if self.checkInputsValid(message) == False:
            self.userMessage.setText("Вводите только русские слова")
        elif self.checkWin(message) == False:
            self.userMessage.setText(" ")
            if self.currentRow < 4:
                self.colourActiveRow()
                self.activateNextRow()
            else:
                self.colourActiveRow()
                self.gameOver()

    def gameOver(self):
        self.userMessage.setText(f"Вы проиграли:( Слово {self.gameWord}")


    def activateNextRow(self):
        for i in range(5):
            self.gameBoxes[self.currentRow + 1][i].setStyleSheet("""
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

    def checkWin(self, message):
        win = False
        if message == self.gameWord:
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
            message = 'конецигры'
            self.client.send(message.encode('koi8-r'))

        return win


    def checkInputsValid(self, message):
        alphabet = set('абвгдеёжзийклмнопрстуфхцчшщъыьэюя')
        valid = True
        for i in message:
            if i.lower() not in alphabet:
                valid = False
        with open('words.txt', 'r') as file:
            file_words = file.readline()
            if message not in file_words:
                valid = False
        return valid


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Game()
    ex.show()
    sys.exit(app.exec())