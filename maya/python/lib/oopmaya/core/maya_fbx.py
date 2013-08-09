import maya.cmds as cmds
import maya.mel as mel

import utilities.maya_message as maya_message



class FBX_Exporter():
	def convert_to_joints( self ):
		pass

	def merge_mesh( self ):
		pass

	def export_mesh( self, file_path ):
		file_path = file_path.replace( '\\', '/' )
	
		mel.eval( "FBXProperty Export|IncludeGrp|Geometry|SmoothingGroups -v true;" )
		mel.eval( "FBXProperty Export|IncludeGrp|Geometry|expHardEdges -v false;" )
		mel.eval( "FBXProperty Export|IncludeGrp|Geometry|TangentsandBinormals -v true;" )
		mel.eval( "FBXProperty Export|IncludeGrp|Geometry|SmoothMesh -v true;" )
		mel.eval( "FBXProperty Export|IncludeGrp|Geometry|SelectionSet -v false;" )
		mel.eval( "FBXProperty Export|IncludeGrp|Geometry|BlindData -v false;" )
		mel.eval( "FBXProperty Export|IncludeGrp|Geometry|AnimationOnly -v false;" )
		mel.eval( "FBXProperty Export|IncludeGrp|Geometry|GeometryNurbsSurfaceAs -v NURBS;" )
		mel.eval( "FBXProperty Export|IncludeGrp|Geometry|Instances -v false;" )
		mel.eval( "FBXProperty Export|IncludeGrp|Geometry|ContainerObjects -v true;" )
		mel.eval( "FBXProperty Export|IncludeGrp|Geometry|Triangulate -v false;" )

		mel.eval( "FBXExportInputConnections -v false;" )
		mel.eval( "FBXExportInAscii -v false;" )

		mel.eval( 'FBXExport -f "{0}" -s;'.format( file_path ) )
		
		maya_message.message( 'Export finished!' )

	def export_skin( self, file_path ):
		file_path = file_path.replace( '\\', '/' )

		mel.eval( "FBXExportAnimationOnly -v false;" )
		mel.eval( "FBXExportSkins -v true;" )
		mel.eval( "FBXExportScaleFactor 1.0" )

		mel.eval( "FBXExportInputConnections -v false;" )
		mel.eval( "FBXExportInAscii -v false;" )

		mel.eval( 'FBXExport -f "{0}" -s;'.format( file_path ) )
		
		maya_message.message( 'Export finished!' )

	def export_animation( self, file_path ):
		file_path = file_path.replace( '\\', '/' )
		
		start = str( cmds.playbackOptions( ast = True, q = True ) )
		end = str( cmds.playbackOptions( aet = True, q = True ) )

		mel.eval( "FBXExportBakeComplexAnimation -v true;" )

		mel.eval( 'FBXExportBakeComplexStart -v ' + start + ';' )
		mel.eval( 'FBXExportBakeComplexEnd -v ' + end + ';' )
			
		mel.eval( "FBXExportInputConnections -v false;" )
		mel.eval( "FBXExportInAscii -v false;" )

		mel.eval( 'FBXExport -f "{0}" -s;'.format( file_path ) )
		
		maya_message.message( 'Export finished!' )
