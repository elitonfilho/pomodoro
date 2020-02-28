# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Pomodoro
                                 A QGIS plugin
 Pomodoro for improvements on productivity
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                              -------------------
        begin                : 2020-01-22
        git sha              : $Format:%H$
        copyright            : (C) 2020 by Eliton
        email                : eliton.filho@eb.mil.br
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
from qgis.PyQt.QtCore import QSettings, QTranslator, QCoreApplication, Qt, pyqtSlot
from qgis.PyQt.QtGui import QIcon, QPixmap
from qgis.PyQt.QtWidgets import QAction, QGraphicsGridLayout, QGraphicsScene, QLabel, QVBoxLayout, QHBoxLayout, QBoxLayout, QGridLayout
from PyQt5 import QtCore
# Initialize Qt resources from file resources.py
from .resources import *

# Import the code for the DockWidget
import os.path
from .pomodoro_dockwidget import PomodoroDockWidget
from .handlePomodoro import HandlePomodoro
from .monitorCanvas import MonitorCanvas


class Pomodoro:
    """QGIS Plugin Implementation."""

    def __init__(self, iface):
        """Constructor.

        :param iface: An interface instance that will be passed to this class
            which provides the hook by which you can manipulate the QGIS
            application at run time.
        :type iface: QgsInterface
        """
        # Save reference to the QGIS interface
        self.iface = iface

        # initialize plugin directory
        self.plugin_dir = os.path.dirname(__file__)

        # Declare instance attributes
        self.actions = []
        self.menu = u'&Pomodoro'
        self.toolbar = self.iface.addToolBar(u'Pomodoro')
        self.toolbar.setObjectName(u'Pomodoro')

        # Initialize Pomodoro

        self.pluginIsActive = False
        self.dockwidget = None

        self._thread = HandlePomodoro()
        self.monitor = MonitorCanvas()
        self.monitor.startMonitoring()

    def add_action(
            self,
            icon_path,
            text,
            callback,
            enabled_flag=True,
            add_to_menu=True,
            add_to_toolbar=True,
            status_tip=None,
            whats_this=None,
            parent=None):
        """Add a toolbar icon to the toolbar.

        :param icon_path: Path to the icon for this action. Can be a resource
            path (e.g. ':/plugins/foo/bar.png') or a normal file system path.
        :type icon_path: str

        :param text: Text that should be shown in menu items for this action.
        :type text: str

        :param callback: Function to be called when the action is triggered.
        :type callback: function

        :param enabled_flag: A flag indicating if the action should be enabled
            by default. Defaults to True.
        :type enabled_flag: bool

        :param add_to_menu: Flag indicating whether the action should also
            be added to the menu. Defaults to True.
        :type add_to_menu: bool

        :param add_to_toolbar: Flag indicating whether the action should also
            be added to the toolbar. Defaults to True.
        :type add_to_toolbar: bool

        :param status_tip: Optional text to show in a popup when mouse pointer
            hovers over the action.
        :type status_tip: str

        :param parent: Parent widget for the new action. Defaults None.
        :type parent: QWidget

        :param whats_this: Optional text to show in the status bar when the
            mouse pointer hovers over the action.

        :returns: The action that was created. Note that the action is also
            added to self.actions list.
        :rtype: QAction
        """

        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        action.setEnabled(enabled_flag)

        if status_tip is not None:
            action.setStatusTip(status_tip)

        if whats_this is not None:
            action.setWhatsThis(whats_this)

        if add_to_toolbar:
            self.toolbar.addAction(action)

        if add_to_menu:
            self.iface.addPluginToMenu(
                self.menu,
                action)

        self.actions.append(action)

        return action

    def initGui(self):
        """Create the menu entries and toolbar icons inside the QGIS GUI."""

        icon_path = ':/plugins/pomodoro/icon.png'
        self.add_action(
            icon_path,
            text=u'Pomodoro',
            callback=self.run,
            parent=self.iface.mainWindow())

    def onClosePlugin(self):
        """Cleanup necessary items here when plugin dockwidget is closed"""

        # disconnects
        self.dockwidget.closingPlugin.disconnect(self.onClosePlugin)

        # remove this statement if dockwidget is to remain
        # for reuse if plugin is reopened
        # Commented next statement since it causes QGIS crashe
        # when closing the docked window:
        # self.dockwidget = None

        self.pluginIsActive = False
        self._thread.terminate()
        self.monitor.terminate()

    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        self._thread.terminate()
        self.monitor.terminate()
        # #print "** UNLOAD Pomodoro"

        # for action in self.actions:
        #     self.iface.removePluginMenu(
        #         u'&Pomodoro',
        #         action)
        #     self.iface.removeToolBarIcon(action)
        # # remove the toolbar
        # del self.toolbar

    def onStart(self):
        """Starts the thread"""
        self._thread.start()
        # print('main id', int(QtCore.QThread.currentThreadId()))

    def closeEvent(self, event):
        if self._thread.isRunning():
            self._thread.quit()
            # self._thread.terminate()
        del self._thread

    def updateLCD(self):
        self.dockwidget.lcdNumber.display(self._thread.lcdString())

    def deleteLayoutItems(self):
        for idx in range(self.dockwidget.testeLayout.count()):
            item = self.dockwidget.testeLayout.itemAt(idx)
            if item is None:
                continue
            item.widget().deleteLater()

    def updateHistoric(self):
        # TODO: Append dinamically using deleteLayoutItems
        # 1: Works dinamically, but there's no limit
        #hbox = QHBoxLayout()
        # label = QLabel()
        # last = self._thread.session['historic'][-1]
        # if last:
        #     label.setPixmap(self.dockwidget.sucess)
        #     self.dockwidget.testeLayout.addWidget(label)
        # else:
        #     label.setPixmap(self.dockwidget.fail)
        #     self.dockwidget.testeLayout.addWidget(label)
        # #self.dockwidget.testeLayout.addLayout(hbox)
        # if len(self._thread.session['historic']) > 3:
        #     self.deleteLayoutItems()

        # 2: Inserts 1, 2, 3...
        # hbox = QHBoxLayout()
        # for _id, item in enumerate(self._thread.session['historic']):
        #     label = QLabel()
        #     if item:
        #         label.setPixmap(self.dockwidget.sucess)
        #         hbox.addWidget(label)
        #     else:
        #         label.setPixmap(self.dockwidget.fail)
        #         hbox.addWidget(label)
        # self.dockwidget.testeLayout.addLayout(hbox)

        # 3: Works well, but needs to pre-define layouts on ui
        items = ['icon_0', 'icon_1', 'icon_2',
                 'icon_3', 'icon_4', 'icon_5', 'icon_6']
        historic = self._thread.session['historic'].copy()
        layout = self.dockwidget.dockWidgetContents.children()
        for item in items:
            child = self.dockwidget.dockWidgetContents.findChild(QLabel, item)
            try:
                status = historic.pop()
            except IndexError:
                break
            if status:
                child.setPixmap(self.dockwidget.sucess)
            else:
                child.setPixmap(self.dockwidget.fail)

        self.dockwidget.label.setText('Estatística de uso (sucesso/falha): {}/{}'.format(
            self._thread.vars['sThisSession'],
            self._thread.vars['fThisSession']
        ))
        # hbox = QHBoxLayout()
        # for _id, item in enumerate(self._thread.session['historic']):
        #     label = QLabel()
        #     if item:
        #         label.setPixmap(self.dockwidget.sucess)
        #         hbox.addWidget(label)
        #     else:
        #         label.setPixmap(self.dockwidget.fail)
        #         hbox.addWidget(label)
        # self.dockwidget.label.setLayout(hbox)

    def updateHistoricByMonitor(self):
        if self._thread.isTimerRunning:
            self._thread.refreshPomodoroByMonitor()
            self.monitor.stopMonitoring()

    def updateHistoricByButton(self):
        self._thread.refreshPomodoro(self.monitor.isMonitoring)
        self.monitor.startMonitoring()

    def run(self):
        """Run method that loads and starts the plugin"""

        if not self.pluginIsActive:
            self.pluginIsActive = True

            # dockwidget may not exist if:
            #    first run of plugin
            #    removed on close (see self.onClosePlugin method)
            if self.dockwidget == None:
                # Create the dockwidget (after translation) and keep reference
                self.dockwidget = PomodoroDockWidget()

            # connect to provide cleanup on closing of dockwidget
            self.dockwidget.closingPlugin.connect(self.onClosePlugin)
            # connect button to refresh Pomodoro
            self.dockwidget.pushButton.clicked.connect(
                self.updateHistoricByButton)
            # connect pyqtsignal to refresh screen
            self._thread.updateTimer.connect(self.updateLCD)
            # connect pyqtsignal to refresh historic
            self._thread.updateHistoric.connect(self.updateHistoric)
            # connect pyqtsignal from monitor
            self.monitor.updateByMonitor.connect(self.updateHistoricByMonitor)
            # show the dockwidget
            # TODO: fix to allow choice of dock location
            self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockwidget)
            self.dockwidget.show()
            self._thread.start()
            self.monitor.start()
