import os

import pyfbsdk #@UnresolvedImport

import mobu_env
import mobu_menu



class Setup():
	def __init__( self ):
		mobu_name = 'mobu'
	
		script_path = os.path.dirname( os.path.abspath( __file__ ) )
		print os.path.dirname( os.path.dirname( script_path ) )
	
		mobu_version = str( 2000 + int( str( pyfbsdk.FBSystem().Version )[:2] ) )
		mobu_env.Env_Paths().load_paths( '{0}_{1}'.format( mobu_name, mobu_version ) )
		
		pyfbsdk.FBSystem().Scene.OnChange.Add( mobu_menu.Mobu_Menu )
		pyfbsdk.FBApplication().OnFileExit.Add( self.remove_all_callbacks )
		
	def remove_all_callbacks( self, control, event ):
		pyfbsdk.FBSystem().Scene.OnChange.RemoveAll()
