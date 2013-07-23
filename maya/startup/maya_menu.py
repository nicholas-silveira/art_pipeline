"""
Mayas Pipeline Menu

*Author:*
	* Nicholas Silveira, Nicholas.Silveira@gmail.com, Jul 21, 2013 4:55:14 PM
"""

'''IMPORTED MODULES'''
import maya.cmds as cmds #@UnresolvedImport
import maya.mel as mel #@UnresolvedImport

import pipeline.config #@UnresolvedImport

import maya_env

import animation.fkik_snap_tool #@UnresolvedImport
import animation.zero_out_tool #@UnresolvedImport

import rigging.fkik_snap_setup #@UnresolvedImport
import rigging.no_flip_pole_vector_tool #@UnresolvedImport



'''
========================================================================
---->  UI MAIN CLASS  <----
========================================================================
'''
class Maya_Menu():
	def __init__( self ):
		self.add_maya_script_paths()
		self.pipeline_name = pipeline.config.pipeline_name

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
		cmds.menuItem( parent = animation_menu, label = "FKIK Snap Tool", to = True, c = animation.fkik_snap_tool.FKIK_Snap_Tool )
		cmds.menuItem( parent = animation_menu, label = "Zero Out Tool", to = True, c = animation.zero_out_tool.Zero_Out_Tool )

		rig_menu = cmds.menuItem( parent = studio_tools_menu, label = "Rig Tools", subMenu = True, to = True )
		cmds.menuItem( parent = rig_menu, label = "FKIK Snap Setup", to = True, c = self.fkik_snap_setup )
		cmds.menuItem( parent = rig_menu, label = "No Flip Pole Vector Setup", to = True, c = self.no_flip_pole_vector_setup )

	'''
	========================================================================
	---->  FKIK Snap Setup  <----
	========================================================================
	'''
	def fkik_snap_setup( self, *args ):
		rigging.fkik_snap_setup.FKIK_Snap_Setup().show_ui()

	'''
	========================================================================
	---->  No Flip Pole Vector Setup  <----
	========================================================================
	'''
	def no_flip_pole_vector_setup( self, *args ):
		rigging.no_flip_pole_vector_tool.No_Flip_Pole_Vector().show_ui()

	'''
	========================================================================
	---->  Add Maya Script Paths  <----
	========================================================================
	'''
	def add_maya_script_paths( self ):
		maya_version = str( 'maya_{0}'.format( mel.eval( 'getApplicationVersionAsFloat' ) ) )
		maya_paths = maya_env.Env_Paths().get_paths( maya_version )

		get_script_env_string = mel.eval( 'getenv "MAYA_SCRIPT_PATH";' )
		get_script_env = get_script_env_string.split( ';' )

		for path in maya_paths:
			path = path.replace( '\\', '/' )

			if path not in get_script_env:
				get_script_env.append( path )

		get_script_env = ';'.join( get_script_env )
		mel.eval( 'putenv "MAYA_SCRIPT_PATH" "{0}";'.format( get_script_env ) )
