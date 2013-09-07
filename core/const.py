import os



core_path = os.path.dirname( os.path.abspath( __file__ ) ).replace( '\\', '/' )
pipeline_path = os.path.dirname( core_path )

oop_maya_path = pipeline_path + '/maya/packages/oop_maya'

oop_maya_core_path = oop_maya_path + '/core'
oop_maya_tools_pth = oop_maya_path + '/tools'

oop_dcc_path = pipeline_path + '/dcc/packages/oop_dcc'

oop_dcc_core_path = oop_dcc_path + '/core'
oop_dcc_tools_path = oop_dcc_path + '/tools'
