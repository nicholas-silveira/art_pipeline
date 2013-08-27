import sys

import maya.cmds as cmds #@UnresolvedImport
import maya.OpenMaya as OpenMaya #@UnresolvedImport

VERSION = 1.0



'''
========================================================================
---->  Creates and removes callbacks  <----
========================================================================
'''
class Maya_Callback():
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
		# Get callback procedure
		self.procedure = procedure

		# Get callbacks main window
		self.window = window

		# Initiate callback list
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
	---->  Changed Attribute Callback  <----
	========================================================================
	'''
	def add_attr( self, obj_name, attr_name ):
		"""
		*Arguments:*
			* ``obj_name`` Pass object name
			* ``attr_name`` Pass attribute name

		*Examples:* ::
			# Import Python modules
			import sys

			# Import Maya modules
			import maya.cmds as cmds
			
			# Import Callback module
			import maya_callback
			reload(maya_callback)
			
			# Global Variables
			locator_name = 'callback_loc'
			attr_name = 'translate'
			
			# Print out 'Attribute Callback Works!'
			def print_something( *args ):
				sys.stdout.write( '// Result: Attribute Callback Works!' )
			
			# Create space locator
			locator = cmds.spaceLocator( n = locator_name )[0]
			
			# Create callback & add proc
			callback = maya_callback.Maya_Callback( ( print_something ) )
			
			# Add attribute callback
			callback.add_attr( locator, attr_name )
			
			# Remove callback
			callback.remove()
		"""
		self.obj_name = obj_name
		self.attr_name = attr_name

		sel = cmds.ls( sl = True )
		cmds.select( obj_name )

		node = self.get_mobject( obj_name )
		MSelectionList = OpenMaya.MSelectionList()
		OpenMaya.MGlobal.getActiveSelectionList( MSelectionList )
		MSelectionList.getDependNode( 0, node )

		self.callback_list.append( OpenMaya.MNodeMessage.addAttributeChangedCallback( node, self.run_add_attr, None ) )

		cmds.select( sel )

	'''
	========================================================================
	---->  Run Changed Attribute Callback  <----
	========================================================================
	'''
	def run_add_attr( self, message, m_obj, *args ):
		"""
		*Arguments:*
			* ``message`` Callback passes a message ID
			* ``m_obj`` Callback passes MObject
		"""
		node_name, attr_name = m_obj.name().split( '.' )

		if message == 2056:
			if node_name == self.obj_name:
				if attr_name == self.attr_name:
					self.run_callback()

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

	def get_mobject( self, name ):
		selectionList = OpenMaya.MSelectionList()
		selectionList.add( name )
		node = OpenMaya.MObject()
		selectionList.getDependNode( 0, node )
		return node

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





