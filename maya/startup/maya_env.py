import sys
import os



class Env_Paths():
	def __init__( self ):
		script_path = os.path.dirname( os.path.abspath( __file__ ) )
		script_path = os.path.dirname( script_path )
		self.pipeline_path = os.path.dirname( script_path )

	def maya_2013( self ):
		#Import Maya paths
		maya_paths = ['{0}\\maya\\libs_2013'.format( self.pipeline_path ),
					  	  '{0}\\maya\\tools'.format( self.pipeline_path )]

		return maya_paths

	def maya_2014( self ):
		#Import Maya paths
		maya_paths = ['{0}\\maya\\libs_2014'.format( self.pipeline_path ),
					  	  '{0}\\maya\\tools'.format( self.pipeline_path )]

		return maya_paths

	def dcc_2013( self ):
		#Import DCC paths
		dcc_paths = ['{0}\\dcc\\libs_2013'.format( self.pipeline_path )]

		return dcc_paths

	def dcc_2014( self ):
		#Import DCC paths
		dcc_paths = ['{0}\\dcc\\libs_2014'.format( self.pipeline_path ),
						  '{0}\\dcc\\modules'.format( self.pipeline_path )]

		return dcc_paths

	def add_paths( self, software = None ):
		for path in self.get_paths( software ):
			sys.path.append( path )

	def get_paths( self, software = None ):
		maya_paths = []
		dcc_paths = []

		if software == 'maya_2013.0':
			maya_paths = self.maya_2013()
			dcc_paths = self.dcc_2013()

		elif software == 'maya_2014.0':
			maya_paths = self.maya_2014()
			dcc_paths = self.dcc_2014()

		print 'Maya Environment'
		for path in maya_paths:
			print path

		print '\nDCC Environment'
		for path in dcc_paths:
			print path

		return maya_paths + dcc_paths






