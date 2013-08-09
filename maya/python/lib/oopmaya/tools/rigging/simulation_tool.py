import maya.cmds as cmds # @UnresolvedImport

import utilities.maya_dag as maya_dag
reload( maya_dag )

import utilities.maya_search as maya_search
reload( maya_search )


class Simulation_Tool():
	def add_rigid_body( self, objects, magnitude = 50 ):
		objects = maya_search.get_object_type( objects, 'mesh' )
		
		cmds.rigidBody( objects, active = False, m = magnitude, collisions = False )
		
		cmds.gravity( pos = [0, 0, 0], m = magnitude, att = 0, dx = 0, dy = -1, dz = 0, mxd = -1, vsh = 'none', vex = 0, vof = [0, 0, 0], vsw = 360, tsr = 0.5 )
		gravity_dag = maya_dag.DAG_Node()
		cmds.connectDynamic( objects, fields = gravity_dag.name() )

	def create_crack_distance( self, objects ):
		distance_locator_name = 'distance_locator'
		
		objects = maya_search.get_object_type( objects, 'mesh' )
		
		cmds.spaceLocator( n = distance_locator_name )
		distance_locator_dag = maya_dag.DAG_Node()

		for obj in objects:
			distance_node = cmds.shadingNode ( 'distanceBetween', asUtility = True, name = '{0}Distance_node'.format( obj ) )

			cmds.connectAttr ( '{0}.worldMatrix[0]'.format( distance_locator_dag.name() ), '{0}.inMatrix1'.format( distance_node ), force = True )
			cmds.connectAttr ( '{0}.transMinusRotatePivot'.format( obj ), '{0}.point2'.format( distance_node ), force = True )
			
			cmds.addAttr( distance_locator_dag.name(), ln = obj, at = "message" )
			cmds.addAttr( distance_node, ln = distance_locator_name, at = "message" )
			
			cmds.connectAttr ( '{0}.{1}'.format( distance_node, distance_locator_name ), '{0}.{1}'.format( distance_locator_dag.name(), obj ), force = True )
			
		cmds.select( distance_locator_dag.name() )

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

	def bake_sim( self, objects ):
		bake_attr = []
		
		min_time = cmds.playbackOptions( min = True, q = True )
		max_time = cmds.playbackOptions( max = True, q = True )
		
		objects = maya_search.get_object_type( objects, 'mesh' )
		
		for obj in objects:
			bake_attr.append( '{0}.translateX'.format( obj ) )
			bake_attr.append( '{0}.translateY'.format( obj ) )
			bake_attr.append( '{0}.translateZ'.format( obj ) )
		
		cmds.bakeResults( bake_attr, simulation = True, t = ( min_time, max_time ) )
		cmds.DeleteRigidBodies()
		
		
