"""
All Pipeline Environment Paths

*Author:*
	* Nicholas Silveira, Nicholas.Silveira@gmail.com, Jul 21, 2013 4:54:22 PM
"""

import sys
import os



class Env_Paths():
	def __init__( self ):
		script_path = os.path.dirname( os.path.abspath( __file__ ) )
		script_path = os.path.dirname( script_path )
		self.pipeline_path = os.path.dirname( script_path )

	'''
	========================================================================
	---->  Global Pipeline Core Paths  <----
	========================================================================
	'''
	def core( self ):
		pipeline_paths = ['{0}\\core'.format( self.pipeline_path )]
		

		return pipeline_paths

	'''
	========================================================================
	---->  Maya 2013 Environment Paths  <----
	========================================================================
	'''
	def maya_2013( self ):
		#Import Maya paths
		maya_paths = ['{0}\\maya\\packages'.format( self.pipeline_path )]

		return maya_paths

	'''
	========================================================================
	---->  Maya 2014 Environment Paths  <----
	========================================================================
	'''
	def maya_2014( self ):
		#Import Maya paths
		maya_paths = ['{0}\\maya\\packages'.format( self.pipeline_path )]

		return maya_paths

	'''
	========================================================================
	---->  Maya 2014 Environment Paths  <----
	========================================================================
	'''
	def dcc( self ):
		#Import Maya paths
		dcc_paths = ['{0}\\dcc\\packages'.format( self.pipeline_path )]

		return dcc_paths
	
	'''
	========================================================================
	---->  Python Environment Paths  <----
	========================================================================
	'''
	def python( self ):
		#Import Python paths
		dcc_paths = ['{0}\\python\\packages'.format( self.pipeline_path )]

		return dcc_paths

	'''
	========================================================================
	---->  Add Paths  <----
	========================================================================
	'''
	def add_paths( self, software = None ):
		for path in self.get_paths( software ):
			if not path in sys.path:
				sys.path.append( path )

	'''
	========================================================================
	---->  Get Paths  <----
	========================================================================
	'''
	def get_paths( self, software = None, print_paths = True ):
		paths = []

		if software == 'maya_2013.0':
			maya_paths = self.maya_2013()

		elif software == 'maya_2014.0':
			maya_paths = self.maya_2014()
			
		core_paths = self.core()
		dcc_paths = self.dcc()
		python_paths = self.python()
		
		paths += maya_paths + core_paths + dcc_paths + python_paths
						
		if print_paths:			
			print '\nCore Pipeline Environment'
			for path in core_paths:
				print path
	
			print '\nMaya Pipeline Environment'
			for path in maya_paths:
				print path
	
			print '\nDCC Environment'
			for path in dcc_paths:
				print path
				
			print '\nPython Environment'
			for path in python_paths:
				print path

		return paths


