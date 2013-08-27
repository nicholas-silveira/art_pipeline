# Import Maya modules
import maya.cmds as cmds #@UnresolvedImport

import maya_dag



'''
========================================================================
---->  Maya Controller  <----
========================================================================
'''
class Maya_Controller():
	'''
	========================================================================
	---->  Creates Controller  <----
	========================================================================
	'''
	def __init__( self, name = '', shape = 'circle_curve', scale = 1, color = 'white' ):
		if shape == 'circle_curve':
			self.controller_dag = cmds.circle( nr = [0, 1, 0], r = 0.5 )[0]

		elif shape == 'square_curve':
			self.square_curve()

		elif shape == 'box_curve':
			self.box_curve()

		elif shape == 'diamond_curve':
			self.diamond_curve()

		if name == '':
			name = '{0}_controller'.format( shape )

		if self.controller_dag:
			self.controller_dag.rename( name )
			cmds.setAttr( '{0}.scale'.format( self.controller_dag.name() ), scale, scale, scale )
			cmds.makeIdentity( self.controller_dag.name(), a = True, t = True, r = True, s = True )
			cmds.delete( self.controller_dag.name(), ch = True )

			self.set_color( color )

	'''
	========================================================================
	---->  Builds Square Controller  <----
	========================================================================
	'''
	def square_curve( self ):
		cmds.curve( d = 1, p = [( 0.5, 0, -0.5 ),
											  ( 0.5, 0, 0.5 ),
											  ( -0.5, 0, 0.5 ),
											  ( -0.5, 0, -0.5 ),
											  ( 0.5, 0, -0.5 )],
											  k = [0, 1, 2, 3, 4] )

		self.controller_dag = maya_dag.DAG_Node()

	'''
	========================================================================
	---->  Builds Box Controller  <----
	========================================================================
	'''
	def box_curve( self ):
		cmds.curve( d = 1, p = [( 0.5, 0.5, 0.5 ), ( 0.5, 0.5, -0.5 ), ( -0.5, 0.5, -0.5 ),
											  ( -0.5, 0.5, 0.5 ), ( 0.5, 0.5, 0.5 ), ( 0.5, -0.5, 0.5 ),
											  ( -0.5, -0.5, 0.5 ), ( -0.5, 0.5, 0.5 ), ( 0.5, 0.5, 0.5 ),
											  ( 0.5, 0.5, -0.5 ), ( 0.5, -0.5, -0.5 ), ( 0.5, -0.5, 0.5 ),
											  ( -0.5, -0.5, 0.5 ), ( -0.5, 0.5, 0.5 ), ( -0.5, 0.5, -0.5 ),
											  ( -0.5, -0.5, -0.5 ), ( -0.5, -0.5, 0.5 ), ( 0.5, -0.5, 0.5 ),
											  ( 0.5, -0.5, -0.5 ), ( -0.5, -0.5, -0.5 )] )

		self.controller_dag = maya_dag.DAG_Node()

	'''
	========================================================================
	---->  Builds Diamond Controller  <----
	========================================================================
	'''
	def diamond_curve( self ):
		cmds.curve( d = 1, p = [( 0.5, 0, 0 ), ( 0, 0, -0.5 ), ( -0.5, 0, 0 ),
											  ( 0, 0, 0.5, ), ( 0, -0.5, 0 ), ( 0, 0, -0.5 ),
											  ( 0, 0.5, 0 ), ( -0.5, 0, 0 ), ( 0, -0.5, 0 ),
											  ( 0.5, 0, 0 ), ( 0, 0.5, 0 ), ( 0, 0, 0.5 ),
											  ( 0.5, 0, 0 )],
											  k = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12] )

		self.controller_dag = maya_dag.DAG_Node()

	'''
	========================================================================
	---->  Sets controller color  <----
	========================================================================
	'''
	def set_color( self, color ):
		cmds.setAttr( '{0}.overrideEnabled'.format( self.controller_dag.name() ), True )

		if color == 'white':
			cmds.setAttr( '{0}.overrideColor'.format( self.controller_dag.name() ), 16 )

		elif color == 'black':
			cmds.setAttr( '{0}.overrideColor'.format( self.controller_dag.name() ), 1 )

		elif color == 'purple':
			cmds.setAttr( '{0}.overrideColor'.format( self.controller_dag.name() ), 30 )

		elif color == 'blue':
			cmds.setAttr( '{0}.overrideColor'.format( self.controller_dag.name() ), 18 )

		else:
			return False

		return True
