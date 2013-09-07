import oop_maya.core as oop_maya
import oop_python.core as oop_python #@UnresolvedImport

UI_FILE_PATH = 'C:\\Users\\NicholasSilveira\\Documents\\GitHub\\art_pipeline\\dcc\\packages\\oop_dcc\\tools\\developer\\ui\\batch_tool.ui'
ui_object, base_class = oop_python.get_ui_class( UI_FILE_PATH )

class ui_test( base_class, ui_object ):
   def __init__( self, parent = oop_maya.get_maya_window(), *args ):
      super( ui_test, self ).__init__( parent )
      
      self.setupUi( self )
      self.show()

ui_test()
