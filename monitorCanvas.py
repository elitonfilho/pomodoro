from qgis.PyQt.QtCore import QThread, pyqtSignal
from qgis.utils import iface

class MonitorCanvas(QThread):

    updateByMonitor = pyqtSignal()

    def __init__(self, parent = None):
        super(MonitorCanvas, self).__init__(parent)
        self.iface = iface
        self.running = True
        self.hasChangedCanvas = False

    def startMonitoring(self):
        iface.mapCanvas().mapCanvasRefreshed.connect(self.updateMonitoring)

    def updateMonitoring(self):
        print(self.hasChangedCanvas)
        self.hasChangedCanvas = True

    def run(self):
        while self.running:
            if self.hasChangedCanvas:
                self.hasChangedCanvas = False
                QThread.sleep(10)
            elif not self.hasChangedCanvas:
                self.updateByMonitor.emit()
                QThread.sleep(10)



