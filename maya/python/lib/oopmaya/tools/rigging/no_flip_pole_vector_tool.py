'''
I N S T A L L A T I O N::

Step 1:
Copy "no_flip_pole_vector_tool.py" to your Maya plugins directory.
Windows: C:\Users\UserName\Documents\maya\scripts

Step 2:
Run this in the Maya's Script Editor under the Python tab...

import no_flip_pole_vector_tool as nfpv

nfpv.No_Flip_Pole_Vector().show_ui()


If you have any problems email me at Nicholas.Silveira@gmail.com
'''



import sys
import functools

import maya.cmds as cmds
import maya.OpenMaya as OpenMaya

VERSION = 1.0

'''
========================================================================
---->  No Flip Pole Vector  <----
========================================================================
'''
class No_Flip_Pole_Vector():
	"""
	*Examples:* ::
		import no_flip_pole_vector_tool as nfpv
		
		# Show ui
		nfpv.No_Flip_Pole_Vector().show_ui()
	
	*Author:*
	    * nicholas.silveira, Nicholas.Silveira@gmail.com, Jun 13, 2013 8:53:53 AM
	"""
	'''
	========================================================================
	---->  Shows No Flip Pole Vector ui  <----
	========================================================================
	'''
	def show_ui( self ):
		"""
		*Examples:* ::
			import no_flip_pole_vector_tool as nfpv
			
			# Show ui
			nfpv.No_Flip_Pole_Vector().show_ui()
		"""
		if cmds.window( 'no_flip_pole_vector_window', exists = True, q = True ):
			cmds.deleteUI( 'no_flip_pole_vector_window' )

		self.no_flip_pole_vector_ui()

	'''
	========================================================================
	---->  No Flip Pole Vector ui  <----
	========================================================================
	'''
	def no_flip_pole_vector_ui( self ):
		self.root_joint = None
		self.controller = None
		self.pole_vector = None

		window = cmds.window( 'no_flip_pole_vector_window', title = 'No Flip Pole Vector {0}'.format( VERSION ), menuBar = True )

		cmds.menu( label = 'Help' )
		cmds.menuItem( 'sample"', label = 'Build Sample', c = self.sample )
		cmds.menuItem( 'code_sample"', label = 'Code Sample', c = self.code_sample )
		cmds.menuItem( 'about"', label = 'About No Flip Pole Vector', c = self.about )

		cmds.columnLayout()

		cmds.rowColumnLayout ( nc = 2, columnWidth = [( 1, 100 ), ( 2, 200 )] )
		cmds.text( label = 'Name: ', align = 'right' )
		self.name_text = cmds.textField()
		cmds.setParent( '..' )

		cmds.rowColumnLayout ( nc = 1, columnWidth = ( 1, 300 ) )
		cmds.separator( height = 20, style = 'in' )

		cmds.rowColumnLayout ( nc = 2, columnWidth = [( 1, 100 ), ( 2, 200 )] )
		cmds.button( label = 'Root Joint', c = functools.partial( self.set_text_field, 'root_joint' ) )
		self.root_joint_text = cmds.textField()

		cmds.button( label = 'Controller', c = functools.partial( self.set_text_field, 'controller' ) )
		self.controller_text = cmds.textField()

		cmds.button( label = 'Pole Vector', c = functools.partial( self.set_text_field, 'pole_vector' ) )
		self.pole_vector_text = cmds.textField()
		cmds.setParent( '..' )

		cmds.rowColumnLayout ( nc = 1, columnWidth = ( 1, 300 ) )
		cmds.separator( height = 20, style = 'in' )
		cmds.button( label = 'Build No Flip Pole Vector', c = self.run_setup )

		cmds.showWindow( window )

	'''
	========================================================================
	---->  Set Maya ui text field  <----
	========================================================================
	'''
	def set_text_field( self, text_field_name, *args ):
		"""		
		*Arguments:*
			* ``text_field_name`` Pass a text field name that will take on the selected objects name.
		
		*Examples:* ::
			import pymel.core
		
			import no_flip_pole_vector_tool as nfpv
			reload( nfpv )
			
			# Show ui
			no_flip_pole_vector_tool = nfpv.No_Flip_Pole_Vector()
			no_flip_pole_vector.show_ui()
			
			# Create locator
			cmds.spaceLocator()
			
			# Add selected to text field
			no_flip_pole_vector.set_text_field('controller')
		"""
		objs = cmds.ls( sl = True )

		if len( objs ) == 1:
			obj_name = objs[0].split( '|' )[-1]
			obj_dag = DAG_Node( cmds.ls( sl = True )[0] )

			if text_field_name == 'root_joint':
				self.root_joint = obj_dag
				cmds.textField( self.root_joint_text, edit = True, text = obj_name )

			elif text_field_name == 'controller':
				self.controller = obj_dag
				cmds.textField( self.controller_text, edit = True, text = obj_name )

			elif text_field_name == 'pole_vector':
				self.pole_vector = obj_dag
				cmds.textField( self.pole_vector_text, edit = True, text = obj_name )

		elif len( objs ) >= 1:
			OpenMaya.MGlobal.displayError( "There are to many objects selected!" )

		elif len( objs ) <= 1:
			OpenMaya.MGlobal.displayError( "There are no objects selected!" )

	'''
	========================================================================
	---->  Run Setup gets ui data and runs build  <----
	========================================================================
	'''
	def run_setup( self, *args ):
		self.name = cmds.textField( self.name_text, text = True, q = True )

		if self.root_joint:
			self.root_joint = self.root_joint.name()

		if self.controller:
			self.controller = self.controller.name()

		if self.pole_vector:
			self.pole_vector = self.pole_vector.name()

		self.build( root_joint = self.root_joint,
		                      controller = self.controller,
		                      pole_vector = self.pole_vector,
		                      name = self.name )

	'''
	========================================================================
	---->  Builds No Flip Pole Vector  <----
	========================================================================
	'''
	def build( self, root_joint = None, controller = None, pole_vector = None, name = '', *args ):
		"""
		*Keyword Arguments:*
			* ``root_joint`` Pass the top of the joint chain.
			* ``controller`` Pass the main controller.
			* ``pole_vector`` Pass the pole vector controller.
			* ``name`` Add prefix to all created nodes
		
		*Returns:*
			* ``True`` If process finishes.
		
		*Examples:* ::
			import pymel.core
		
			import no_flip_pole_vector_tool as nfpv
			reload( nfpv )
		
			# Build example rig
			# Build joint chain
			cmds.select( cl = True )
			chain1_jnt = cmds.joint( n = 'chain1_jnt', p = [0, 6, 0] )
			chain2_jnt = cmds.joint( n = 'chain2_jnt', p = [0, 3, 1] )
			chain3_jnt = cmds.joint( n = 'chain3_jnt', p = [0, 0, 0] )
			
			# Build ikHandle
			cmds.ikHandle ( n = 'chain_ikHandle', startJoint = chain1_jnt, endEffector = chain3_jnt, sol = 'ikRPsolver' )
			chain_ikHandle = cmds.selected()[0]
			
			# Build pole vector
			pole_vector_loc = cmds.spaceLocator()
			pole_vector_loc.rename( 'pole_vector_loc' )
			pole_vector_loc.translateY.set( 3 )
			pole_vector_loc.translateZ.set( 2 )
			cmds.poleVectorConstraint( pole_vector_loc, chain_ikHandle )
			
			# Build controller
			controller = cmds.circle ( nr = [0, 1, 0], r = 1 )[0]
			cmds.pointConstraint( controller, chain_ikHandle )
			
			# Standalone code
			nfpv.No_Flip_Pole_Vector().build( root_joint = chain1_jnt, controller = controller, pole_vector = pole_vector_loc, name = 'example' )
		"""
		if root_joint == None or controller == None or pole_vector == None:
			get_selected_objs = cmds.ls( sl = True )

			if len( get_selected_objs ) == 3:
				root_joint = DAG_Node( get_selected_objs[0] )
				controller = DAG_Node( get_selected_objs[1] )
				pole_vector = DAG_Node( get_selected_objs[2] )

			elif len( get_selected_objs ) >= 3:
				OpenMaya.MGlobal.displayError( "There more than 3 objects selected!" )
				return False

			elif len( get_selected_objs ) <= 3:
				OpenMaya.MGlobal.displayError( "There less than 3 objects selected!" )
				return False

		else:
			root_joint = DAG_Node( root_joint )
			controller = DAG_Node( controller )
			pole_vector = DAG_Node( pole_vector )

		cmds.select( cl = True )

		# Get pole vector parent
		pole_parent = pole_vector.parent()

		# Create pole main grp
		self.pole_main_grp = DAG_Node( cmds.group( n = '{0}_poleMain_grp'.format( name ), em = True ) )

		# Create pole parent grp
		pole_parent_grp = DAG_Node( cmds.group( n = '{0}_poleParent_grp'.format( name ), em = True ) )

		if pole_parent:
			pole_parent_grp.set_parent( pole_parent )

		controller_pivot = cmds.xform( controller.name(), ws = True, rp = True, q = True )
		controller_rotation = cmds.xform( controller.name(), ws = True, rotation = True, q = True )

		cmds.xform( pole_parent_grp.name(), translation = controller_pivot, ws = True )
		cmds.xform( pole_parent_grp.name(), rotation = controller_rotation, ws = True )

		pole_vector.set_parent( pole_parent_grp )

		# Create pole world grp
		pole_world_grp = DAG_Node( cmds.group( n = '{0}_poleWorld_grp'.format( name ), em = True ) )
		pole_world_grp.set_parent( self.pole_main_grp )

		cmds.xform( pole_world_grp.name(), translation = controller_pivot, ws = True )
		cmds.xform( pole_world_grp.name(), rotation = controller_rotation, ws = True )

		# Object up vector
		up_vector_grp = DAG_Node( cmds.group( n = '{0}_upVector_grp'.format( name ), em = True ) )
		up_vector_grp.set_parent( self.pole_main_grp )

		cmds.pointConstraint( root_joint.name() , up_vector_grp.name() )

		# Create bottom chain aim locator
		aim_grp = DAG_Node( cmds.group( n = '{0}_aim_grp'.format( name ), em = True ) )
		aim_grp.set_parent( self.pole_main_grp )

		cmds.aimConstraint ( root_joint.name(), aim_grp.name(),
									aimVector = [1, 0, 0],
									upVector = [0, 1, 0],
									worldUpType = "objectrotation",
									worldUpVector = [-1, 0, 0],
									worldUpObject = up_vector_grp.name() )

		cmds.pointConstraint( controller.name(), aim_grp.name() )

		# Create pole vector parent groups
		pole_controller_grp = DAG_Node( cmds.group( n = '{0}_poleController_grp'.format( name ), em = True ) )
		pole_rotate_grp = DAG_Node( cmds.group( n = '{0}_poleRotate_grp'.format( name ), em = True ) )

		pole_rotate_grp.set_parent( pole_controller_grp )
		pole_controller_grp.set_parent( aim_grp )

		# Set controller orientation on main pole group
		cmds.xform( pole_controller_grp.name(), translation = controller_pivot, ws = True )
		cmds.xform( pole_controller_grp.name(), rotation = controller_rotation, ws = True )

		# Connect rotate group's rotation Y,Z for twist follow
		cmds.connectAttr( '{0}.rotateY'.format( controller.name() ), '{0}.rotateY'.format( pole_rotate_grp.name() ) )
		cmds.connectAttr( '{0}.rotateZ'.format( controller.name() ), '{0}.rotateZ'.format( pole_rotate_grp.name() ) )

		# Create and attach new custom attribute
		position_follow_str = 'position_follow'
		rotation_follow_str = 'rotation_follow'

		if not cmds.objExists( '{0}.{1}'.format( pole_vector.name(), position_follow_str ) ):
			cmds.addAttr( pole_vector.name(), longName = position_follow_str, attributeType = 'double', min = 0, max = 1, k = True )

		if not cmds.objExists( '{0}.{1}'.format( pole_vector.name(), rotation_follow_str ) ):
			cmds.addAttr( pole_vector.name(), longName = rotation_follow_str, attributeType = 'double', min = 0, max = 1, k = True )

		cmds.setAttr( '{0}.{1}'.format( pole_vector.name(), position_follow_str ), 1 )
		cmds.setAttr( '{0}.{1}'.format( pole_vector.name(), rotation_follow_str ), 1 )

		# Constraint pole parent to world and follow grps
		point_constraint = DAG_Node( cmds.pointConstraint( pole_world_grp.name(), pole_rotate_grp.name(), pole_parent_grp.name() )[0] )
		orient_constraint = DAG_Node( cmds.orientConstraint( pole_world_grp.name(), pole_rotate_grp.name(), pole_parent_grp.name() )[0] )

		position_constraint_weights = cmds.pointConstraint( point_constraint.name(), weightAliasList = True, query = True )
		rotation_constraint_weights = cmds.orientConstraint( orient_constraint.name(), weightAliasList = True, query = True )

		cmds.connectAttr( '{0}.{1}'.format( pole_vector.name(), position_follow_str ), '{0}.{1}'.format( point_constraint.name(), position_constraint_weights[1] ) )
		cmds.connectAttr( '{0}.{1}'.format( pole_vector.name(), rotation_follow_str ), '{0}.{1}'.format( orient_constraint.name(), rotation_constraint_weights[1] ) )

		Maya_Util().reverse_node( parent_attr = '{0}.{1}'.format( pole_vector.name(), position_follow_str ),
										  child_attr = '{0}.{1}'.format( point_constraint.name(), position_constraint_weights[0] ),
										  node_name = '{0}_positionFollow_node'.format( name ) )

		Maya_Util().reverse_node( parent_attr = '{0}.{1}'.format( pole_vector.name(), rotation_follow_str ),
										  child_attr = '{0}.{1}'.format( orient_constraint.name(), rotation_constraint_weights[0] ),
										  node_name = '{0}_rotationFollow_node'.format( name ) )

		cmds.select( cl = True )

		sys.stdout.write( '// Result: No FLip Pole Vector is finished!' )

		return True

	'''
	========================================================================
	---->  Build Rig Sample  <----
	========================================================================
	'''
	def sample( self, *args ):
		# Build joint chain
		cmds.select( cl = True )
		chain1_jnt = cmds.joint( n = 'chain1_jnt', p = [0, 6, 0] )
		cmds.joint( n = 'chain2_jnt', p = [0, 3, 1] )
		chain3_jnt = cmds.joint( n = 'chain3_jnt', p = [0, 0, 0] )

		# Build ikHandle
		chain_ikHandle = cmds.ikHandle ( n = 'chain_ikHandle', startJoint = chain1_jnt, endEffector = chain3_jnt, sol = 'ikRPsolver' )[0]

		# Build pole vector
		pole_vector_loc = cmds.spaceLocator( n = 'pole_vector_loc' )[0]
		cmds.setAttr( '{0}.translateY'.format( pole_vector_loc ), 3 )
		cmds.setAttr( '{0}.translateZ'.format( pole_vector_loc ), 2 )
		cmds.poleVectorConstraint( pole_vector_loc, chain_ikHandle )

		# Build controller
		controller = cmds.circle ( nr = [0, 1, 0], r = 1 )[0]
		cmds.pointConstraint( controller, chain_ikHandle )

		# Run Standalone code
		No_Flip_Pole_Vector().build( root_joint = chain1_jnt, controller = controller, pole_vector = pole_vector_loc, name = 'example' )

	'''
	========================================================================
	---->  Code Sample  <----
	========================================================================
	'''
	def code_sample( self, *args ):
		code = '''
		import maya.cmds
		import no_flip_pole_vector_tool as nfpv
		
		# Show ui
		nfpv.No_Flip_Pole_Vector().show_ui()
		
		"""
		========================================================================
		---->  Run Standalone code  <----
		========================================================================
		"""
		nfpv.No_Flip_Pole_Vector().build( root_joint = None, controller = None, pole_vector = None, name = 'example' )
		'''

		if cmds.window( 'code_sample_window', exists = True, q = True ):
			cmds.deleteUI( 'code_sample_window' )

		cmds.window( 'code_sample_window', title = 'Code Sample' )
		cmds.paneLayout()
		cmds.scrollField( editable = False, text = code.replace( '		', '' ) )
		cmds.showWindow()

	'''
	========================================================================
	---->  About No Flip Pole Vector  <----
	========================================================================
	'''
	def about( self, *args ):
		about = '''
		"""
		========================================================================
		---->  No Flip Pole Vector  <----
		========================================================================
		"""
		This tool builds a no flip pole vector. After passing in a root joint,
		main controller, and pole vector the tool will allow the pole vector to
		follow the main controller or switch to world space.
		
		If you have any questions email me at Nicholas.Silveira@gmail.com
		'''

		if cmds.window( 'about_window', exists = True, q = True ):
			cmds.deleteUI( 'about_window' )

		cmds.window( 'about_window', title = 'About' )
		cmds.paneLayout()
		cmds.scrollField( editable = False, text = about.replace( '		', '' ) )
		cmds.showWindow()



'''
========================================================================
---->  Maya Utilities  <----
========================================================================
'''
class Maya_Util():
	'''
	========================================================================
	---->  Create a Maya reverse node  <----
	========================================================================
	'''
	def reverse_node ( self, parent_attr, child_attr, node_name = '' ):
		"""
		*Arguments:*
			* ``parent_attr`` Pass the parent attribute.
			* ``child_attr`` Pass the child attribute.
		
		*Keyword Arguments:*
			* ``node_name`` Pass a node name.
		
		*Returns:*
			* ``node`` Returns reverse node
		"""
		node = cmds.shadingNode( 'reverse', name = node_name, asUtility = True )

		cmds.connectAttr( parent_attr, '{0}.inputX'.format( node ) )
		cmds.connectAttr( '{0}.outputX'.format( node ), child_attr )



'''
========================================================================
---->  DAG Node Utilities  <----
========================================================================
'''
class DAG_Node():
	"""
	*Arguments:*
		* ``node`` Makes a DAG instance from passed node
	
	*Examples:* ::
		import maya.cmds as cmds
		import no_flip_pole_vector_tool as nfpv
	
		exampleA_grp = nfpv.DAG_Node( cmds.group( n = 'exampleA_grp', em = True ) )
		exampleB_grp = nfpv.DAG_Node( cmds.group( n = 'exampleB_grp', em = True ) )
		
		exampleA_grp.set_parent(exampleB_grp)
		print exampleA_grp.parent()
		print exampleA_grp.name()
	"""
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
