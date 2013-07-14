import sys

pipeline_dir = ''

sys.path.append( pipeline_dir )
sys.path.append( '{0}/maya'.format( pipeline_dir ) )

import startup.maya_setup as maya_setup
maya_setup.Setup()