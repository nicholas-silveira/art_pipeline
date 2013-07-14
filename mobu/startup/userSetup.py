import sys

pipeline_dir = ''

sys.path.append( pipeline_dir )
sys.path.append( '{0}/mobu'.format( pipeline_dir ) )

import startup.mobu_setup as mobu_setup
mobu_setup.Setup()