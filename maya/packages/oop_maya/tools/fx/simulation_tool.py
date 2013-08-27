import maya.cmds as cmds # @UnresolvedImport

import oopmaya.core as oopmaya # @UnresolvedImport
reload( oopmaya )



'''
========================================================================
---->  Simulation Tool  <----
========================================================================
'''
class Simulation_Tool():
	'''
	========================================================================
	---->  Add Rigid Body  <----
	========================================================================
	'''
	def add_rigid_body( self, objects, magnitude = 50 ):
		
		cmds.rigidBody( objects, active = False, m = magnitude, collisions = False )
		
		cmds.gravity( pos = [0, 0, 0], m = magnitude, att = 0, dx = 0, dy = -1, dz = 0, mxd = -1, vsh = 'none', vex = 0, vof = [0, 0, 0], vsw = 360, tsr = 0.5 )
		gravity_dag = oopmaya.DAG_Node()
		cmds.connectDynamic( objects, fields = gravity_dag.name() )

	'''
	========================================================================
	---->  Create Crack Distance  <----
	========================================================================
	'''
	def create_crack_distance( self, objects ):
		distance_locator_name = 'distance_locator'
				
		cmds.spaceLocator( n = distance_locator_name )
		distance_locator_dag = oopmaya.DAG_Node()

		for obj in objects:
			distance_node = cmds.shadingNode ( 'distanceBetween', asUtility = True, name = '{0}Distance_node'.format( obj ) )

			cmds.connectAttr ( '{0}.worldMatrix[0]'.format( distance_locator_dag.name() ), '{0}.inMatrix1'.format( distance_node ), force = True )
			cmds.connectAttr ( '{0}.transMinusRotatePivot'.format( obj ), '{0}.point2'.format( distance_node ), force = True )
			
			if not cmds.objExists( '{0}.{1}'.format( distance_locator_dag.name(), obj ) ):
				cmds.addAttr( distance_locator_dag.name(), ln = obj, at = "message" )
				
			if not cmds.objExists( '{0}.{1}'.format( distance_node, distance_locator_name ) ):
				cmds.addAttr( distance_node, ln = distance_locator_name, at = "message" )
			
			cmds.connectAttr ( '{0}.{1}'.format( distance_node, distance_locator_name ), '{0}.{1}'.format( distance_locator_dag.name(), obj ), force = True )
			
		cmds.select( distance_locator_dag.name() )

	'''
	========================================================================
	---->  Build Crack Distance  <----
	========================================================================
	'''
	def build_crack_distance( self, distance_locator ):
		obj_distance = {}
		
		current_time = cmds.currentTime( query = True )
		loc_custon_attrs = cmds.listAttr( ud = True )
		
		for attr in loc_custon_attrs:
			distance_node = cmds.listConnections( '{0}.{1}'.format( distance_locator, attr ) )
			
			if distance_node:
				distance_node = distance_node[0]
				mesh_node = cmds.listConnections( '{0}.point2'.format( distance_node ) )

				if mesh_node:
					mesh_node = mesh_node[0]
					
					obj_distance[cmds.getAttr( '{0}.distance'.format( distance_node ) )] = mesh_node

		for value in sorted( obj_distance ):
			obj = obj_distance[value]

			obj_active = '{0}.active'.format( obj )

			if cmds.objExists( obj_active ):
				cmds.setAttr( obj_active, 0 )
				cmds.setKeyframe( obj_active, time = current_time )

				current_time = current_time + 0.5
				cmds.setAttr( obj_active, 1 )
				cmds.setKeyframe( obj_active, time = current_time )

	'''
	========================================================================
	---->  Bake Sim  <----
	========================================================================
	'''
	def bake_sim( self, objects, bake_attr = ['all'] ):
		bake_attr_list = []
		
		min_time = cmds.playbackOptions( min = True, q = True )
		max_time = cmds.playbackOptions( max = True, q = True )
		
		for obj in objects:
			if 'all' in bake_attr or 'translate' in bake_attr:
				bake_attr_list.append( '{0}.translateX'.format( obj ) )
				bake_attr_list.append( '{0}.translateY'.format( obj ) )
				bake_attr_list.append( '{0}.translateZ'.format( obj ) )
				
			if 'all' in bake_attr or 'rotate' in bake_attr:
				bake_attr_list.append( '{0}.rotateX'.format( obj ) )
				bake_attr_list.append( '{0}.rotateY'.format( obj ) )
				bake_attr_list.append( '{0}.rotateZ'.format( obj ) )
				
			if 'all' in bake_attr or 'scale' in bake_attr:
				bake_attr_list.append( '{0}.scaleX'.format( obj ) )
				bake_attr_list.append( '{0}.scaleY'.format( obj ) )
				bake_attr_list.append( '{0}.scaleZ'.format( obj ) )
		
		cmds.bakeResults( bake_attr_list, simulation = True, t = ( min_time, max_time ) )
		cmds.DeleteRigidBodies()
		
		
