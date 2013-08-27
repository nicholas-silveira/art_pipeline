import maya.cmds as cmds # @UnresolvedImport

import oopdcc.core # @UnresolvedImport


WINDOW_NAME = 'environment_window'
VERSION = 1.0
WINDOW_TITLE = 'Environment Tool {0}'.format( VERSION )

WINDOW_WIDTH = 500
WINDOW_HEIGHT = 300

class Environment_UI():
	def __init__( self ):
		if cmds.window( WINDOW_NAME, exists = True, q = True ):
			cmds.deleteUI( WINDOW_NAME )

		self.layout()

	def layout( self ):
		window = cmds.window( WINDOW_NAME, title = WINDOW_TITLE )
		row = cmds.columnLayout( adjustableColumn = True, parent = window )
		self.environment_scroll = cmds.textScrollList( parent = row )

		cmds.textFieldButtonGrp( buttonLabel = 'Add Path', cw = [1, WINDOW_WIDTH] )
		cmds.button( label = 'Remove Selected' )
		cmds.setParent( '..' )

		cmds.showWindow()

		self.load_ui()

	def load_ui( self ):
		cmds.textScrollList( self.environment_scroll, append = oopdcc.core.get_environment(), e = True )
