# -*- coding: utf-8 -*-
"""
/***************************************************************************
 PEW
                                 A QGIS plugin
 This plugin calculate geodesic area 
                              -------------------
        begin                : 2016-10-19
        git sha              : $Format:%H$
        copyright            : (C) 2016 by RS
        email                : sevil37@poczta.onet.pl
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
from PyQt4.QtCore import QSettings, QTranslator, qVersion, QCoreApplication
from PyQt4.QtGui import QAction, QIcon
from qgis.core import *
from PyQt4.QtCore import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialog
from PEW_dialog import PEWDialog
import os.path


class PEW:
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
        # initialize locale
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(
            self.plugin_dir,
            'i18n',
            'PEW_{}.qm'.format(locale))

        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)

            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)

        # Create the dialog (after translation) and keep reference
        self.dlg = PEWDialog()

        # Declare instance attributes
        self.actions = []
        self.menu = self.tr(u'&PEW')
        # TODO: We are going to let the user set this up in a future iteration
        self.toolbar = self.iface.addToolBar(u'PEW')
        self.toolbar.setObjectName(u'PEW')

    # noinspection PyMethodMayBeStatic
    def tr(self, message):
        """Get the translation for a string using Qt translation API.

        We implement this ourselves since we do not inherit QObject.

        :param message: String for translation.
        :type message: str, QString

        :returns: Translated version of message.
        :rtype: QString
        """
        # noinspection PyTypeChecker,PyArgumentList,PyCallByClass
        return QCoreApplication.translate('PEW', message)


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

        icon_path = ':/plugins/PEW/icon.png'
        self.add_action(
            icon_path,
            text=self.tr(u'calculate geodesic area '),
            callback=self.run,
            parent=self.iface.mainWindow())


    def unload(self):
        """Removes the plugin menu item and icon from QGIS GUI."""
        for action in self.actions:
            self.iface.removePluginMenu(
                self.tr(u'&PEW'),
                action)
            self.iface.removeToolBarIcon(action)
        # remove the toolbar
        del self.toolbar


    def run(self):
        """Run method that performs all the real work"""
        layers = self.iface.legendInterface().layers()
        self.dlg.comboBox.clear() #Clear the QComboBox before loading layers
        layer_list = []
        for layer in layers:
            layer_list.append(layer.name())
        
        self.dlg.comboBox.addItems(layer_list)
        # show the dialog
        self.dlg.show()
        # Run the dialog event loop
        result = self.dlg.exec_()
        # See if OK was pressed
        if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
            #layer = self.iface.activeLayer()
            selectedLayerIndex = self.dlg.comboBox.currentIndex()
            layer = layers[selectedLayerIndex]
            layer.dataProvider().addAttributes([QgsField('pow_mat', QVariant.Double),
                                    QgsField('X_2000', QVariant.Double),
                                    QgsField('Y_2000', QVariant.Double),
                                    QgsField('Xgk', QVariant.Double),
                                    QgsField('Ygk', QVariant.Double),
                                    QgsField('v', QVariant.Double),
                                    QgsField('u', QVariant.Double),
                                    QgsField('sigma', QVariant.Double),
                                    QgsField('skal_m', QVariant.Double),
                                    QgsField('delta_p', QVariant.Double),
                                    QgsField('pow_geod', QVariant.Double),
                                    QgsField('pow_ha', QVariant.Double, len=10, prec=4)])
            layer.updateFields()
            idx_pow_mat = layer.fieldNameIndex('pow_mat')
            idx_x_2000 = layer.fieldNameIndex('X_2000')
            idx_y_2000 = layer.fieldNameIndex('Y_2000')
            idx_Xgk = layer.fieldNameIndex('Xgk')
            idx_Ygk = layer.fieldNameIndex('Ygk')
            idx_v = layer.fieldNameIndex('v')
            idx_u = layer.fieldNameIndex('u')
            idx_sigma = layer.fieldNameIndex('sigma')
            idx_skal_m = layer.fieldNameIndex('skal_m')
            idx_delta_p = layer.fieldNameIndex('delta_p')
            idx_pow_geod = layer.fieldNameIndex('pow_geod')
            idx_pow_ha = layer.fieldNameIndex('pow_ha')
        
            layer.startEditing()
            for f in layer.getFeatures():
                area = f.geometry().area()
                cent = f.geometry().centroid()
                cent_x = cent.asPoint().y()
                cent_y = cent.asPoint().x()
                layer.changeAttributeValue(f.id(),idx_pow_mat, area)
                layer.changeAttributeValue(f.id(),idx_x_2000, cent_x)
                layer.changeAttributeValue(f.id(),idx_y_2000, cent_y)
            
            e1 = QgsExpression("X_2000/0.999923")
            e3 = QgsExpression("Ygk*0.000002")
            e4 = QgsExpression("(Xgk-5800000)*0.000002")
            e5 = QgsExpression("-7.7+0.999923*v^2*(306.752873+(-0.312616*u)+(0.006382*u^2)+(0.158591*v^2))")
            e6 = QgsExpression("(sigma*10^-5)+1")
            e7 = QgsExpression("pow_mat*(skal_m^2-1)")
            e8 = QgsExpression("pow_mat-delta_p")

            e1.prepare(layer.pendingFields())
            e3.prepare(layer.pendingFields())
            e4.prepare(layer.pendingFields())
            e5.prepare(layer.pendingFields())
            e6.prepare(layer.pendingFields())
            e7.prepare(layer.pendingFields())
            e8.prepare(layer.pendingFields())
            
            pas = int(self.dlg.comboBox_2.currentText()) #pobiera wartosc z listy i zamienia ja na liczbe
            if pas == 5:
                for e in layer.getFeatures():
                    e2 = QgsExpression("(Y_2000-(5000000+500000))/0.999923")
                    e2.prepare(layer.pendingFields())
                    value_e2 = e2.evaluate(e)
                    layer.changeAttributeValue(e.id(), idx_Ygk, value_e2)
            elif pas == 6:
                for e in layer.getFeatures():
                    e2 = QgsExpression("(Y_2000-(6000000+500000))/0.999923")
                    e2.prepare(layer.pendingFields())
                    value_e2 = e2.evaluate(e)
                    layer.changeAttributeValue(e.id(), idx_Ygk, value_e2)
            elif pas == 7:
                for e in layer.getFeatures():
                    e2 = QgsExpression("(Y_2000-(7000000+500000))/0.999923")
                    e2.prepare(layer.pendingFields())
                    value_e2 = e2.evaluate(e)
                    layer.changeAttributeValue(e.id(), idx_Ygk, value_e2)
            elif pas == 8:
                for e in layer.getFeatures():
                    e2 = QgsExpression("(Y_2000-(8000000+500000))/0.999923")
                    e2.prepare(layer.pendingFields())
                    value_e2 = e2.evaluate(e)
                    layer.changeAttributeValue(e.id(), idx_Ygk, value_e2)
            layer.commitChanges()
            
            layer.startEditing()
            for e in layer.getFeatures(): #wykonywanie poszczegolnych wzorow 
                value_e1 = e1.evaluate(e)
                layer.changeAttributeValue(e.id(), idx_Xgk, value_e1)

            layer.commitChanges()
            
            layer.startEditing()
            for k in layer.getFeatures():
                value_e3 = e3.evaluate(k)
                value_e4 = e4.evaluate(k)
                layer.changeAttributeValue(k.id(), idx_v, value_e3)
                layer.changeAttributeValue(k.id(), idx_u, value_e4)

            layer.commitChanges()
            layer.startEditing()

            for m in layer.getFeatures():
                value_e5 = e5.evaluate(m)
                layer.changeAttributeValue(m.id(), idx_sigma, value_e5)

            layer.commitChanges()

            layer.startEditing()
            for n in layer.getFeatures():
                value_e6 = e6.evaluate(n)
                layer.changeAttributeValue(n.id(), idx_skal_m, value_e6)

            layer.commitChanges()

            layer.startEditing()
            for l in layer.getFeatures():
                value_e7 = e7.evaluate(l)
                layer.changeAttributeValue(l.id(), idx_delta_p, value_e7)

            layer.commitChanges()

            layer.startEditing()
            for o in layer.getFeatures():
                value_e8 = e8.evaluate(o)
                layer.changeAttributeValue(o.id(), idx_pow_geod, value_e8)

            layer.commitChanges()
            
            layer.startEditing()
            for p in layer.getFeatures():
                e9 = QgsExpression("pow_geod/10000")
                e9.prepare(layer.pendingFields())
                value_e9 = e9.evaluate(p)
                layer.changeAttributeValue(p.id(), idx_pow_ha, value_e9)
            
            layer.commitChanges()
            
            #usuwanie zbednych kolumn  
            res=layer.dataProvider().deleteAttributes([idx_x_2000, idx_y_2000, idx_Xgk, idx_Ygk, idx_v, idx_u, idx_sigma, idx_skal_m])
            layer.updateFields()