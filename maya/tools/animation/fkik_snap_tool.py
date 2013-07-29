"""
FKIK Snap Tool - Looks for controllers with stamped attributes and snaps fk to ik or ik to fk

*Author:*
	* Nicholas, Nicholas@gmail.com, Jul 21, 2013 12:28:31 PM
"""
import maya.cmds as cmds #@UnresolvedImport
import maya.OpenMaya as OpenMaya #@UnresolvedImport

VERSION = 1.0



'''
========================================================================
---->  FKIK Snap Tool  <----
========================================================================
'''
class FKIK_Snap_Tool():
	"""
	*Examples:* ::
	
		import fkik_snap_tool
		
		# Select a controller that has fkik snap attributes
		fkik_snap_tool.FKIK_Snap_Tool()
	"""
	def __init__( self, *args ):
		self.get_global()

		selected = cmds.ls( sl = True )

		controller_list = {}
		opposite_set = None
		auto_key = cmds.autoKeyframe( st = True, q = True )

		if auto_key:
			cmds.autoKeyframe( st = False )

		if selected:

			for obj in selected:
				obj_set_attr = '{0}.{1}'.format( obj, self.set_parent_str )

				if cmds.objExists( obj_set_attr ):
					obj_set = cmds.listConnections( obj_set_attr )

					if obj_set:
						obj_set = obj_set[0]

						opposite_set_attr = '{0}.{1}'.format( obj_set, self.opposite_set_str )

						if cmds.objExists( opposite_set_attr ):
							opposite_set = cmds.listConnections( opposite_set_attr )

						if opposite_set:
							opposite_set = opposite_set[0]

							for controller in cmds.sets( opposite_set, q = True ):
								controller_order_attr = '{0}.{1}'.format( controller, self.snap_order_attr )

								if cmds.objExists( controller_order_attr ):
									controller_order = cmds.getAttr( controller_order_attr )

									if controller_order:
										controller_order = int( controller_order[0] )

										controller_list[controller_order] = controller

			for controller in controller_list.values():

				obj_snap_attr = '{0}.{1}'.format( controller, self.snap_parent_str )

				print obj_snap_attr

				if cmds.objExists( obj_snap_attr ):
					snap_obj = cmds.listConnections( obj_snap_attr )

					if snap_obj:
						snap_obj = snap_obj[0]

						tra = cmds.xform( snap_obj, ws = True, rp = True, q = True )
						rot = cmds.xform( snap_obj, ws = True, ro = True, q = True )

						try:
							cmds.xform( controller, ws = True, t = tra )

						except:
							pass

						try:
							cmds.xform( controller, ws = True, ro = rot )

						except:
							try:
								rot_x = cmds.getAttr( '{0}.rotateX'.format( snap_obj ) )
								cmds.setAttr( '{0}.rotateX'.format( controller ), rot_x )

							except:
								pass

							try:
								rot_x = cmds.getAttr( '{0}.rotateY'.format( snap_obj ) )
								cmds.setAttr( '{0}.rotateY'.format( controller ), rot_x )

							except:
								pass

							try:
								rot_x = cmds.getAttr( '{0}.rotateZ'.format( snap_obj ) )
								cmds.setAttr( '{0}.rotateZ'.format( controller ), rot_x )

							except:
								pass

			if not opposite_set:
				OpenMaya.MGlobal.displayError( "Can not find FKIK Snap on selected controller!" )

			else:

				switch_attr = cmds.listConnections( '{0}.{1}'.format( opposite_set, self.switch_parent_str ), plugs = True )[0]

				current_time = cmds.currentTime( query = True )
				cmds.setKeyframe( switch_attr, time = current_time - 1 )
				cmds.setKeyframe( cmds.sets( obj_set, q = True ), cmds.sets( opposite_set, q = True ) )

				if cmds.getAttr( switch_attr ) == 0:
					cmds.setAttr( switch_attr, 1 )

				elif cmds.getAttr( switch_attr ) == 1:
					cmds.setAttr( switch_attr, 0 )

				cmds.setKeyframe( switch_attr )

		else:
			OpenMaya.MGlobal.displayError( "You need to select a controller!" )

		if auto_key:
			cmds.autoKeyframe( st = True )

		cmds.select( cl = True )

	'''
	========================================================================
	---->  Get Globals  <----
	========================================================================
	'''
	def get_global( self ):
		"""
		*Author:*
			* Nicholas Silveira, Nicholas.Silveira@gmail.com, Jul 21, 2013 12:36:16 PM
		"""
		self.main_set = 'fkik_snap_set'

		self.snap_order_attr = 'snap_order'

		self.opposite_set_str = 'opposite_set'
		self.set_parent_str = 'set_parent'
		self.set_child_str = 'set_child'

		self.snap_parent_str = 'snap_parent'
		self.snap_child_str = 'snap_child'

		self.switch_parent_str = 'switch_parent'
