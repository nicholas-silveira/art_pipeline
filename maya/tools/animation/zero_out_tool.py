"""
Zero Out Tool - Zero's out all attributes in "Zero_Out_Set"

*Author:*
	* Nicholas Silveira, Nicholas.Silveira@gmail.com, Jul 21, 2013 12:25:16 PM
"""

import maya.cmds as cmds #@UnresolvedImport
import maya.OpenMaya as OpenMaya #@UnresolvedImport



'''
========================================================================
---->  Zero Out Tool  <----
========================================================================
'''
class Zero_Out_Tool():
	"""
	*Examples:* ::
	
		import zero_out_tool
		
		zero_out_tool.Zero_Out_Tool()
	"""
	def __init__( self, *args ):
		zero_out_set_name = 'Zero_Out_Set'
		selected = cmds.ls( sl = True )

		character_set_list = []

		if not selected:
			OpenMaya.MGlobal.displayError( "You can't select the same set!" )

		else:
			for controller in selected:
				namespace = controller.split( ':' )[:-1]
				namespace = ':'.join( namespace )

				zero_out_set = '{0}:{1}'.format( namespace, zero_out_set_name )
				if zero_out_set not in character_set_list:
					character_set_list.append( zero_out_set )

					if cmds.objExists( zero_out_set ):
							for attr in cmds.sets( zero_out_set, q = True ):
								if not cmds.getAttr( attr, cb = True ):
									cmds.setAttr( attr, 0 )
