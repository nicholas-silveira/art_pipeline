import maya.OpenMaya as OpenMaya #@UnresolvedImport
import maya.cmds as cmds #@UnresolvedImport




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
		import no_flip_pole_vector as nfpv
	
		exampleA_grp = nfpv.DAG_Node( cmds.group( n = 'exampleA_grp', em = True ) )
		exampleB_grp = nfpv.DAG_Node( cmds.group( n = 'exampleB_grp', em = True ) )
		
		exampleA_grp.set_parent(exampleB_grp)
		print exampleA_grp.parent()
		print exampleA_grp.name()
	"""
	def __init__( self, node = None ):
		if not node:
			node = cmds.ls( sl = True )[0]
		
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
	---->  DAG Full Path Name  <----
	========================================================================
	'''
	def short_name( self ):
		"""
		*Returns:*
			* ``node_name`` Returns DAG's full path name.
		"""
		node_short_name = self.name().split( '|' )[-1]

		return node_short_name

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
