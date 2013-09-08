
import maya.mel as mel # @UnresolvedImport



def get_maya_version():
   return mel.eval( 'getApplicationVersionAsFloat;' )
