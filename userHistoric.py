from datetime import date
from qgis.core import QgsSettings


class UserHistoric:

    def __init__(self):
        self.s = QgsSettings()
        variables = ['dateLastAcess', 'sThisSession', 'fThisSession',
                     'sTotal', 'fTotal','workTime', 'idleTime',
                     'greatWorkTime', 'greatIdleTime', 'tmpGreatWorkTime',
                     'tmpGreatIdleTime', 'idleSince', 'timeWithoutFail']
        dateLastAcess = self.s.value("pomodoro/dateLastAcess", None)
        self.lastStatus = True
        self.tick = 1
        if dateLastAcess == date.today():
            self.vars = {x: self.s.value(f"pomodoro/{x}", 0) for x in variables}
        else:
            self.vars = {x: 0 for x in variables}
        self.s.setValue('pomodoro/dateLastAcess', date.today())
    # TODO setValue should be called from an unique function which receives the param name
    def updateSucess(self):
        self.vars['sThisSession'] = int(self.vars['sThisSession']) + self.tick
        self.s.setValue('pomodoro/sThisSession', self.vars['sThisSession'])

    def updateFail(self):
        self.vars['fThisSession'] = int(self.vars['fThisSession']) + self.tick
        self.s.setValue('pomodoro/fThisSession', self.vars['fThisSession'])

    def updateWorkTime(self):
        self.vars['workTime'] = int(self.vars['workTime']) + self.tick
        self.s.setValue('pomodoro/workTime', self.vars['workTime'])
        if self.lastStatus:
            self.vars['tmpGreatWorkTime'] = int(self.vars['tmpGreatWorkTime']) + self.tick
        else:
            self.vars['tmpGreatWorkTime'] = 0
        self.updatelongestWorkTime()

    def updateIdleTime(self):
        self.vars['idleTime'] = int(self.vars['idleTime']) + self.tick
        self.s.setValue('pomodoro/idleTime', self.vars['idleTime'])
        if not self.lastStatus:
            self.vars['tmpGreatIdleTime'] = int(self.vars['tmpGreatIdleTime']) + self.tick
        else:
            self.vars['tmpGreatIdleTime'] = 0
        self.updatelongestWorkTime()

    def updatelongestWorkTime(self, newStatus):
        if self.vars['tmpGreatWorkTime'] > self.vars['greatWorkTime']:
            self.vars['greatWorkTime'] = self.vars['tmpGreatWorkTime']
        if self.vars['tmpGreatIdleTime'] > self.vars['greatIdleTime']:
            self.vars['greatIdleTime'] = self.vars['tmpGreatIdleTime']


    def updateTimeWithoutFail(self):
        self.vars['timeWithoutFail'] = int(self.vars['timeWithoutFail']) + self.tick
        self.s.setValue('pomodoro/timeWithoutFail', self.vars['timeWithoutFail'])


