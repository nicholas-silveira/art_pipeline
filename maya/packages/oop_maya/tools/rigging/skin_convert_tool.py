import maya.cmds as cmds # @UnresolvedImport

import oopmaya.core as oopmaya # @UnresolvedImport
reload( oopmaya )

import simulation_tool # @UnresolvedImport
reload( simulation_tool )



class Skin_Convert_Tool():
   def convert_mesh_to_joints( self, objects ):  
      mesh_joints = []    
      joints_dag = []
      
      cluster_joints = []
      cluster_data = {}
      
      meshes = oopmaya.get_object_type( objects, 'mesh' )
      cluster_handles = oopmaya.get_object_type( objects, 'cluster1Handle' )

      for mesh in meshes:
         cmds.select( cl = True )
         
         mesh_joints.append( cmds.joint( n = '{0}_jnt'.format( mesh ) ) )
         joint_dag = oopmaya.DAG_Node()
         joints_dag.append( joint_dag )
         
         cmds.parentConstraint( mesh, joint_dag.name() )
         
      for cluster_handle in cluster_handles:
         cluster_vert = oopmaya.get_cluster_verts( cluster_handle )
         
         if cluster_vert:
            mesh_shape = cmds.cluster( cluster_handle, geometry = True, q = True )
            mesh_transform = cmds.listRelatives( mesh_shape, parent = True )
            
            cluster_data[mesh_transform] = [cluster_handles, cluster_vert]
            
            cluster_joints.append( cmds.joint( n = '{0}_jnt'.format( cluster_handle ) ) )
            joint_dag = oopmaya.DAG_Node()
            joints_dag.append( joint_dag )
            
            cmds.parentConstraint( cluster_handle, joint_dag.name() )
      
      simulation_tool.Simulation_Tool().bake_sim( mesh_joints, cluster_joints )
      cmds.delete( objects, cn = True )
      
      for obj_dag, joint_dag in zip( meshes, joints_dag ):
         if obj_dag.name() in cluster_data:
            print 1
            
         obj_dag.parent_constraint( joint_dag )

