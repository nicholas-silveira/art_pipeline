import maya.OpenMayaUI # @UnresolvedImport



def get_maya_window():
   maya_window = maya.OpenMayaUI.apiUI.MQtUtil.mainWindow()
   
   return maya_window
