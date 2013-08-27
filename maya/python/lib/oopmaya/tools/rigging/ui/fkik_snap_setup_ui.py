"""
*Author:*
	* Nicholas Silveira, Nicholas.Silveira@gmail.com, Jul 21, 2013 4:42:15 PM
"""

import functools

import maya.cmds as cmds #@UnresolvedImport

VERSION = 1.0
WINDOW_NAME = 'fkik_snap_build_window'


class FKIK_Snap_Setup():
	'''
	========================================================================
	---->  Shows FKIK Snap Build UI  <----
	========================================================================
	'''
	def show( self ):
		"""
		*Examples:* ::
			import fkik_snap_build
			
			# Show UI
			fkik_snap_build.FKIK_Snap_Build().show_ui()
		"""
		if cmds.window( WINDOW_NAME, exists = True, q = True ):
			cmds.deleteUI( WINDOW_NAME )

		self.fkik_snap_build_ui()

	'''
	========================================================================
	---->  FKIK Snap Build UI  <----
	========================================================================
	'''
	def fkik_snap_build_ui( self ):

		cmds.window( WINDOW_NAME, title = 'FKIK Snap Build {0}'.format( VERSION ), w = 500, h = 300 )

		cmds.rowColumnLayout( 'main_column', numberOfRows = 1 )
		cmds.rowColumnLayout( 'set_column', numberOfRows = 3 )

		self.set_scroll = cmds.textScrollList( self.set_scroll_str, w = 150, h = 300, dcc = self.test, selectCommand = self.test )
		cmds.button( label = 'Add Set', c = self.test )
		cmds.button( label = 'Remove Set', c = self.test )
		cmds.setParent( '..' )

		form = cmds.formLayout()
		tabs = cmds.tabLayout( w = 500, h = 300 )
		cmds.formLayout( form, edit = True, attachForm = ( ( tabs, 'top', 0 ), ( tabs, 'left', 0 ), ( tabs, 'bottom', 0 ), ( tabs, 'right', 0 ) ) )

		set_objects_column = cmds.rowColumnLayout()
		cmds.rowColumnLayout( numberOfColumns = 4, columnWidth = [( 1, 25 ), ( 2, 200 ), ( 3, 50 ), ( 4, 200 )] )

		self.object_order_scroll = cmds.textScrollList( self.object_number_str, allowMultiSelection = False, h = 300, selectCommand = functools.partial( self.test, self.test ),
																																						dcc = self.test )

		self.object_name_scroll = cmds.textScrollList( self.object_name_str, allowMultiSelection = False, h = 300, selectCommand = functools.partial( self.test, self.test ),
																																					dcc = functools.partial( self.test, self.test ) )

		self.object_connect_scroll = cmds.textScrollList( self.object_connect_str, allowMultiSelection = False, h = 300, selectCommand = functools.partial( self.test, self.test ),
																																							dcc = self.test )

		self.object_snap_scroll = cmds.textScrollList( self.object_snap_str, allowMultiSelection = False, h = 300, selectCommand = functools.partial( self.test, self.test ),
																																					dcc = functools.partial( self.select_obj, self.test ) )
		cmds.setParent( '..' )

		cmds.button( label = 'Add Selected Object', c = self.test )
		cmds.button( label = 'Remove Selected Object', c = self.test )

		cmds.separator( height = 20, style = 'in' )
		cmds.button( label = 'BUILD FKIK SNAP', c = self.test, bgc = [1, 1, 1] )
		cmds.setParent( '..' )

		set_connections_column = cmds.rowColumnLayout( numberOfColumns = 2 )

		self.opposite_set_scroll = cmds.textScrollList( h = 300, w = 225 )
		self.switch_scroll = cmds.textScrollList( h = 300, w = 225 )
		cmds.button( label = 'Pick Opposite Set', c = self.test )
		cmds.button( label = 'Add Selected FKIK Switch Attribute', c = self.test )
		cmds.setParent( '..' )

		self.connected_set_scroll = cmds.tabLayout( tabs, edit = True, tabLabel = ( ( set_objects_column, 'Set Objects' ), ( set_connections_column, 'Opposite Set' ) ) )

		self.load_ui()

		cmds.showWindow()

	def test( self ):
		pass
