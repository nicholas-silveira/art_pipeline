import sys

import maya.cmds as cmds #@UnresolvedImport
import maya.OpenMaya as OpenMaya #@UnresolvedImport

VERSION = 1.0



'''
========================================================================
---->  Creates and removes callbacks  <----
========================================================================
'''
class Callbacks():
	"""
	----> Examples <----
	
		import maya.cmds as cmds
		
		import callback_util
		
		# Example proc
		def print_all_nodes(*args):
		    print cmds.ls('*')
		    print len(cmds.ls('*'))
		
		# Create callback instance
		callback_obj = callback_util.Callback((print_all_nodes))
		
		# Run proc before scene updates
		callback_obj.scene_update_before()
		
		# Run proc after scene updates
		callback_obj.scene_update_after()
		
		# Adds more maya node
		for i in range(20):
    		cmds.spaceLocator()
    		
    	# Open new Maya scene
    	cmds.file (f=True, new=True)
		
		# Removes callback from instance
		callback_obj.remove()

	*Author:*
		* nick.silveira, Nicholas.Silveira@gmail.com, Jun 15, 2013 7:39:20 PM
	"""
	def __init__( self, procedure, window = None ):
		self.procedure = procedure
		self.window = window
		self.callback_list = []

	'''
	========================================================================
	---->  Callback runs passed procedure when scene updates  <----
	========================================================================
	'''
	def scene_update_before( self ):
		"""
		----> Examples <----
		
		import maya.cmds as cmds
		import callback_util
		
		def create_locator( *args ):
			cmds.spaceLocator()
		
		callback_obj = callback_util.Callback( ( create_locator ) )
		callback_obj.scene_update_before()
		"""
		self.callback_list.append( OpenMaya.MSceneMessage.addCallback( OpenMaya.MSceneMessage.kBeforeNew, self.run_callback ) )
		self.callback_list.append( OpenMaya.MSceneMessage.addCallback( OpenMaya.MSceneMessage.kBeforeImport, self.run_callback ) )
		self.callback_list.append( OpenMaya.MSceneMessage.addCallback( OpenMaya.MSceneMessage.kBeforeOpen, self.run_callback ) )
		self.callback_list.append( OpenMaya.MSceneMessage.addCallback( OpenMaya.MSceneMessage.kBeforeReference, self.run_callback ) )
		self.callback_list.append( OpenMaya.MSceneMessage.addCallback( OpenMaya.MSceneMessage.kBeforeRemoveReference, self.run_callback ) )

	'''
	========================================================================
	---->  Callback runs passed procedure when scene updates  <----
	========================================================================
	'''
	def scene_update_after( self ):
		"""
		----> Examples <----
		
		import maya.cmds as cmds
		import callback_util
		
		def create_locator( *args ):
			cmds.spaceLocator()
		
		callback_obj = callback_util.Callback( ( create_locator ) )
		callback_obj.scene_update_after()
		"""
		self.callback_list.append( OpenMaya.MSceneMessage.addCallback( OpenMaya.MSceneMessage.kAfterNew, self.run_callback ) )
		self.callback_list.append( OpenMaya.MSceneMessage.addCallback( OpenMaya.MSceneMessage.kAfterImport, self.run_callback ) )
		self.callback_list.append( OpenMaya.MSceneMessage.addCallback( OpenMaya.MSceneMessage.kAfterOpen, self.run_callback ) )
		self.callback_list.append( OpenMaya.MSceneMessage.addCallback( OpenMaya.MSceneMessage.kAfterReference, self.run_callback ) )
		self.callback_list.append( OpenMaya.MSceneMessage.addCallback( OpenMaya.MSceneMessage.kAfterRemoveReference, self.run_callback ) )

	'''
	========================================================================
	---->  Runs passed proc and removes ui callbacks if ui dosn't exist  <----
	========================================================================
	'''
	def run_callback( self, *args ):
		if self.window:
			run_proc = self.window_remove()

		else:
			run_proc = True

		if run_proc:
			self.procedure()

	'''
	========================================================================
	---->  Callback runs passed procedure when scene updates  <----
	========================================================================
	'''
	def window_remove( self, *args ):
		if not cmds.window( self.window, exists = True, q = True ) and not cmds.dockControl( self.window, vis = True, q = True ):

			for callback in self.callback_list:
				OpenMaya.MMessage.removeCallback( callback )

			sys.stdout.write( '// Removed {0} callbacks!'.format( self.window ) )

			return False

		return True

	'''
	========================================================================
	---->  Removes all callbacks in instance  <----
	========================================================================
	'''
	def remove( self ):
		for callback in self.callback_list:
				OpenMaya.MMessage.removeCallback( callback )
	'''
	========================================================================
	---->  Code Sample  <----
	========================================================================
	'''
	def code_sample( self, *args ):
		code = '''
		import maya.cmds as cmds
		
		import callback_util
		
		# Example proc
		def print_all_nodes(*args):
		    print cmds.ls('*')
		    print len(cmds.ls('*'))
		
		# Create callback instance
		callback_obj = callback_util.Callback((print_all_nodes))
		
		# Run proc before scene updates
		callback_obj.scene_update_before()
		
		# Run proc after scene updates
		callback_obj.scene_update_after()
		
		# Adds more maya node
		for i in range(20):
			cmds.spaceLocator()
				
		# Open new Maya scene
		cmds.file (f=True, new=True)
		
		# Removes callback from instance
		callback_obj.remove()
		'''

		if cmds.window( 'code_sample_window', exists = True, q = True ):
			cmds.deleteUI( 'code_sample_window' )

		cmds.window( 'code_sample_window', title = 'Code Sample' )
		cmds.paneLayout()
		cmds.scrollField( editable = False, text = code.replace( '		', '' ) )
		cmds.showWindow()





