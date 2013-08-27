
import sys

import maya.OpenMaya as OpenMaya #@UnresolvedImport
import maya.cmds as cmds #@UnresolvedImport


def message( message ):
	sys.stdout.write( '// Result: {0}'.format( message ) )

def warning( message ):
	cmds.warning( message )

def error( message ):
	OpenMaya.MGlobal.displayError( message )
