"""
Sets up Maya Tools
*Author:*
	* Nicholas Silveira, Nicholas.Silveira@gmail.com, Jul 21, 2013 4:52:44 PM
"""

import os

import maya.cmds as cmds #@UnresolvedImport
import maya.mel as mel #@UnresolvedImport

import maya_env
import maya_menu

'''
========================================================================
---->  Setup  <----
========================================================================
'''
class Setup():
	'''
	========================================================================
	---->  Runs Script Node On NewSceneOpened <----
	========================================================================
	'''
	def __init__( self ):
		self.add_maya_paths()
		cmds.scriptJob( event = ['NewSceneOpened', self.custom_maya] )

	'''
	========================================================================
	---->  Add Maya Script Paths  <----
	========================================================================
	'''
	def add_maya_paths( self ):
		maya_version = str( 'maya_{0}'.format( mel.eval( 'getApplicationVersionAsFloat' ) ) )
		maya_paths = maya_env.Env_Paths().get_paths( maya_version, print_paths = False )

		get_script_env_string = mel.eval( 'getenv "MAYA_SCRIPT_PATH";' )
		get_script_env = get_script_env_string.split( ';' )

		for path in maya_paths:
			path = path.replace( '\\', '/' )

			if path not in get_script_env:
				get_script_env.append( path )

		get_script_env = ';'.join( get_script_env )
		mel.eval( 'putenv "MAYA_SCRIPT_PATH" "{0}";'.format( get_script_env ) )

	'''
	========================================================================
	---->  Builds Custom Maya Tools <----
	========================================================================
	'''
	def custom_maya( self ):
		maya_menu.Maya_Menu()

		maya_version = str( 'maya_{0}'.format( mel.eval( 'getApplicationVersionAsFloat' ) ) )
		maya_paths = maya_env.Env_Paths().get_paths( maya_version )

		for path in maya_paths:
			if 'shelves' in path:
				os.chdir( path )

				for item in os.listdir( "." ):
					if item.endswith( ".mel" ):
						try:
							path = path.replace( '\\', '/' )
							mel.eval( 'loadNewShelf "{0}/{1}";'.format( path, item ) )

						except:
							pass
