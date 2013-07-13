'''IMPORTED MODULES'''
import maya.cmds as cmds
import maya.mel as mel

import maya_env



'''
========================================================================
---->  UI MAIN CLASS  <----
========================================================================
'''
class Maya_Menu():
	def __init__(self):
		self.tools_menu()
		self.debug_menu()
		

	'''Procedure creates top menu in Maya'''
	def tools_menu(self):
		
		
		gMainWindow = mel.eval( '$tmpVar = $gMainWindow' )
		
		if cmds.menu ('studioTools', exists=True):
			cmds.deleteUI ('studioTools', menu=True)
		
		studio_tools_menu = cmds.menu('studioTools', parent= gMainWindow, label= "Studio Tools", to=True)
		
		cmds.menuItem(parent= studio_tools_menu, label= "Animation Tools", subMenu= True, to=True)
		cmds.menuItem(parent= studio_tools_menu, label= "Rig Tools", subMenu= True, to=True)
		cmds.menuItem(parent= studio_tools_menu, label= "UV Tools", subMenu= True, to=True)
		cmds.menuItem(parent= studio_tools_menu, label= "P4", subMenu= True, to=True)
		cmds.menuItem(parent= studio_tools_menu, label= "Maya Preferences", subMenu= True, to=True)

		#uvTools = cmds.menuItem(parent= customMenu, label= "UV Tools", subMenu= True, to=True)
		#cmds.menuItem (parent= uvTools, label= 'SG UV Tool', c= self.sgUVTool)
		#cmds.menuItem (parent= uvTools, label= 'Zebruv', c= self.zebruv)

		#fbxExport = cmds.menuItem(parent= customMenu, label= "FBX Exporter", c= self.exportTool)
		#fbxBatchExport = cmds.menuItem(parent= customMenu, label= "FBX Batch Exporter", c= self.batchTool)
	
			
			
	def debug_menu(self):
		gMainWindow = mel.eval( '$tmpVar = $gMainWindow' )
		
		if cmds.menu ('studioDebug', exists=True):
			cmds.deleteUI ('studioDebug', menu=True)

		debug_menu = cmds.menu('studioDebug', parent= gMainWindow, label= "Studio Debug", to=True)
		cmds.menuItem(parent= debug_menu, label= "Maya Environment")
		cmds.menuItem(parent= debug_menu, label= "Documents")
	


		
		