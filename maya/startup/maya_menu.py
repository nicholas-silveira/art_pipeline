'''IMPORTED MODULES'''
import maya.cmds as cmds #@UnresolvedImport
import maya.mel as mel #@UnresolvedImport

import core.pipeline_core #@UnresolvedImport


'''
========================================================================
---->  UI MAIN CLASS  <----
========================================================================
'''
class Maya_Menu():
	def __init__( self ):
		self.studio_name = core.pipeline_core.studio_name
		
		self.tools_menu()
		self.developer_menu()
		
	'''Procedure creates top menu in Maya'''
	def tools_menu( self ):
		tools_menu = 'studioTools'
		tools_menu_name = '{0} Tools'.format( self.studio_name )
		
		gMainWindow = mel.eval( '$tmpVar = $gMainWindow' )
		
		if cmds.menu ( tools_menu, exists = True ):
			cmds.deleteUI ( tools_menu, menu = True )
		
		studio_tools_menu = cmds.menu( tools_menu, parent = gMainWindow, label = tools_menu_name, to = True )
		
		cmds.menuItem( parent = studio_tools_menu, label = "Animation Tools", subMenu = True, to = True )
		cmds.menuItem( parent = studio_tools_menu, label = "Rig Tools", subMenu = True, to = True )
		cmds.menuItem( parent = studio_tools_menu, label = "UV Tools", subMenu = True, to = True )
		cmds.menuItem( parent = studio_tools_menu, label = "P4", subMenu = True, to = True )
		cmds.menuItem( parent = studio_tools_menu, label = "Maya Preferences", subMenu = True, to = True )

		#uvTools = cmds.menuItem(parent= customMenu, label= "UV Tools", subMenu= True, to=True)
		#cmds.menuItem (parent= uvTools, label= 'SG UV Tool', c= self.sgUVTool)
		#cmds.menuItem (parent= uvTools, label= 'Zebruv', c= self.zebruv)

		#fbxExport = cmds.menuItem(parent= customMenu, label= "FBX Exporter", c= self.exportTool)
		#fbxBatchExport = cmds.menuItem(parent= customMenu, label= "FBX Batch Exporter", c= self.batchTool)
	
			
			
	def developer_menu( self ):
		developer_menu = 'studioDeveloper'
		developer_menu_name = '{0} Developer'.format( self.studio_name )
	
		gMainWindow = mel.eval( '$tmpVar = $gMainWindow' )
		
		if cmds.menu ( developer_menu, exists = True ):
			cmds.deleteUI ( developer_menu, menu = True )

		debug_menu = cmds.menu( developer_menu, parent = gMainWindow, label = developer_menu_name, to = True )
		cmds.menuItem( parent = debug_menu, label = "Maya Environment" )
		cmds.menuItem( parent = debug_menu, label = "Documents" )
	


		
		
