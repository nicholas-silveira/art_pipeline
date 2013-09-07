

import core.const

import oop_maya.core as oop_maya
import oop_python.core.py_pyside as py_pyside

UI_NAME = 'environment_tool.ui'
UI_FILE_PATH = '{0}/developer/ui/{1}'.format( core.const.oop_dcc_tools_path, UI_NAME )

ui_object, base_class = py_pyside.get_ui_class( UI_FILE_PATH )

class Environment_Tool( base_class, ui_object ):
   def __init__( self, parent = oop_maya.get_maya_window(), *args ):
      super( Environment_Tool, self ).__init__( parent )
      
      self.setupUi( self )
      self.show()
