
import maya.mel as mel # @UnresolvedImport



def maya_version():
   return mel.eval( 'getApplicationVersionAsFloat' )