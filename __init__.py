# -*- coding: utf-8 -*-
"""
/***************************************************************************
 Pomodoro
                                 A QGIS plugin
 Pomodoro for improvements on productivity
 Generated by Plugin Builder: http://g-sherman.github.io/Qgis-Plugin-Builder/
                             -------------------
        begin                : 2020-01-22
        copyright            : (C) 2020 by Eliton
        email                : eliton.filho@eb.mil.br
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load Pomodoro class from file Pomodoro.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .pomodoro import Pomodoro
    return Pomodoro(iface)
