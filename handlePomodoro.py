import time
from datetime import date, timedelta
from PyQt5.QtCore import QThread, pyqtSignal
from qgis.core import QgsSettings

class HandlePomodoro(QThread):

    updateTimer = pyqtSignal(int)
    updateHistoric = pyqtSignal(list)

    def __init__(self, parent=None):
        super(HandlePomodoro, self).__init__(parent)
        self.running = True
        self.duration = 10
        self.today = date.today
        self.session = {
            'historic' : []
        }

        # Reads old settings
        s = QgsSettings()


    def run(self):
        # if not self.duration:
        #     self.session['historic'].append(True)
        #     self.updateHistoric.emit(self.session['historic'])
        while self.running:
            if self.duration:
                print('thread id', int(QThread.currentThreadId()))
                for i in range(self.duration):
                    # print('value', i)
                    self.updateTimer.emit(i)
                    self.duration -= 1
                    QThread.sleep(1)

        # timer = QTimer(self)
        # timer.setInterval(1000)
        # timer.timeout.connect(self.updateText)
        # timer.start()

    def changeState(self):
        self.running = ~self.running

    def refreshPomodoro(self):
        # TODO: append the pixmap itself
        if self.duration:
            self.session['historic'].append(False)
        elif not self.duration:
            self.session['historic'].append(True)
        self.duration = 10
        self.updateHistoric.emit(self.session['historic'])
        # print(self.session)

    def lcdString(self):
        return f'{self.duration // 60}:{self.duration % 60}'


    # def tick(self):
    #     self.duration = self.duration - timedelta(seconds=1)

if __name__ == "__main__":
    pomodoro = HandlePomodoro()
    pomodoro.run()