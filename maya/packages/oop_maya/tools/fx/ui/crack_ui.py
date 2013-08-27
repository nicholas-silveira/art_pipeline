import maya.cmds as cmds # @UnresolvedImport

import oopmaya.core as oopmaya # @UnresolvedImport
reload( oopmaya )

import oopmaya.tools.crack_tool as crack_tool # @UnresolvedImport
import oopmaya.tools.simulation_tool as simulation_tool # @UnresolvedImport
import oopmaya.tools.skin_convert_tool as skin_convert_tool # @UnresolvedImport

reload( crack_tool )
reload( simulation_tool )
reload( skin_convert_tool )

VERSION = 1.0



class Crack_Tool():
	'''
   ========================================================================
   ---->  Run Fissure Tool  <----
   ========================================================================
   '''
	def __init__( self ):
		window_name = 'fissureToolWindow'
		window_width = 200
		window_height = 200

		if cmds.window( window_name, exists = True, q = True ):
			cmds.deleteUI( window_name )

		cmds.window( window_name, title = 'Fissure Tool {0}'.format( VERSION ), widthHeight = ( window_width, window_height ) )
		form = cmds.formLayout()
		tabs = cmds.tabLayout( innerMarginWidth = 5, innerMarginHeight = 5 )
		cmds.formLayout( form, edit = True, attachForm = ( ( tabs, 'top', 0 ), ( tabs, 'left', 0 ), ( tabs, 'bottom', 0 ), ( tabs, 'right', 0 ) ) )

		# Crack Row
		crack_row = cmds.rowColumnLayout( numberOfColumns = 1 )
		cmds.separator( style = 'none', height = 20 )
		cmds.text( label = 'Crack Pieces' )
		self.crack_float = cmds.floatField( value = 50, precision = 0 )
		cmds.button( l = 'Crack Mesh', w = window_width, c = self.run_crack_obj )
		cmds.separator( height = 40, style = 'in' )

		cmds.button( l = 'Create Plane Rig', w = window_width, c = self.run_create_plane_rig )
		cmds.button( l = 'Attach Plane Rig', w = window_width, c = self.run_attach_plane_rig )
		cmds.separator( height = 40, style = 'in' )

		cmds.button( l = 'Create Cluster', w = window_width, c = self.run_create_cluster )
		cmds.setParent( '..' )

		# Simulation Row
		sim_row = cmds.rowColumnLayout( numberOfColumns = 1 )
		cmds.separator( style = 'none', height = 20 )
		cmds.text( label = 'Gravity Magnitude' )
		self.magnitude_float = cmds.floatField( value = 50, precision = 2 )
		cmds.button( l = 'Add Rigid Body', w = window_width, c = self.run_add_rigid_body )
		cmds.separator( height = 40, style = 'in' )

		cmds.button( l = 'Add Crack Distance', w = window_width, c = self.run_create_crack_distance )
		cmds.button( l = 'Run Crack Distance', w = window_width, c = self.run_build_crack_distance )
		cmds.separator( height = 40, style = 'in' )

		cmds.button( l = 'Bake Simulation', w = window_width, c = self.run_bake_sim )
		cmds.setParent( '..' )

		# Export Row
		export_row = cmds.rowColumnLayout( numberOfColumns = 1 )
		cmds.separator( style = 'none', height = 20 )
		cmds.button( l = 'Convert to game skin', w = window_width, c = self.run_convert_to_game_skin )
		cmds.separator( height = 40, style = 'in' )

		cmds.button( l = 'Export FBX Mesh', w = window_width )
		cmds.button( l = 'Export FBX Skin', w = window_width )
		cmds.button( l = 'Export FBX Animation', w = window_width )
		cmds.setParent( '..' )

		cmds.tabLayout( tabs, edit = True, tabLabel = ( ( crack_row, 'Crack' ), ( sim_row, 'Simulation' ), ( export_row, 'Export' ) ) )

		cmds.showWindow()

	'''
   ========================================================================
   ---->  Run Crack Obj  <----
   ========================================================================
   '''
	def run_crack_obj( self, *args ):
		crack_value = cmds.floatField( self.crack_float, value = True, q = True )

		selected = cmds.ls( sl = True )

		if len( selected ) == 1:
			dag_node = oopmaya.DAG_Node()
			crack_tool.Crack_Tool().crack_obj( dag_node, crack_value )
			
			oopmaya.message( 'Finished cracking mesh!' )

		elif len( selected ) == 0:
			oopmaya.error( 'There are no objects selected!' )

		elif len( selected ) >= 1:
			oopmaya.error( 'There are to many objects selected!' )

	'''
   ========================================================================
   ---->  Run Create Plane Rig  <----
   ========================================================================
   '''
	def run_create_plane_rig( self, *args ):
		crack_tool.Crack_Tool().create_plane_rig()
		
		oopmaya.message( 'Created plane rig!' )

	'''
   ========================================================================
   ---->  Run Attach Plane Rig  <----
   ========================================================================
   '''
	def run_attach_plane_rig( self, *args ):
		objects = cmds.ls( sl = True )
		crack_tool.Crack_Tool().attach_plane_rig( objects )
		
		oopmaya.message( 'Attached plane rig!' )

	'''
   ========================================================================
   ---->  Run Create Cluster  <----
   ========================================================================
   '''
	def run_create_cluster( self, *args ):
		mesh = cmds.ls( sl = True, objectsOnly = True )[0]
		
		crack_tool.Crack_Tool().create_cluster( mesh )
		
		oopmaya.message( 'Created cluster!' )

	'''
   ========================================================================
   ---->  Run Add Rigid Body  <----
   ========================================================================
   '''
	def run_add_rigid_body( self, *args ):
		mag_value = cmds.floatField( self.magnitude_float, value = True, q = True )

		objects = cmds.ls( sl = True )
		objects = oopmaya.get_object_type( objects, 'mesh' )
		
		simulation_tool.Simulation_Tool().add_rigid_body( objects, magnitude = mag_value )
		
		oopmaya.message( 'Added rigid body!' )
		
	'''
   ========================================================================
   ---->  Run Create Crack Distance  <----
   ========================================================================
   '''
	def run_create_crack_distance( self, *args ):
		objects = cmds.ls( sl = True )
		objects = oopmaya.get_object_type( objects, 'mesh' )
		
		simulation_tool.Simulation_Tool().create_crack_distance( objects )
		
		oopmaya.message( 'Added crack distance!' )
	
	'''
   ========================================================================
   ---->  Run Build Crack Distance  <----
   ========================================================================
   '''
	def run_build_crack_distance( self, *args ):
		dis_locator = cmds.ls( sl = True )[0]
		
		simulation_tool.Simulation_Tool().build_crack_distance( dis_locator )
		
		oopmaya.message( 'Build crack distance!' )
	
	'''
   ========================================================================
   ---->  Run Bake Sim  <----
   ========================================================================
   '''
	def run_bake_sim( self, *args ):
		objects = cmds.ls( sl = True )
		objects = oopmaya.get_object_type( objects, 'mesh' )
		
		simulation_tool.Simulation_Tool().bake_sim( objects, bake_attr = ['translate'] )
		
		oopmaya.message( 'Finished baking simulation!' )
	
	'''
   ========================================================================
   ---->  Run Convert To Game Skin  <----
   ========================================================================
   '''
	def run_convert_to_game_skin( self, args ):
		objects = cmds.ls( sl = True )
		
		skin_convert_tool.Skin_Convert_Tool().convert_to_game_skin( objects )
		
		oopmaya.message( 'Finished converting mesh onto joints!' )
