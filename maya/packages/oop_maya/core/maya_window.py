

import maya.OpenMayaUI #@UnresolvedImport

import oop_maya.core as oop_maya

print oop_maya
#maya_version = oop_maya.maya_version()
'''
if maya_version >= 2014:
   import PySide.QtGui as QtGui #@UnresolvedImport
   import PySide.QtCore as QtCore #@UnresolvedImport
   import pysideuic #@UnresolvedImport
   import shiboken #@UnresolvedImport
   
else:
   import PyQt4.QtGui as QtGui #@UnresolvedImport
   import PyQt4.QtCore as QtCore #@UnresolvedImport
   import PyQt4.uic as uic #@UnresolvedImport
   import sip #@UnresolvedImport


def get_maya_window():

   maya_window = None
   maya_window_util = maya.OpenMayaUI.MQtUtil.mainWindow()

   if not maya_window_util:
      oop_maya.error( '!' )
      return False

   if maya_version >= 2014:
      maya_window = sip.wrapinstance( long( maya_window_util ), QtGui.QWidget )
      
   else:
      maya_window = sip.wrapinstance( long( maya_window_util ), QtCore.QObject )

   return maya_window
'''