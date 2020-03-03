import time
from datetime import date, timedelta
from PyQt5.QtCore import QThread, pyqtSignal
from qgis.core import QgsSettings
from .userHistoric import UserHistoric


class HandlePomodoro(QThread, UserHistoric):

    updateTimer = pyqtSignal(int)
    updateHistoric = pyqtSignal(list)

    def __init__(self, parent=None):
        super(HandlePomodoro, self).__init__(parent)
        self.running = True
        # TODO: Use QTimer()
        self.duration = 900
        self.today = date.today
        self.isTimerRunning = True
        # TODO: use a simple array
        self.session = {
            'historic': []
        }

    def run(self):
        while self.running:
            if self.duration:
                for i in range(self.duration):
                    if self.isTimerRunning:
                        self.updateTimer.emit(i)
                        self.duration -= 1
                        if not self.duration:
                            self.triggerSuccess()
                            self.isTimerRunning = False
                        # TODO: use QThread.sleep()
                        time.sleep(1)

        # timer = QTimer(self)
        # timer.setInterval(1000)
        # timer.timeout.connect(self.updateText)
        # timer.start()

    def refreshPomodoroByButton(self, isMonitoring=True):
        # TODO: append the pixmap itself
        if isMonitoring and self.duration:
            self.triggerFail()
        self.duration = 900
        self.isTimerRunning = True

    def refreshPomodoroByMonitor(self, isMonitoring=True):
        self.isTimerRunning = False
        if self.duration:
            self.triggerFail()

    def triggerSuccess(self):
        self.updateSucess()
        self.session['historic'].append(True)
        self.updateHistoric.emit(self.session['historic'])

    def triggerFail(self):
        self.updateFail()
        if self.duration:
            self.session['historic'].append(False)
        self.updateHistoric.emit(self.session['historic'])

    def lcdString(self):
        return '{:2}:{:0>2}'.format(self.duration // 60, self.duration % 60)