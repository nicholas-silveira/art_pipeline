"""
Mayas Pipeline Menu

*Author:*
	* Nicholas Silveira, Nicholas.Silveira@gmail.com, Jul 21, 2013 4:55:14 PM
"""

'''IMPORTED MODULES'''
import maya.cmds as cmds #@UnresolvedImport
import maya.mel as mel #@UnresolvedImport

import core.config #@UnresolvedImport



'''
========================================================================
---->  UI MAIN CLASS  <----
========================================================================
'''
class Maya_Menu():
	def __init__( self ):
		self.pipeline_name = core.config.pipeline_name

		self.tools_menu()

	'''
	========================================================================
	---->  Tools Menu  <----
	========================================================================
	'''
	def tools_menu( self ):
		tools_menu = 'studioTools'
		tools_menu_name = '{0} Tools'.format( self.pipeline_name )

		gMainWindow = mel.eval( '$tmpVar = $gMainWindow' )

		if cmds.menu ( tools_menu, exists = True ):
			cmds.deleteUI ( tools_menu, menu = True )

		studio_tools_menu = cmds.menu( tools_menu, parent = gMainWindow, label = tools_menu_name, to = True )

		animation_menu = cmds.menuItem( parent = studio_tools_menu, label = "Animation Tools", subMenu = True, to = True )
		cmds.menuItem( parent = animation_menu, label = "FKIK Snap Tool", to = True, c = self.test )
		cmds.menuItem( parent = animation_menu, label = "Zero Out Tool", to = True )

		rig_menu = cmds.menuItem( parent = studio_tools_menu, label = "Rig Tools", subMenu = True, to = True )
		cmds.menuItem( parent = rig_menu, label = "FKIK Snap Setup", to = True )
		cmds.menuItem( parent = rig_menu, label = "No Flip Pole Vector Setup", to = True )

		developer_menu = 'developerTools'
		developer_menu_name = '{0} Developer'.format( self.pipeline_name )

		if cmds.menu ( developer_menu, exists = True ):
			cmds.deleteUI ( developer_menu, menu = True )

		studio_developer_menu = cmds.menu( developer_menu, parent = gMainWindow, label = developer_menu_name, to = True )
		cmds.menuItem( parent = studio_developer_menu, label = "Environment Tool", to = True, c = self.environment_tool )

	def test( self, *args ):
		pass

	def environment_tool( self, *args ):
		import oop_dcc.tools.developer.environment_tool as environment_tool
		reload( environment_tool )
		
		environment_tool.show()
