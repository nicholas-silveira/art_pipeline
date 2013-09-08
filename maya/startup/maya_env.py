"""
All Pipeline Environment Paths

*Author:*
	* Nicholas Silveira, Nicholas.Silveira@gmail.com, Jul 21, 2013 4:54:22 PM
"""

import sys

import core.const

PIPELINE_PATH = core.const.pipeline_path



'''
========================================================================
---->  Global Pipeline Core Paths  <----
========================================================================
'''
def core():
	pipeline_paths = ['{0}\\core'.format( PIPELINE_PATH )]
	

	return pipeline_paths

'''
========================================================================
---->  Maya 2013 Environment Paths  <----
========================================================================
'''
def maya_2013():
	# Import Maya paths
	maya_paths = ['{0}\\maya\\packages'.format( PIPELINE_PATH )]

	return maya_paths

'''
========================================================================
---->  Maya 2014 Environment Paths  <----
========================================================================
'''
def maya_2014():
	# Import Maya paths
	maya_paths = ['{0}\\maya\\packages'.format( PIPELINE_PATH ),
						'{0}\\maya\\shelves'.format( PIPELINE_PATH )]

	return maya_paths

'''
========================================================================
---->  Maya 2014 Environment Paths  <----
========================================================================
'''
def dcc():
	# Import Maya paths
	dcc_paths = ['{0}\\dcc\\packages'.format( PIPELINE_PATH )]

	return dcc_paths

'''
========================================================================
---->  Python Environment Paths  <----
========================================================================
'''
def python():
	# Import Python paths
	dcc_paths = ['{0}\\python\\packages'.format( PIPELINE_PATH )]

	return dcc_paths

'''
========================================================================
---->  Add Paths  <----
========================================================================
'''
def add_paths( software = None ):
	for path in get_paths( software ):
		if not path in sys.path:
			sys.path.append( path )

'''
========================================================================
---->  Get Paths  <----
========================================================================
'''
def get_paths( software = None, print_paths = True ):
	paths = []

	if software == 2013.0:
		maya_paths = maya_2013()

	elif software == 2014.0:
		maya_paths = maya_2014()
		
	core_paths = core()
	dcc_paths = dcc()
	python_paths = python()
	
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


