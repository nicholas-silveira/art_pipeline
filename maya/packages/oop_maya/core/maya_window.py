

import maya.OpenMayaUI #@UnresolvedImport

import __init__ as oop_maya

maya_version = oop_maya.maya_version()

if maya_version >= 2014:
   import PySide.QtGui as QtGui #@UnresolvedImport
   import PySide.QtCore as QtCore #@UnresolvedImport
   import pysideuic #@UnresolvedImport
   import shiboken #@UnresolvedImport
   
else:
   import PyQt4.QtGui as QtGui #@UnresolvedImport
   import PyQt4.QtCore as QtCore #@UnresolvedImport
   import sip #@UnresolvedImport
   
def wrapinstance( ptr, base = None ):
   """
   Nathan Horne
   """
   if ptr is None:
      return None
   ptr = long( ptr ) #Ensure type
   if globals().has_key( 'shiboken' ):
      if base is None:
         qObj = shiboken.wrapInstance( long( ptr ), QtCore.QObject )
         metaObj = qObj.metaObject()
         cls = metaObj.className()
         superCls = metaObj.superClass().className()
         if hasattr( QtGui, cls ):
            base = getattr( QtGui, cls )
         elif hasattr( QtGui, superCls ):
            base = getattr( QtGui, superCls )
         else:
            base = QtGui.QWidget
      return shiboken.wrapInstance( long( ptr ), base )
   elif globals().has_key( 'sip' ):
      base = QtCore.QObject
      return sip.wrapinstance( long( ptr ), base )
   else:
      return None

def get_maya_window():
   maya_window_util = maya.OpenMayaUI.MQtUtil.mainWindow()

   if maya_version >= 2014:
      maya_window = wrapinstance( long( maya_window_util ), QtGui.QWidget )
      
   else:
      maya_window = sip.wrapinstance( long( maya_window_util ), QtCore.QObject )

   return maya_window
