from datetime import date
from qgis.core import QgsSettings

class UserHistoric:

    def __init__(self):
        s = QgsSettings()
        variables = ['dateLastAcess''sThisSession', 'fThisSession', 'sTotal', 'fTotal', 'sTimeWithoutFail']
        dateLastAcess = s.value("pomodoro/dateLastAcess", None)
        if dateLastAcess == date.today():
            self.vars = {x:s.value(f"pomodoro/{x}", None) for x in variables}
        else:
            self.vars = {x:None for x in variables}
        s.setValue('pomodoro/dateLastAcess', date.today())
    
    def updateSucess(self):
        pass

    def updateFail(self):
        pass

    def updateTimeWithoutFail(self):
        pass

    