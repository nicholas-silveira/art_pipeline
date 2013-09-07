import maya.cmds as cmds # @UnresolvedImport
import maya.mel as mel # @UnresolvedImport

import __init__ as oop_maya

def get_selected_attr():
	list_attr = []

	channel_box = mel.eval( 'global string $gChannelBoxName; $temp=$gChannelBoxName;' )

	selected_attr = cmds.channelBox( channel_box, q = True, sma = True )

	if selected_attr:
		for obj in cmds.ls( sl = True ):
			for attr in selected_attr:
				list_attr.append( '{0}.{1}'.format( obj, attr ) )

	else:
		oop_maya.warning( 'You must select attributes in the Channel Box!' )

	return list_attr