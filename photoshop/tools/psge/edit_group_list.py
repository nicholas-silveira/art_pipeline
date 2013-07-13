'''Import Modules'''
import sys
import os

import PyQt4.QtCore
import PyQt4.uic
import PyQt4.QtGui

'''Import Custom Modules'''
import utilities

'''Global Variables'''
ICON_PATH = 'ui/icons/'
DATA_PATH = 'data/'

GROUPS_FILE = 'groups.data'

UI_LOCATION = 'ui/edit_group_list.ui'
GROUPS_LOCATION = '{0}{1}'.format( DATA_PATH, GROUPS_FILE )



try:
    ui_object, base_class = PyQt4.uic.loadUiType( UI_LOCATION )

except:
    pass


class Edit_Group_List( base_class, ui_object ):
    def __init__( self, parent = None ):
        super( base_class, self ).__init__( parent )
        self.setupUi( self )

        self.connect( self.addGroup_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), self.add_group )
        self.connect( self.removeGroup_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), self.remove_group )

        self.setWindowIcon( PyQt4.QtGui.QIcon( '{0}psge_icon.ico'.format( ICON_PATH ) ) )

        self.tool_setup()



    '''
    ========================================================================
    ---->  Procedure sets up the group list ui  <----
    ========================================================================
    '''
    def tool_setup( self ):
        self.load_group_list()



    '''
    ========================================================================
    ---->  Procedure parses groups.data and adds data to table  <----
    ========================================================================
    '''
    def load_group_list( self ):
        if os.path.exists( DATA_PATH ):
            group_list = utilities.load_json_file( GROUPS_LOCATION )

            for group in group_list:
                utilities.add_table_item( self.group_list_table, [group, group_list[group]] )



    '''
    ========================================================================
    ---->  Procedure adds new group to table and to groups.data  <----
    ========================================================================
    '''
    def add_group ( self ):
        group_name = str( self.groupName_line.text() )
        suffix_name = str( self.groupSuffix_line.text() )

        if group_name != '':
            if suffix_name != '':
                utilities.add_table_item( self.group_list_table, [group_name, suffix_name] )

        group_list = utilities.load_json_file( GROUPS_LOCATION )
        group_list[group_name] = suffix_name

        utilities.write_json_file( GROUPS_LOCATION, group_list )



    '''
    ========================================================================
    ---->  Procedure removes group from table and from groups.data  <----
    ========================================================================
    '''
    def remove_group ( self ):
        remove_items = utilities.get_selected_table_items( self.group_list_table )


        group_list = utilities.load_json_file( GROUPS_LOCATION )

        for item in remove_items:
            if group_list.has_key( item ):
                del group_list[ item ]

        utilities.write_json_file( GROUPS_LOCATION, group_list )
        utilities.remove_selected_table_row( self.group_list_table )


'''
========================================================================
---->  Runs main class  <----
========================================================================
'''
if __name__ == '__main__':
    app = PyQt4.QtGui.QApplication( sys.argv )
    main_ui = Edit_Group_List()
    main_ui.show()
    sys.exit( app.exec_() )
