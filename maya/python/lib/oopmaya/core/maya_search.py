import maya.cmds as cmds # @UnresolvedImport


def get_object_type( objects, types ):   
   shapes = cmds.listRelatives( objects, shapes = True )
   nodes = cmds.ls( shapes, type = types )
   transform_nodes = cmds.listRelatives( nodes, parent = True )
   
   return list( set( transform_nodes ) )

def get_cluster_set( cluster_handle ):
   cluster = cmds.listConnections( '{0}.worldMatrix[0]'.format( cluster_handle ) )
         
   if cluster:
      cluster_set = cmds.listConnections( '{0}.message'.format( cluster[0] ) )
      
      if cluster_set:
         return cluster_set[0]

   return False

def get_cluster_verts( cluster_handle ):
   cluster = cmds.listConnections( '{0}.worldMatrix[0]'.format( cluster_handle ) )
         
   if cluster:
      cluster_set = cmds.listConnections( '{0}.message'.format( cluster[0] ) )
      
      if cluster_set:
         return cmds.sets( union = cluster_set[0] )

   return False
