'''IMPORTED MODULES'''
import pyfbsdk #@UnresolvedImport

import core.pipeline_core #@UnresolvedImport



'''
========================================================================
---->  UI MAIN CLASS  <----
========================================================================
'''
class Mobu_Menu():
	def __init__( self, control, event ):
		self.pipeline_name = core.pipeline_core.pipeline_name
		
		self.menuMgr = pyfbsdk.FBMenuManager()
		self.tools_menu()
		self.debug_menu()

		

	'''Procedure creates top menu in Maya'''
	def tools_menu( self ):
		tools_menu_name = '{0} Tools'.format( self.pipeline_name )
		
		if self.menuMgr.GetMenu( tools_menu_name ) == None:
			self.menuMgr.InsertBefore( None, 'Help', tools_menu_name )	
			
			
			
	def debug_menu( self ):
		developer_menu_name = '{0} Developer'.format( self.pipeline_name )
		
		if self.menuMgr.GetMenu( developer_menu_name ) == None:
			self.menuMgr.InsertBefore( None, 'Help', developer_menu_name )	
	


		
		
