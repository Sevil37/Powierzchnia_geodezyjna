# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PEW
                                 A QGIS plugin
 This plugin calculate geodesic area 
                             -------------------
        begin                : 2016-10-19
        copyright            : (C) 2016 by RS
        email                : sevil37@poczta.onet.pl
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
    """Load PEW class from file PEW.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .PEW import PEW
    return PEW(iface)
