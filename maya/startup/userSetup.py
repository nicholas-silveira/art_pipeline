"""
userSetup runs at startup

*Author:*
	* Nicholas Silveira, Nicholas.Silveira@gmail.com, Jul 21, 2013 4:46:06 PM
"""

import os
import sys

import maya.cmds as cmds # @UnresolvedImport
import maya.mel as mel # @UnresolvedImport



PIPELINE_INSTALL_WINDOW = 'pipeline_install_window'
PIPELINE_PATH = 'pipeline_path.txt'


'''
========================================================================
---->  Pipeline Setup  <----
========================================================================
'''
class Pipeline_Setup():
	'''
	========================================================================
	---->  If pipeline doesn't extist run Install_Pipeline()  <----
	========================================================================
	'''
	def __init__( self ):
		maya_script_path = cmds.internalVar( userPrefDir = True )
		pipeline_path_file = '{0}{1}'.format( maya_script_path, PIPELINE_PATH )

		if os.path.exists( pipeline_path_file ):
			pipeline_path_file = open( pipeline_path_file, 'r' )
			pipeline_dir = pipeline_path_file.readline()

			self.add_pipeline_paths( pipeline_dir )
			self.run_tools_setup()

		else:
			Install_Pipeline()

	'''
	========================================================================
	---->  Adds all Maya environment paths  <----
	========================================================================
	'''
	def add_pipeline_paths( self, pipeline_dir ):
		maya_dir = '{0}/maya'.format( pipeline_dir )

		if os.path.exists( pipeline_dir ):
				if not pipeline_dir in sys.path:
					sys.path.append( sys.path.append( pipeline_dir ) )

		if os.path.exists( maya_dir ):
				if not maya_dir in sys.path:
					sys.path.append( sys.path.append( maya_dir ) )

		import startup.maya_env

		maya_version = mel.eval( 'getApplicationVersionAsFloat;' )
		maya_paths = startup.maya_env.get_paths( maya_version )

		for path in maya_paths:
			if os.path.exists( path ):
				if not path in sys.path:
					sys.path.append( path )

	'''
	========================================================================
	---->  Run Tools Setup  <----
	========================================================================
	'''
	def run_tools_setup( self ):
		import startup.maya_setup as maya_setup
		maya_setup.Setup()

'''
========================================================================
---->  Install Pipeline  <----
========================================================================
'''
class Install_Pipeline():
	'''
	========================================================================
	---->  Shows FKIK Snap Build UI  <----
	========================================================================
	'''
	def __init__( self ):
		self.pipeline_dir = None

		if cmds.window( PIPELINE_INSTALL_WINDOW, exists = True ):
			cmds.deleteUI( PIPELINE_INSTALL_WINDOW )

		window = cmds.window( PIPELINE_INSTALL_WINDOW, title = "Install Pipeline", w = 300, h = 110, titleBarMenu = False, sizeable = False )

		cmds.columnLayout( w = 300, h = 110 )
		form = cmds.formLayout( w = 300, h = 110 )


		text = cmds.text( label = "ERROR: Could not find pipeline directory. \nPlease locate using the \'Browse\' button!", w = 300 )

		browseButton = cmds.button( label = "Browse", w = 140, h = 50, c = self.install_browse )
		cancelButton = cmds.button( label = "Cancel", w = 140, h = 50, c = self.install_cancel )

		cmds.formLayout( form, edit = True, af = [( text, 'left', 10 ), ( text, 'top', 10 )] )
		cmds.formLayout( form, edit = True, af = [( browseButton, 'right', 5 ), ( browseButton, 'top', 50 )] )
		cmds.formLayout( form, edit = True, af = [( cancelButton, 'left', 5 ), ( cancelButton, 'top', 50 )] )

		cmds.showWindow( window )
		cmds.window( window, edit = True, w = 300, h = 110 )

	'''
	========================================================================
	---->  Install Browse  <----
	========================================================================
	'''
	def install_browse( self, *args ):
		pipeline_dir = cmds.fileDialog2( dialogStyle = 2, fileMode = 3 )[0]

		cmds.deleteUI( PIPELINE_INSTALL_WINDOW )

		maya_script_path = cmds.internalVar( upd = True )
		pipeline_path_file = '{0}{1}'.format( maya_script_path, PIPELINE_PATH )

		pipeline_path_file = open( pipeline_path_file, 'w' )
		pipeline_path_file.write( pipeline_dir )
		pipeline_path_file.close()

		Pipeline_Setup().add_pipeline_paths( pipeline_dir )
		Pipeline_Setup().run_tools_setup()

	'''
	========================================================================
	---->  Install Cancel  <----
	========================================================================
	'''
	def install_cancel( self, *args ):
		cmds.deleteUI( PIPELINE_INSTALL_WINDOW )


Pipeline_Setup()
