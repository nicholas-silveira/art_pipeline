import maya.cmds as cmds # @UnresolvedImport
import maya.mel as mel # @UnresolvedImport

import utilities.maya_dag as maya_dag
reload( maya_dag )

import utilities.maya_controller as maya_controller
reload( maya_controller )

import utilities.maya_search as maya_search
reload( maya_search )


class Crack_Tool():
	def crack_obj( self, dag_node, crack_value, *args ):
		cmds.duplicate( dag_node.name() )[0]
		mesh_copy = maya_dag.DAG_Node()
		cmds.delete( mesh_copy.name(), ch = True )
		cmds.makeIdentity( mesh_copy.name(), a = True, t = True, r = True, s = True )

		dag_node.hide()
		dag_node.short_name()
		cmds.select( mesh_copy.name() )
		mel.eval( 'solidShatter( "{0}_shatter_grp", {1}, 0, 1, 0, 0, 0, 0, 3, "shapes", 0, 0);'.format( dag_node.short_name(), crack_value ) )
		cmds.selectMode( object = True )


	def create_plane_rig( self ):
		nurb_name = 'plane'

		cmds.group( n = '{0}Rig_grp'.format( nurb_name ), em = True )
		plane_grp_dag = maya_dag.DAG_Node()

		cmds.group( n = '{0}Controller_grp'.format( nurb_name ), em = True )
		controller_grp_dag = maya_dag.DAG_Node()

		cmds.nurbsPlane( n = '{0}_nurb'.format( nurb_name ), p = [0, 0, 0], ax = [0, 1, 0], w = 10, lr = 1, d = 3, u = 4, v = 1, ch = True )
		plane_nurb_dag = maya_dag.DAG_Node()

		soft_mod = cmds.softMod( '{0}.cv[3][0:3]'.format( plane_nurb_dag.name() ) )[0]
		soft_mod_handle_dag = maya_dag.DAG_Node()

		maya_controller.Maya_Controller( name = '{0}Deformer_controller'.format( nurb_name ), shape = 'diamond_curve' )
		controller_dag = maya_dag.DAG_Node()

		plane_nurb_dag.set_parent( plane_grp_dag )
		controller_grp_dag.set_parent( plane_grp_dag )
		controller_dag.set_parent( controller_grp_dag )
		soft_mod_handle_dag.set_parent( plane_nurb_dag )
		soft_mod_handle_dag.parent_constraint( controller_dag )

		controller_grp_dag.parent_constraint( plane_nurb_dag )
		controller_grp_dag.scale_constraint( plane_nurb_dag )

		soft_mod_handle_dag.hide()

		cmds.setAttr( '{0}.relative'.format( soft_mod ), 1 )
		cmds.setAttr( '{0}.falloffAroundSelection'.format( soft_mod ), 0 )

		cmds.select( plane_nurb_dag.name() )


	def attach_plane_rig( self, objects ):
		plane_name = 'plane_nurb'

		if plane_name in objects:
			cmds.select( plane_name, deselect = True )

			transform_nodes = maya_search.get_object_type( objects, 'mesh' )

			cmds.select( transform_nodes )
			cmds.select( plane_name, add = True )

			cmds.CreateWrap()

	def create_cluster( self, *args ):
		cmds.cluster()









