import time
from datetime import date, timedelta
from PyQt5.QtCore import QThread, pyqtSignal

class HandlePomodoro(QThread):

    valueChanged = pyqtSignal(int)

    def __init__(self, parent=None):
        super(HandlePomodoro, self).__init__(parent)
        self.running = True
        self.duration = 120
        self.today = date.today

    def run(self):
        while self.running and self.duration:
            print('thread id', int(QThread.currentThreadId()))
            for i in range(self.duration):
                print('value', i)
                self.valueChanged.emit(i)
                self.duration -= 1
                QThread.sleep(1)

    def changeState(self):
        self.running = ~self.running

    def refreshPomodoro(self):
        self.duration = 120

    def lcdString(self):
        return f'{self.duration // 60}:{self.duration % 60}'


    # def tick(self):
    #     self.duration = self.duration - timedelta(seconds=1)

if __name__ == "__main__":
    pomodoro = HandlePomodoro()
    pomodoro.run()