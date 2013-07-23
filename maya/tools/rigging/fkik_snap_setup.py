"""
*Author:*
	* Nicholas Silveira, Nicholas.Silveira@gmail.com, Jul 21, 2013 4:42:15 PM
"""

import functools

import maya.mel as mel #@UnresolvedImport
import maya.cmds as cmds #@UnresolvedImport
import maya.OpenMaya as OpenMaya #@UnresolvedImport

VERSION = 1.0
WINDOW_NAME = 'fkik_snap_build_window'


class FKIK_Snap_Setup():
	'''
	========================================================================
	---->  Shows FKIK Snap Build UI  <----
	========================================================================
	'''
	def show_ui( self ):
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

		self.get_globals()

		cmds.window( WINDOW_NAME, title = 'FKIK Snap Build {0}'.format( VERSION ), w = 500, h = 300 )

		cmds.rowColumnLayout( 'main_column', numberOfRows = 1 )
		cmds.rowColumnLayout( 'set_column', numberOfRows = 3 )

		self.set_scroll = cmds.textScrollList( self.set_scroll_str, w = 150, h = 300, dcc = self.rename_set, selectCommand = self.load_set_data )
		cmds.button( label = 'Add Set', c = self.add_set )
		cmds.button( label = 'Remove Set', c = self.remove_set )
		cmds.setParent( '..' )

		form = cmds.formLayout()
		tabs = cmds.tabLayout( w = 500, h = 300 )
		cmds.formLayout( form, edit = True, attachForm = ( ( tabs, 'top', 0 ), ( tabs, 'left', 0 ), ( tabs, 'bottom', 0 ), ( tabs, 'right', 0 ) ) )

		set_objects_column = cmds.rowColumnLayout()
		cmds.rowColumnLayout( numberOfColumns = 4, columnWidth = [( 1, 25 ), ( 2, 200 ), ( 3, 50 ), ( 4, 200 )] )

		self.object_order_scroll = cmds.textScrollList( self.object_number_str, allowMultiSelection = False, h = 300, selectCommand = functools.partial( self.obj_list_select, self.object_number_str ),
																																						dcc = self.change_obj_number )

		self.object_name_scroll = cmds.textScrollList( self.object_name_str, allowMultiSelection = False, h = 300, selectCommand = functools.partial( self.obj_list_select, self.object_name_str ),
																																					dcc = functools.partial( self.select_obj, self.object_name_str ) )

		self.object_connect_scroll = cmds.textScrollList( self.object_connect_str, allowMultiSelection = False, h = 300, selectCommand = functools.partial( self.obj_list_select, self.object_connect_str ),
																																							dcc = self.add_snap_obj )

		self.object_snap_scroll = cmds.textScrollList( self.object_snap_str, allowMultiSelection = False, h = 300, selectCommand = functools.partial( self.obj_list_select, self.object_snap_str ),
																																					dcc = functools.partial( self.select_obj, self.object_snap_str ) )
		cmds.setParent( '..' )

		cmds.button( label = 'Add Selected Object', c = self.add_obj )
		cmds.button( label = 'Remove Selected Object', c = self.remove_obj )

		cmds.separator( height = 20, style = 'in' )
		cmds.button( label = 'BUILD FKIK SNAP', c = self.build, bgc = [1, 1, 1] )
		cmds.setParent( '..' )

		set_connections_column = cmds.rowColumnLayout( numberOfColumns = 2 )

		self.opposite_set_scroll = cmds.textScrollList( h = 300, w = 225 )
		self.switch_scroll = cmds.textScrollList( h = 300, w = 225 )
		cmds.button( label = 'Pick Opposite Set', c = self.sets_list_ui )
		cmds.button( label = 'Add Selected FKIK Switch Attribute', c = self.add_switch )
		cmds.setParent( '..' )

		self.connected_set_scroll = cmds.tabLayout( tabs, edit = True, tabLabel = ( ( set_objects_column, 'Set Objects' ), ( set_connections_column, 'Opposite Set' ) ) )

		self.load_ui()

		cmds.showWindow()

	'''
	========================================================================
	---->  Sets List UI  <----
	========================================================================
	'''
	def sets_list_ui( self, *args ):
		if cmds.window( self.sets_list_window, exists = True, q = True ):
			cmds.deleteUI( self.sets_list_window )

		cmds.window( self.sets_list_window, title = 'Sets List Window', w = 200, h = 400 )

		cmds.rowColumnLayout( numberOfColumns = 1 )
		self.sets_list = cmds.textScrollList( self.sets_list_str, w = 150, h = 300, dcc = self.rename_set, selectCommand = self.load_set_data )

		cmds.button( label = 'Connect Set', c = self.get_opposite_set )

		self.load_sets( self.sets_list )

		cmds.showWindow()

	'''
	========================================================================
	---->  Add Switch  <----
	========================================================================
	'''
	def add_switch( self, *args ):

		controller = cmds.ls( sl = True )
		set_node = cmds.textScrollList( self.set_scroll, si = True, q = True )

		if controller:
			controller = controller[0]

			channel_box = mel.eval( 'global string $gChannelBoxName; $temp=$gChannelBoxName;' )
			switch_attr = cmds.channelBox( channel_box, q = True, sma = True )

			if switch_attr:
				switch_attr = switch_attr[0]

				if set_node:
					set_node = set_node[0]

					controller_switch_attr = '{0}.{1}'.format( controller, switch_attr )

					cmds.connectAttr( controller_switch_attr, '{0}.{1}'.format( set_node, self.switch_parent_str ), force = True )

					cmds.textScrollList( self.switch_scroll, removeAll = True, e = True )
					cmds.textScrollList( self.switch_scroll, append = '{0}.{1}'.format( controller, switch_attr ), e = True )

	'''
	========================================================================
	---->  Get Opposite Set  <----
	========================================================================
	'''
	def get_opposite_set( self, *args ):
		opposite_set = cmds.textScrollList( self.sets_list_str, si = True, q = True )

		if opposite_set:
			self.connect_opposite_set( opposite_set[0] )

			if cmds.window( self.sets_list_window, exists = True, q = True ):
				cmds.deleteUI( self.sets_list_window )

	'''
	========================================================================
	---->  Connect Opposite Set  <----
	========================================================================
	'''
	def connect_opposite_set( self, opposite_set ):
		set_node = cmds.textScrollList( self.set_scroll, si = True, q = True )

		if set_node:
			set_node = set_node[0]

			if not opposite_set == set_node:
				opposite_set_attr = '{0}.{1}'.format( opposite_set, self.set_child_str )

				if not cmds.objExists( opposite_set_attr ):
					opposite_set_attr = Maya_Util().add_attr( opposite_set, self.set_child_str, 'message' )

				cmds.connectAttr( opposite_set_attr, '{0}.{1}'.format( set_node, self.opposite_set_str ), force = True )

				cmds.textScrollList( self.opposite_set_scroll, removeAll = True, e = True )
				cmds.textScrollList( self.opposite_set_scroll, append = opposite_set, e = True )

			else:
				OpenMaya.MGlobal.displayError( "You can't select the same set!" )

	'''
	========================================================================
	---->  Get Globals  <----
	========================================================================
	'''
	def get_globals( self ):
		# Load global Values
		self.main_set = 'fkik_snap_set'

		self.set_scroll_str = 'set_list'

		self.object_number_str = 'object_order_list'
		self.object_name_str = 'object_name_list'
		self.object_connect_str = 'object_connect_list'
		self.object_snap_str = 'object_snap_list'

		self.arrow_str = '--->'

		self.snap_order_attr = 'snap_order'

		self.opposite_set_str = 'opposite_set'
		self.set_parent_str = 'set_parent'
		self.set_child_str = 'set_child'

		self.snap_parent_str = 'snap_parent'
		self.snap_child_str = 'snap_child'

		self.sets_list_window = 'sets_list_window'
		self.sets_list_str = 'set_list'

		self.switch_parent_str = 'switch_parent'

	'''
	========================================================================
	---->  Load UI  <----
	========================================================================
	'''
	def load_ui( self ):
		self.load_sets( self.set_scroll )
		self.load_set_data()

	'''
	========================================================================
	---->  Add Set  <----
	========================================================================
	'''
	def add_set( self, *args ):
		selected = cmds.ls( sl = True )

		cmds.select( cl = True )
		if not cmds.objExists( self.main_set ):
			cmds.sets( n = self.main_set )

		set_name = cmds.sets()
		cmds.sets( set_name, add = self.main_set )

		Maya_Util().add_attr( set_name, self.switch_parent_str, attr_type = 'message' )
		Maya_Util().add_attr( set_name, self.opposite_set_str, attr_type = 'message' )
		Maya_Util().add_attr( set_name, self.set_child_str, attr_type = 'message' )

		cmds.textScrollList( self.set_scroll, append = set_name, e = True )
		cmds.textScrollList( self.set_scroll, si = set_name, e = True )

		self.clear_obj_list()

		if selected:
			cmds.select( selected )

	'''
	========================================================================
	---->  Rename Set  <----
	========================================================================
	'''
	def rename_set( self, *args ):
		set_node = cmds.textScrollList( self.set_scroll, si = True, q = True )[0]
		set_name = raw_input()

		if set_name:
			cmds.rename( set_node, set_name )
			cmds.textScrollList( self.set_scroll, removeItem = set_node, e = True )
			cmds.textScrollList( self.set_scroll, append = set_name, e = True )

			cmds.textScrollList( self.set_scroll, selectItem = set_name, e = True )

	'''
	========================================================================
	---->  Remove Set  <----
	========================================================================
	'''
	def remove_set( self, *args ):
		set_node = cmds.textScrollList( self.set_scroll, si = True, q = True )[0]
		cmds.delete( set_node )
		cmds.textScrollList( self.set_scroll, removeItem = set_node, e = True )

		self.load_set_data()

	'''
	========================================================================
	---->  Load Sets  <----
	========================================================================
	'''
	def load_sets( self, scroll_list ):
		if cmds.objExists( self.main_set ):
			set_list = cmds.sets( self.main_set, q = True )

			for set_item in set_list:
				cmds.textScrollList( scroll_list, append = set_item, e = True )

			if set_list:
				cmds.textScrollList( scroll_list, selectItem = set_list[0], e = True )

	'''
	========================================================================
	---->  Load Set Data  <----
	========================================================================
	'''
	def load_set_data( self ):
		self.clear_obj_list()

		set_node = cmds.textScrollList( self.set_scroll, si = True, q = True )

		if set_node:
			set_node = set_node[0]
			set_items = cmds.sets( set_node, q = True )

			if not set_items:
				set_items = []

			for obj in set_items:

				obj_snap_attr = '{0}.{1}'.format( obj, self.snap_parent_str )

				snap_obj = ''

				if cmds.objExists( obj_snap_attr ):
					get_snap_obj = cmds.listConnections( obj_snap_attr )

					if get_snap_obj:
						snap_obj = get_snap_obj[0]


				self.add_obj_list( obj, snap_obj = snap_obj )

			opposite_set = cmds.listConnections( '{0}.{1}'.format( set_node, self.opposite_set_str ) )

			if not opposite_set:
				opposite_set = ''

			cmds.textScrollList( self.opposite_set_scroll, removeAll = True, e = True )
			cmds.textScrollList( self.opposite_set_scroll, append = opposite_set, e = True )

			set_switch_attr = cmds.listConnections( '{0}.{1}'.format( set_node, self.switch_parent_str ), plugs = True )

			if not set_switch_attr:
				set_switch_attr = ''

			cmds.textScrollList( self.switch_scroll, removeAll = True, e = True )
			cmds.textScrollList( self.switch_scroll, append = set_switch_attr, e = True )

	'''
	========================================================================
	---->  Change Obj Number  <----
	========================================================================
	'''
	def change_obj_number( self, *args ):
		obj_index = cmds.textScrollList( self.object_order_scroll, selectIndexedItem = True, q = True )[0]
		obj_name = cmds.textScrollList( self.object_name_scroll, selectItem = True, q = True )[0]
		obj_connection = cmds.textScrollList( self.object_connect_scroll, selectItem = True, q = True )[0]

		obj_num = raw_input()

		if obj_num:
			cmds.setAttr( '{0}.{1}'.format( obj_name, self.snap_order_attr ), obj_num, type = 'string' )
			self.remove_set_connections( obj_index )

			cmds.textScrollList( self.object_order_scroll, append = obj_num, e = True )
			cmds.textScrollList( self.object_name_scroll, append = obj_name, e = True )
			cmds.textScrollList( self.object_connect_scroll, append = obj_connection, e = True )

			self.obj_list_select( index = cmds.textScrollList( self.object_order_scroll, numberOfItems = True, q = True ) )

	'''
	========================================================================
	---->  Remove Set Connections  <----
	========================================================================
	'''
	def remove_set_connections( self, index ):
		cmds.textScrollList( self.object_order_scroll, removeIndexedItem = index, e = True )
		cmds.textScrollList( self.object_name_scroll, removeIndexedItem = index, e = True )
		cmds.textScrollList( self.object_connect_scroll, removeIndexedItem = index, e = True )
		cmds.textScrollList( self.object_snap_scroll, removeIndexedItem = index, e = True )

	'''
	========================================================================
	---->  Add Obj  <----
	========================================================================
	'''
	def add_obj( self, *args ):
		obj_exists = False

		objs = cmds.ls( sl = True )

		if objs:
			obj = objs[0]

			# Add obj to set
			set_node = cmds.textScrollList( self.set_scroll, si = True, q = True )[0]

			set_objs = cmds.sets( set_node, q = True )

			if not set_objs:
				set_objs = []

			for item in set_objs:
				if obj == item or obj == '|{0}'.format( item ):
					obj_exists = True
					break

			if not obj_exists:
				cmds.sets( obj, add = set_node )

				obj_count = cmds.textScrollList( self.object_order_scroll, numberOfItems = True, q = True )

				if not obj_count:
					obj_count = 0

				snap_order_attr = Maya_Util().add_attr( obj, self.snap_order_attr, attr_type = 'string' )
				cmds.setAttr( snap_order_attr, obj_count + 1, type = 'string' )

				Maya_Util().add_attr( obj, self.snap_parent_str, attr_type = 'message' )
				set_parent_attr = Maya_Util().add_attr( obj, self.set_parent_str, attr_type = 'message' )

				cmds.connectAttr( '{0}.{1}'.format( set_node, self.set_child_str ), set_parent_attr, force = True )


				self.add_obj_list( obj )
				self.obj_list_select( index = cmds.textScrollList( self.object_order_scroll, numberOfItems = True, q = True ) )

			else:
				OpenMaya.MGlobal.displayError( "Selected object is already in the list!" )

		else:
			OpenMaya.MGlobal.displayError( "There are no objects selected!" )

	'''
	========================================================================
	---->  Remove Obj  <----
	========================================================================
	'''
	def remove_obj( self, *args ):
		set_name = cmds.textScrollList( self.set_scroll, si = True, q = True )[0]
		obj_name = cmds.textScrollList( self.object_name_scroll, si = True, q = True )[0]
		obj_index = cmds.textScrollList( self.object_name_scroll, selectIndexedItem = True, q = True )[0]

		cmds.sets( obj_name, remove = set_name )
		self.remove_set_connections( obj_index )
		self.break_obj_connections( obj_name )

	'''
	========================================================================
	---->  Select Obj  <----
	========================================================================
	'''
	def select_obj( self, scroll_list, *args ):

		set_name = cmds.textScrollList( scroll_list, si = True, q = True )[0]

		cmds.select( set_name )

	'''
	========================================================================
	---->  Add Obj List  <----
	========================================================================
	'''
	def add_obj_list( self, obj, snap_obj = '' ):
		obj_num = cmds.textScrollList( self.object_order_scroll, numberOfItems = True, q = True )

		cmds.textScrollList( self.object_order_scroll, append = obj_num + 1, e = True )
		cmds.textScrollList( self.object_name_scroll, append = obj, e = True )
		cmds.textScrollList( self.object_connect_scroll, append = self.arrow_str, e = True )
		cmds.textScrollList( self.object_snap_scroll, append = snap_obj, e = True )

	'''
	========================================================================
	---->  Clear Obj List  <----
	========================================================================
	'''
	def clear_obj_list( self ):
		cmds.textScrollList( self.object_order_scroll, removeAll = True, e = True )
		cmds.textScrollList( self.object_name_scroll, removeAll = True, e = True )
		cmds.textScrollList( self.object_connect_scroll, removeAll = True, e = True )
		cmds.textScrollList( self.object_snap_str, removeAll = True, e = True )

	'''
	========================================================================
	---->  Obj List Select  <----
	========================================================================
	'''
	def obj_list_select( self, scroll_list = None, index = None, *args ):
		if not index:
			index = cmds.textScrollList( scroll_list, selectIndexedItem = True, q = True )[0]

		if index:
			cmds.textScrollList( self.object_order_scroll, deselectAll = True, e = True )
			cmds.textScrollList( self.object_name_scroll, deselectAll = True, e = True )
			cmds.textScrollList( self.object_connect_scroll, deselectAll = True, e = True )
			cmds.textScrollList( self.object_snap_scroll, deselectAll = True, e = True )

			cmds.textScrollList( self.object_order_scroll, selectIndexedItem = index, e = True )
			cmds.textScrollList( self.object_name_scroll, selectIndexedItem = index, e = True )
			cmds.textScrollList( self.object_connect_scroll, selectIndexedItem = index, e = True )
			cmds.textScrollList( self.object_snap_scroll, selectIndexedItem = index, e = True )

	'''
	========================================================================
	---->  Add Snap Obj  <----
	========================================================================
	'''
	def add_snap_obj( self, *args ):
		snap_obj = cmds.ls( sl = True )
		main_obj = cmds.textScrollList( self.object_name_scroll, si = True, q = True )[0]

		if snap_obj:
			snap_obj = snap_obj[0]

			snap_attr = '{0}.{1}'.format( snap_obj, self.snap_child_str )

			if not cmds.objExists( snap_attr ):
				snap_attr = Maya_Util().add_attr( snap_obj, self.snap_child_str, 'message' )

			try:
				cmds.connectAttr( snap_attr, '{0}.{1}'.format( main_obj, self.snap_parent_str ), force = True )

			except:
				pass

			order_number = cmds.textScrollList( self.object_order_scroll, si = True, q = True )[0]
			obj_name = cmds.textScrollList( self.object_name_scroll, si = True, q = True )[0]

			self.remove_set_connections( cmds.textScrollList( self.object_name_scroll, selectIndexedItem = True, q = True ) )

			cmds.textScrollList( self.object_order_scroll, append = order_number, e = True )
			cmds.textScrollList( self.object_name_scroll, append = obj_name, e = True )
			cmds.textScrollList( self.object_connect_scroll, append = self.arrow_str, e = True )
			cmds.textScrollList( self.object_snap_scroll, append = snap_obj, e = True )

			self.obj_list_select( index = cmds.textScrollList( self.object_order_scroll, numberOfItems = True, q = True ) )


		else:
			OpenMaya.MGlobal.displayError( "There are no objects selected!" )

	'''
	========================================================================
	---->  Break Obj Connections  <----
	========================================================================
	'''
	def break_obj_connections( self, obj ):
		set_name = cmds.listConnections( '{0}.{1}'.format( obj, self.set_parent_str ) )

		if set_name:
			cmds.disconnectAttr( '{0}.{1}'.format( set_name[0], self.set_child_str ), '{0}.{1}'.format( obj, self.set_parent_str ) )

	'''
	========================================================================
	---->  Build Rig  <----
	========================================================================
	'''
	def build( self, *args ):
		set = cmds.textScrollList( self.set_scroll, si = True, q = True )

		if set:
			FKIK_Snap_Build( set[0] )



'''
========================================================================
---->  FKIK Snap Build  <----
========================================================================
'''
class FKIK_Snap_Build():
	'''
	========================================================================
	---->  Build FK IK Snap  <----
	========================================================================
	'''
	def __init__( self, fkik_snap_set ):
		cmds.select( cl = True )
		self.get_globals()

		for obj in cmds.sets( fkik_snap_set, q = True ):
			controller = DAG_Node( obj )

			obj_snap_attr = '{0}.{1}'.format( controller.name(), self.snap_parent_str )

			if cmds.objExists( obj_snap_attr ):
				obj_snap = cmds.listConnections( obj_snap_attr )

				if obj_snap:
					obj_snap = obj_snap[0]
					snap_grp = DAG_Node( cmds.group( n = '{0}_Snap_Grp'.format( obj.split( '|' )[-1] ), em = True ) )

					snap_grp.set_parent( controller.parent() )

					obj_tra = cmds.xform( controller.name(), ws = True, rp = True, q = True )
					cmds.xform( snap_grp.name(), ws = True, t = obj_tra )

					obj_rot = cmds.xform( controller.name(), ws = True, ro = True, q = True )
					cmds.xform( snap_grp.name(), ws = True, ro = obj_rot )

					cmds.makeIdentity( snap_grp.name(), a = True, t = True, r = True, s = True )

					cmds.parentConstraint( obj_snap, snap_grp.name(), mo = True )

					snap_grp_attr = Maya_Util().add_attr( snap_grp.name(), self.snap_parent_str, 'message' )
					cmds.connectAttr( snap_grp_attr, obj_snap_attr, force = True )

		cmds.select( cl = True )

	'''
	========================================================================
	---->  Get Globals  <----
	========================================================================
	'''
	def get_globals( self ):
		# Load global Values
		self.main_set = 'fkik_snap_set'

		self.snap_order_attr = 'snap_order'

		self.opposite_set_str = 'opposite_set'
		self.set_parent_str = 'set_parent'
		self.set_child_str = 'set_child'

		self.snap_parent_str = 'snap_parent'
		self.snap_child_str = 'snap_child'

class Maya_Util():
	'''
	========================================================================
	---->  Add Attribute  <----
	========================================================================
	'''
	def add_attr( self, obj, attr_name, attr_type ):
		if not cmds.objExists( '{0}.{1}'.format( obj, attr_name ) ):
			try:
				cmds.addAttr( obj, longName = attr_name, at = attr_type )

			except:
				cmds.addAttr( obj, longName = attr_name, dt = attr_type )

		return '{0}.{1}'.format( obj, attr_name )


'''
========================================================================
---->  DAG Node Utilities  <----
========================================================================
'''
class DAG_Node():
	def __init__( self, node ):
		selection_list = OpenMaya.MSelectionList()
		selection_list.add( node )
		self.m_obj = OpenMaya.MObject()
		selection_list.getDependNode( 0, self.m_obj )

	'''
	========================================================================
	---->  DAG Full Path Name  <----
	========================================================================
	'''
	def name( self ):
		"""
		*Returns:*
			* ``node_name`` Returns DAG's full path name.
		"""
		nodeFn = OpenMaya.MFnDagNode( self.m_obj )
		node_name = nodeFn.fullPathName()

		return node_name

	'''
	========================================================================
	---->  DAG Parent  <----
	========================================================================
	'''
	def parent( self ):
		"""
		*Returns:*
			* ``node_parent`` Returns DAG's parent or None.
		"""
		node_parent = cmds.listRelatives( self.name(), parent = True, f = True )

		if node_parent:
			return DAG_Node( node_parent[0] )

		else:
			return None

	'''
	========================================================================
	---->  Set DAG Parent  <----
	========================================================================
	'''
	def set_parent( self, parent ):
		cmds.parent( self.name(), parent.name() )


