from datetime import date
from qgis.core import QgsSettings


class UserHistoric:

    def __init__(self):
        self.s = QgsSettings()
        variables = ['dateLastAcess', 'sThisSession', 'fThisSession',
                     'sTotal', 'fTotal', 'sTimeWithoutFail']
        dateLastAcess = self.s.value("pomodoro/dateLastAcess", None)
        if dateLastAcess == date.today():
            self.vars = {x: self.s.value(f"pomodoro/{x}", 0) for x in variables}
        else:
            self.vars = {x: 0 for x in variables}
        self.s.setValue('pomodoro/dateLastAcess', date.today())

    def updateSucess(self):
        self.vars['sThisSession'] = int(self.vars['sThisSession']) + 1
        self.s.setValue('pomodoro/sThisSession', self.vars['sThisSession'])

    def updateFail(self):
        self.vars['fThisSession'] = int(self.vars['fThisSession']) + 1
        self.s.setValue('pomodoro/fThisSession', self.vars['fThisSession'])


    def updateTimeWithoutFail(self):
        self.vars['sTimeWithoutFail'] = int(self.vars['sTimeWithoutFail']) + 1
        self.s.setValue('pomodoro/sTimeWithoutFail', self.vars['sTimeWithoutFail'])


