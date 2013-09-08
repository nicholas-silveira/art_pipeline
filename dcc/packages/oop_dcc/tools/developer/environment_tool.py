# Import Maya modules
import maya.cmds as cmds #@UnresolvedImport

# Import Pipeline modules
import core.const
import oop_maya.core

import oop_python.core.py_env as py_env
import oop_python.core.py_pyside as py_pyside

reload( py_env )

# Globals
MAYA_VERSION = oop_maya.core.get_maya_version()

UI_NAME = 'environment_tool.ui'
UI_FILE_PATH = '{0}/developer/ui/{1}'.format( core.const.oop_dcc_tools_path, UI_NAME )

WINDOW_TITLE = 'Environment Tool'
WINDOW_VERTION = 1.0
WINDOW_NAME = 'environment_tool_window'

# Import PySide or PyQt
if MAYA_VERSION >= 2014:
   import PySide.QtGui as QtGui #@UnresolvedImport
   import PySide.QtCore as QtCore #@UnresolvedImport
   
else:
   import PyQt4.QtGui as QtGui #@UnresolvedImport
   import PyQt4.QtCore as QtCore #@UnresolvedImport

ui_object, base_class = py_pyside.get_pyside_class( UI_FILE_PATH )

class Environment_Tool( base_class, ui_object ):
   def __init__( self, parent = oop_maya.core.get_maya_window(), *args ):
      super( Environment_Tool, self ).__init__( parent )
      self.setupUi( self )
      
      self.setWindowTitle( '{0} {1}'.format( WINDOW_TITLE, str( WINDOW_VERTION ) ) )
      self.connect( self.add_path_button, QtCore.SIGNAL( 'clicked()' ), self.add_path )
      self.connect( self.remove_path_button, QtCore.SIGNAL( 'clicked()' ), self.remove_path )
      #self.add_path_button.clicked.connect( self.test )
      
      self.load_paths()
      self.show()
      
   def load_paths( self ):
      paths = py_env.get_paths()
      
      for path in paths:
         self.path_list.addItem( path )
      
   def add_path( self ):
      path = py_env.add_paths( [str( self.add_path_line.text() )] )
      
      if path:
         self.path_list.addItem( path[0] )
         print path
         
   def remove_path( self ):      
      paths = self.path_list.selectedItems()
      
      for path in paths:
         py_env.remove_paths( [path.text()] )
         
         index = self.path_list.indexFromItem( path )
         self.path_list.takeItem( index.row() )

def show():
      if cmds.window( WINDOW_NAME, exists = True, q = True ):
         cmds.deleteUI( WINDOW_NAME )
         
      Environment_Tool()
      
show()
