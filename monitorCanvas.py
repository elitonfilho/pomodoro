from qgis.PyQt.QtCore import QThread, pyqtSignal
from qgis.utils import iface

class MonitorCanvas(QThread):

    updateByMonitor = pyqtSignal()

    def __init__(self, parent = None):
        super(MonitorCanvas, self).__init__(parent)
        self.iface = iface
        self.running = True
        self.isMonitoring = True
        self.hasChangedCanvas = False

    def startMonitoring(self):
        self.isMonitoring = True
        self.hasChangedCanvas = True
        print('Started monitoring')
        iface.mapCanvas().mapCanvasRefreshed.connect(self.updateMonitoring)

    def stopMonitoring(self):
        self.isMonitoring = False
        print('Stopped monitoring')
        try:
            iface.mapCanvas().mapCanvasRefreshed.disconnect(self.updateMonitoring)
        except TypeError:
            pass

    def updateMonitoring(self):
        self.hasChangedCanvas = True

    def run(self):
        while self.running:
            if not self.isMonitoring:
                continue
            elif self.hasChangedCanvas:
                self.hasChangedCanvas = False
                QThread.sleep(10)
            elif not self.hasChangedCanvas and self.isMonitoring:
                self.updateByMonitor.emit()
                self.stopMonitoring()
                # QThread.sleep(10)



