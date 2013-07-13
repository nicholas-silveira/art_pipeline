import sys
import os



class Env_Paths():
	def __init__(self):
		script_path = os.path.dirname(os.path.abspath(__file__))
		self.pipeline_path = os.path.dirname(script_path)

	def mobu_2013(self):
		#Import Mobu paths
		mobu_paths = ['{0}\\mobu\\libs_2013'.format(self.pipeline_path),
					  '{0}\\mobu\\tools'.format(self.pipeline_path)]
					  
		return mobu_paths
		
	def mobu_2014(self):
		#Import Mobu paths
		mobu_paths = ['{0}\\mobu\\libs_2014'.format(self.pipeline_path),
					  '{0}\\mobu\\tools'.format(self.pipeline_path)]
					  
		return mobu_paths
		
	def dcc_2013(self):
		#Import DCC paths
		dcc_paths = ['{0}\\dcc\\libs_2013'.format(self.pipeline_path)]
		
		return dcc_paths
		
	def dcc_2014(self):
		#Import DCC paths
		dcc_paths = ['{0}\\dcc\\libs_2014'.format(self.pipeline_path)]
		
		return dcc_paths
		
	def load_paths(self, software = None):
		mobu_paths = []
		dcc_paths = []
					
		if software == 'mobu_2013':
			mobu_paths = self.mobu_2013()
			dcc_paths = self.dcc_2013()
			
		elif software == 'mobu_2014':
			mobu_paths = self.mobu_2014()
			dcc_paths = self.dcc_2014()
	
		for path in mobu_paths:
			sys.path.append(path)

		for path in dcc_paths:
			sys.path.append(path)