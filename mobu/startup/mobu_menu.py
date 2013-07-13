'''IMPORTED MODULES'''
import pyfbsdk



'''
========================================================================
---->  UI MAIN CLASS  <----
========================================================================
'''
class Mobu_Menu():
	def __init__(self, control, event):
		self.menuMgr = pyfbsdk.FBMenuManager()
		self.tools_menu()
		self.debug_menu()

		

	'''Procedure creates top menu in Maya'''
	def tools_menu(self):
		if self.menuMgr.GetMenu("Studio Tools") == None:
			self.menuMgr.InsertBefore(None, "Help", "Studio Tools")	
			
			
			
	def debug_menu(self):
		if self.menuMgr.GetMenu("Studio Debug") == None:
			self.menuMgr.InsertBefore(None, "Help", "Studio Debug")	
	


		
		