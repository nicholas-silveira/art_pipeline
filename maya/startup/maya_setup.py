import maya.mel as mel
import maya.cmds as cmds

import maya_env
import maya_menu

class Setup():
	def __init__( self ):
		maya_version = str( 'maya_{0}'.format( mel.eval( 'getApplicationVersionAsFloat' ) ) )
		maya_env.Env_Paths().add_paths( maya_version )

		cmds.scriptJob( event = ['NewSceneOpened', maya_menu.Maya_Menu] )

