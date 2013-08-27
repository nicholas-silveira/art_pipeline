'''
========================================================================
========================================================================
NS Photoshop Group Exporter

* Description: *
    * The NS Photoshop Group Exporter allows you to export multiple photoshop
      files based off of certain group names.

* Author: *
    * Nicholas Silveira, Nicholas.Silveira@gmail.com, Feb 2, 2013
    
* Thanks *
    * Adam Pletcher  - How to implement Python into Photoshop
    * Peter Hanshaw  - How to save out Photoshop TGAs
    * Yasin Uludag   - Free Qt Dark Orange stylesheet
    * Adam Whitcroft - Free icons
========================================================================
========================================================================
'''

'''Import System Modules'''
import sys
import os

'''Import PyQt4 Modules'''
import PyQt4.QtCore
import PyQt4.uic
import PyQt4.QtGui

'''Import Extra Modules'''
import functools
import win32com.client
import win32ui

'''Import Custom Modules'''
import utilities
import edit_group_list



'''Global Variables'''
VERSION = 1.0

ICON_PATH = 'ui/icons/'
DATA_PATH = 'data/'

STARTUP_FILE = 'startup.data'
GROUPS_FILE = 'groups.data'

UI_LOCATION = 'ui/photoshop_group_exporter.ui'
STARTUP_LOCATION = '{0}{1}'.format( DATA_PATH, STARTUP_FILE )
GROUPS_LOCATION = '{0}{1}'.format( DATA_PATH, GROUPS_FILE )



try:
    ui_object, base_class = PyQt4.uic.loadUiType( UI_LOCATION )

except:
    pass

class Photoshop_Group_Exporter( base_class, ui_object ):
    '''
    ========================================================================
    ---->  Connects, adds icons, and shows ui  <----
    ========================================================================
    '''
    def __init__( self, parent = None ):
        '''Parent ui'''
        super( base_class, self ).__init__( parent )
        self.main_ui = self

        '''Forces main window to stay on top and sets up ui'''
        self.setupUi( self )

        '''Runs ui tool steup'''
        self.tool_setup()

        '''Main menu tittle and icon'''
        self.setWindowTitle ( PyQt4.QtCore.QString( 'NS Photoshop Group Exporter v{0}'.format( VERSION ) ) )
        self.setWindowIcon( PyQt4.QtGui.QIcon( '{0}psge_icon.ico'.format( ICON_PATH ) ) )

        '''When ui has focus'''
        PyQt4.QtCore.QObject.connect( app, PyQt4.QtCore.SIGNAL( "focusChanged(QWidget *, QWidget *)" ), self.focus_changed )

        '''Connect procedures to buttons'''
        self.connect( self.window_stay_on_top_action, PyQt4.QtCore.SIGNAL( 'changed()' ), self.set_project_startup )

        self.connect( self.project_combo, PyQt4.QtCore.SIGNAL( 'currentIndexChanged( QString )' ), self.set_project_startup )

        self.connect( self.projectAdd_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), self.add_project )
        self.connect( self.projectRemove_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), self.remove_project )

        self.connect( self.photoshopDir_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( self.set_photoshop_dir, set_dir = True ) )
        self.connect( self.projectDir_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), self.set_project_dir )
        self.connect( self.browseDir_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), self.set_browse_dir )
        self.connect( self.openFolder_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), self.open_folder )

        self.connect( self.groupList_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), self.edit_group_list )

        self.connect( self.lowRes_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( self.set_resolution, 1 ) )
        self.connect( self.highRes_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( self.set_resolution, 2 ) )

        self.connect( self.w32_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( utilities.set_line, self.width_line, 32 ) )
        self.connect( self.w64_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( utilities.set_line, self.width_line, 64 ) )
        self.connect( self.w128_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( utilities.set_line, self.width_line, 128 ) )
        self.connect( self.w256_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( utilities.set_line, self.width_line, 256 ) )
        self.connect( self.w512_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( utilities.set_line, self.width_line, 512 ) )
        self.connect( self.w1024_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( utilities.set_line, self.width_line, 1024 ) )
        self.connect( self.w2048_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( utilities.set_line, self.width_line, 2048 ) )

        self.connect( self.h32_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( utilities.set_line, self.height_line, 32 ) )
        self.connect( self.h64_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( utilities.set_line, self.height_line, 64 ) )
        self.connect( self.h128_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( utilities.set_line, self.height_line, 128 ) )
        self.connect( self.h256_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( utilities.set_line, self.height_line, 256 ) )
        self.connect( self.h512_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( utilities.set_line, self.height_line, 512 ) )
        self.connect( self.h1024_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( utilities.set_line, self.height_line, 1024 ) )
        self.connect( self.h2048_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( utilities.set_line, self.height_line, 2048 ) )

        self.connect( self.flip_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), functools.partial( self.flip_line_values, self.width_line, self.height_line ) )

        self.connect( self.export_button, PyQt4.QtCore.SIGNAL( 'clicked()' ), self.export )

        '''Connect icons to buttons'''
        add_green_icon = PyQt4.QtGui.QIcon( '{0}/add_green_icon.png'.format ( ICON_PATH ) )
        remove_red_icon = PyQt4.QtGui.QIcon( '{0}/remove_red_icon.png'.format ( ICON_PATH ) )
        flip_icon = PyQt4.QtGui.QIcon( '{0}/flip_icon.png'.format ( ICON_PATH ) )

        self.projectAdd_button.setIcon( add_green_icon )
        self.projectRemove_button.setIcon( remove_red_icon )
        self.flip_button.setIcon( flip_icon )

        self.project_cleanup()



    '''
    ========================================================================
    ---->  Procedure compares the recent ui data to the current ui data. If they
    don't match up the ui will update  <----
    ========================================================================
    '''
    def focus_changed( self, recent_focus, current_focus ):
        self.connect_photoshop()

        if current_focus == None:
            self.save_recent_list = self.update_photoshop_grps()

        else:
            self.save_current_list = self.update_photoshop_grps()

        try:
            if self.save_recent_list != self.save_current_list:
                self.update_photoshop_grps( refresh = True )
                self.save_recent_list = self.save_current_list

        except:
            pass

        try:
            ps_name = self.ps_app.ActiveDocument.name
            ps_path = self.ps_app.ActiveDocument.path
            ps_location = '{0}{1}'.format( ps_path, ps_name )

            ps_location = ps_location.replace( "\\", '/' )

            if current_focus == None:
                self.save_recent_ps = ps_location
                self.save_recent_groups = utilities.load_json_file( GROUPS_LOCATION )

            else:
                self.save_current_ps = ps_location
                self.save_current_groups = utilities.load_json_file( GROUPS_LOCATION )

        except:
            pass

        try:

            if self.save_recent_ps != self.save_current_ps:
                self.update_table()
                self.save_recent_ps = self.save_current_ps

            if self.save_recent_groups != self.save_current_groups:
                self.update_table()
                self.save_recent_groups = self.save_current_groups

        except:
            pass



    '''
    ========================================================================
    ---->  Procedure setups up ui (loads project directory and connects tool
    to Photoshop)  <----
    ========================================================================
    '''
    def tool_setup( self ):
        self.load_projects()
        self.connect_photoshop()
        self.group_list_setup()
        self.update_photoshop_grps( refresh = True )
        self.update_table()



    '''
    ========================================================================
    ---->  Procedure loads in project data into the ui  <----
    ========================================================================
    '''
    def load_projects( self ):
        try:
            project_startup = utilities.load_json_file( STARTUP_LOCATION )
            utilities.window_stay_on_top( project_startup['window_stay_on_top'], self.main_ui )
            self.window_stay_on_top_action.setChecked( project_startup['window_stay_on_top'] )

        except:
            pass

        if os.path.exists( DATA_PATH ):
            for data_file in os.listdir( DATA_PATH ):
                try:
                    data = data_file.split( '.' )[-1]

                    if data == 'project':
                        project_name = data_file.split( '.' )[:-1][0]
                        utilities.add_remove_combo( self.project_combo, add = True, data = project_name )

                except:
                    pass

        if os.path.exists( STARTUP_LOCATION ):
            try:
                project_number = utilities.search_combo_items( self.project_combo, project_startup['main_project'] )
                self.project_combo.setCurrentIndex( project_number )

            except:
                pass

        self.set_project_dir()



    '''
    ========================================================================
    ---->  Connects this ui to the current Photoshop file  <----
    ========================================================================
    '''
    def connect_photoshop( self ):
        try:
            if win32ui.FindWindow( 'Photoshop', None ) != None:
                try:
                    '''COM dispatch for Photoshop'''
                    self.ps_app = win32com.client.Dispatch( 'Photoshop.Application' )
                    self.options = win32com.client.Dispatch( 'Photoshop.TargaSaveOptions' )

                    self.options.Resolution = 24
                    self.options.AlphaChannels = False
                    self.options.RLECompression = False
                    self.ps_app.Preferences.RulerUnits = 1

                except:
                    self.message_report( error_level = 2,
                                         message = "Cannot connect to Photoshop! Make sure all Photoshop option windows are closed!" )

        except:
            self.message_report( error_level = 2,
                                     message = "Cannot find a Photoshop window to connect!" )



    '''
    ========================================================================
    ---->  Procedure searches for group data file if False then it will
    create a new defalt file  <----
    ========================================================================
    '''
    def group_list_setup( self ):
        utilities.get_directory( DATA_PATH )

        if not os.path.exists( GROUPS_LOCATION ):
            project_data = {'diffuse': '_d',
                            'specular': '_s',
                            'normal': '_n',
                            'bump': '_b',
                            'occlusion': '_o',
                            'luminous': '_l'}

            utilities.write_json_file( GROUPS_LOCATION, project_data )



    '''
    ========================================================================
    ---->  Procedure updates table data by parsing current project file  <----
    ========================================================================
    '''
    def update_table( self ):
        group_data = None

        try:
            ps_name = self.ps_app.ActiveDocument.name
            ps_path = self.ps_app.ActiveDocument.path
            ps_path = ps_path.replace( "\\", '/' )

            photoshop_file = '{0}{1}'.format( ps_path, ps_name )

            project_name = str( self.project_combo.currentText() )

            if os.path.exists( '{0}{1}.project'.format( DATA_PATH, project_name ) ):
                group_data = self.get_photoshop_group_data( '{0}{1}.project'.format( DATA_PATH, project_name ), photoshop_file )

        except:
            pass

        if group_data != None:
            low_data = group_data[0]
            high_data = group_data[1]

            rows = self.group_table.rowCount()

            for row in range( rows ):
                for low in low_data:
                    if str( self.group_table.item( row, 0 ).text() ) == low:
                        if low_data[low][0] != None:
                            low_item = str( '{0}x{1}'.format( low_data[low][0], low_data[low][1] ) )
                            low_item = PyQt4.QtGui.QTableWidgetItem( low_item )
                            self.group_table.setItem ( row, 1, low_item )
                            break

                for high in high_data:
                    if str( self.group_table.item( row, 0 ).text() ) == high:
                        if high_data[low][0] != None:
                            high_item = str( '{0}x{1}'.format( high_data[low][0], high_data[low][1] ) )
                            high_item = PyQt4.QtGui.QTableWidgetItem( high_item )
                            self.group_table.setItem ( row, 2, high_item )
                            break



    '''
    ========================================================================
    ---->  Procedure updates photoshop groups in tabale  <----
    ========================================================================
    '''
    def update_photoshop_grps( self, refresh = False ):
        export_grps = []
        export_list = utilities.load_json_file( GROUPS_LOCATION )

        if refresh:
            self.group_table.setRowCount( 0 )

        try:
            layer_grps = self.ps_app.ActiveDocument.LayerSets

            self.message_report( error_level = 0,
                                     message = "Exporter successfully connected to Photoshop!" )

            if ( len( layer_grps ) > 0 ):
                for grp in layer_grps:
                    grp_name = grp.Name

                    if ( grp_name in export_list ):
                            export_grps.append( grp_name )

                            if refresh:
                                utilities.add_table_item( self.group_table, [grp_name] )
                                self.update_table()

            else:
                self.message_report( error_level = 1,
                                     message = "Can't find any Photoshop groups!" )

        except:
            self.message_report( error_level = 1,
                                 message = "Make sure there is a Photoshop file is open!" )

        return export_grps



    '''
    ========================================================================
    ---->  Procedure creates a file with the new project data  <----
    ========================================================================
    '''
    def create_project_file( self, project_name, project_dir ):

        project_data = {'project': project_name, 'project_directory' : str( project_dir ), 'saved_files': [None]}
        utilities.write_json_file( '{0}{1}.project'.format( DATA_PATH, project_name ), project_data )

        self.set_project_startup()



    '''
    ========================================================================
    ---->  Procedure creates a project data file and adds the project directory  <----
    ========================================================================
    '''
    def add_project( self ):
        project_name = str( PyQt4.QtGui.QInputDialog.getText( self, 'Input Dialog', 'Project Name:' )[0] )  # @UndefinedVariable
        existing_projects = utilities.get_combo_items( self.project_combo )

        if any( i in project_name for i in existing_projects ) == False:
            if project_name != '':
                project_dir = PyQt4.QtGui.QFileDialog.getExistingDirectory( self, 'Set Project Folder' )

                if project_dir != '':
                    utilities.add_remove_combo( self.project_combo, add = True, data = project_name )

                    project_dir = project_dir.replace( "\\", '/' )


                    self.create_project_file( project_name, project_dir )
                    utilities.set_line( self.dir_line, '{0}/'.format( project_dir ) )

                    self.message_report( error_level = 0,
                                                 message = "Project is set to {0}".format( project_dir ) )

                else:
                    self.message_report( error_level = 2,
                                                     message = "Name is invalid!" )

            else:
                self.message_report( error_level = 2,
                                                 message = "Directory is invalid!" )

        else:
                self.message_report( error_level = 2,
                                                 message = "This project already exists!" )



    '''
    ========================================================================
    ---->  Procedure removes project from ui and deletes the file  <----
    ========================================================================
    '''
    def remove_project( self ):
        project_name = str( self.project_combo.currentText() )

        if project_name != "":
            dialog_value = utilities.yes_no_dialog( self, 'Delete Project', 'Are you sure you want to remove {0} project?'.format( project_name ) )

            if dialog_value:
                project_file = '{0}{1}.project'.format( DATA_PATH, project_name )

                if os.path.isfile( project_file ):
                    try:
                        os.remove( project_file )

                    except:
                        pass

                    utilities.add_remove_combo( self.project_combo, remove = True )



    '''
    ========================================================================
    ---->  Procedure changes a startup file saving off the ui's preferences  <----
    ========================================================================
    '''
    def set_project_startup( self ):
        self.project_cleanup()

        project_name = str( self.project_combo.currentText() )

        utilities.window_stay_on_top( self.window_stay_on_top_action.isChecked(), self.main_ui )
        self.main_ui.show()

        try:
            utilities.window_stay_on_top( self.window_stay_on_top_action.isChecked(), self.group_ui )
            self.group_ui.show()

        except:
            pass

        project_data = {'main_project': project_name, 'window_stay_on_top': self.window_stay_on_top_action.isChecked ()}
        utilities.write_json_file( STARTUP_LOCATION, project_data )



    '''
    ========================================================================
    ---->  Procedure runs through all files in the data folders and if PSD's
    arn't found the PSD data will be removed from project  <----
    ========================================================================
    '''
    def project_cleanup( self ):
        if os.path.exists( DATA_PATH ):
            for data_file in os.listdir( DATA_PATH ):
                try:
                    data = data_file.split( '.' )[-1]

                    if data == 'project':
                        project_data = utilities.load_json_file( '{0}{1}'.format( DATA_PATH, data_file ) )

                        project_count = 0

                        for project in project_data['saved_files']:
                            if not os.path.exists( project['photoshop_file'] ):
                                project_data['saved_files'].pop( project_count )

                                project_count += -1

                            project_count += 1

                        utilities.write_json_file( '{0}{1}'.format( DATA_PATH, data_file ), project_data )
                except:
                    pass



    '''
    ========================================================================
    ---->  Procedure looks at current project directory and sets the
    QlistWidget  <----
    ========================================================================
    '''
    def set_project_dir( self ):
        project_name = str( self.project_combo.currentText() )

        if os.path.exists( '{0}{1}.project'.format( DATA_PATH, project_name ) ):
            directory = utilities.get_project_directory( '{0}{1}.project'.format( DATA_PATH, project_name ) )
            utilities.set_line( self.dir_line, '{0}/'.format( directory ) )

        else:
            self.message_report( error_level = 2,
                                 message = "Can't find current project!" )



    '''
    ========================================================================
    ---->  Procedure looks at current Photoshop file directory and sets the
    QlistWidget  <----
    ========================================================================
    '''
    def set_photoshop_dir( self, set_dir = False ):
        try:
            get_ps_dir = self.ps_app.ActiveDocument.path[:-1]
            get_ps_dir = get_ps_dir.replace( "\\", '/' )

            self.message_report( error_level = 0,
                                     message = "Exporter successfully connected to Photoshop!" )

        except:
            get_ps_dir = ''
            self.message_report( error_level = 2,
                                 message = "Can't find current Photoshop Directory. Make Sure to save the current Photoshop file!" )

        if set_dir:
            if get_ps_dir != '':
                utilities.set_line( self.dir_line, '{0}/'.format( get_ps_dir ) )

        return get_ps_dir



    '''
    ========================================================================
    ---->  Procedure browses and sets the QlistWidget  <----
    ========================================================================
    '''
    def set_browse_dir( self ):
        export_dir = str( self.dir_line.text() )

        browse_dir = PyQt4.QtGui.QFileDialog.getExistingDirectory( self, 'Set Project Folder', export_dir )
        browse_dir = browse_dir.replace( "\\", '/' )

        if browse_dir != '':
            utilities.set_line( self.dir_line, '{0}/'.format( browse_dir ) )



    '''
    ========================================================================
    ---->  Procedure opens current directory  <----
    ========================================================================
    '''
    def open_folder( self ):
        export_dir = str( self.dir_line.text() )

        if os.path.exists( export_dir ):
            os.startfile( export_dir )



    '''
    ========================================================================
    ---->  Procedure sets the passed column resolution data  <----
    ========================================================================
    '''
    def set_resolution( self, column ):
        sel_rows = self.group_table.selectionModel().selectedRows()

        width = str( self.width_line.text() )
        height = str( self.height_line.text() )

        for row in sel_rows:
            item = PyQt4.QtGui.QTableWidgetItem( '{0}x{1}'.format( width, height ) )
            self.group_table.setItem ( row.row(), column, item )



    '''
    ========================================================================
    ---->  Procedure shows Edit_Group_List.ui  <----
    ========================================================================
    '''
    def edit_group_list( self ):
        self.group_ui = edit_group_list.Edit_Group_List()
        try:
            project_startup = utilities.load_json_file( STARTUP_LOCATION )
            utilities.window_stay_on_top( project_startup['window_stay_on_top'], self.group_ui )
        except:
            pass

        self.group_ui.show()



    '''
    ========================================================================
    ---->  Procedure flips two values from given QLineEdit  <----
    ========================================================================
    '''
    def flip_line_values( self, lineA, lineB ):
        lineA_value = str( lineA.text() )
        lineB_value = str( lineB.text() )

        utilities.set_line( lineA, lineB_value )
        utilities.set_line( lineB, lineA_value )



    '''
    ========================================================================
    ---->  Procedure parses given project_path if photoshop_file is found return
    the Photoshop low and high resolution data  <----
    ========================================================================
    '''
    def get_photoshop_group_data( self, project_path, photoshop_file ):
        load_projects = utilities.load_json_file( project_path )

        for project in load_projects['saved_files']:

            if project['photoshop_file'] == photoshop_file:
                ps_low = project['low']
                ps_high = project['high']

        return ps_low, ps_high



    '''
    ========================================================================
    ---->  Procedure gets all the data from the table and biulds the main
    dictionary  <----
    ========================================================================
    '''
    def get_group_table_data( self, rows ):
        group_data = {}

        low_group_data = {}
        high_group_data = {}

        for row in rows:
            try:
                row = row.row()
            except:
                pass

            group_name = self.group_table.item( row, 0 )
            group_low = self.group_table.item( row, 1 )
            group_high = self.group_table.item( row, 2 )

            if group_name != None:
                group_name = str( group_name.text() )

            if group_low != None:
                group_low = str( group_low.text() )
                group_low_width = int( group_low.split( 'x' )[0] )
                group_low_height = int( group_low.split( 'x' )[1] )

                low_group_data[group_name] = [group_low_width, group_low_height]

            else:
                low_group_data[group_name] = [None, None]

            if group_high != None:
                group_high = str( group_high.text() )
                group_high_width = int( group_high.split( 'x' )[0] )
                group_high_height = int( group_high.split( 'x' )[1] )

                high_group_data[group_name] = [group_high_width, group_high_height]

            else:
                high_group_data[group_name] = [None, None]

        if low_group_data != {} and high_group_data != {}:
            group_data['low'] = low_group_data
            group_data['high'] = high_group_data

        return group_data



    '''
    ========================================================================
    ---->  Procedure exports all or selected items in self.group_table  <----
    ========================================================================
    '''
    def export( self ):
        '''Export directory'''
        export_dir = str( self.dir_line.text() )

        '''Get export list'''
        selected_row = self.group_table.selectionModel().selectedRows()

        if selected_row == []:
            for i in xrange( self.group_table.rowCount() ):
                selected_row.append( i )

        group_data = self.get_group_table_data( selected_row )
        group_list = utilities.load_json_file( GROUPS_LOCATION )

        '''Photoshop data'''
        all_grps = self.ps_app.ActiveDocument.LayerSets

        try:
            ps_path = self.ps_app.ActiveDocument.path
            ps_path = ps_path.replace( "\\", '/' )
            ps_name = self.ps_app.ActiveDocument.name

        except:
            group_data = {}
            self.message_report( error_level = 2,
                                 message = "Can't find current Photoshop Directory. Make Sure to save the current Photoshop file!" )

        if group_data != {}:
            if ( len( all_grps ) > 0 ):
                if os.path.exists( export_dir ):

                    '''Saves all layers and visible presets'''
                    layer_visible_dictionary = self.save_layer_visibility()

                    '''Export each group in list'''
                    for group_size in group_data:
                        for group_name in group_data[group_size]:
                            if group_data[group_size][group_name][0] != None:
                                width = group_data[group_size][group_name][0]
                                height = group_data[group_size][group_name][1]

                                for grp in all_grps:
                                    if grp.Name.lower() == group_name:
                                        grp.Visible = True

                                        '''Create file name'''
                                        file_name = '{0}{1}_{2}{3}.tga'.format( export_dir, ps_name.split( '.' )[0], group_size, group_list[group_name] )

                                        '''Save photoshop scene history'''
                                        saved_state = self.ps_app.ActiveDocument.activeHistoryState

                                        '''Edit layer'''
                                        self.ps_app.ActiveDocument.flatten
                                        self.ps_app.ActiveDocument.ResizeImage ( width, height, 72 )
                                        self.ps_app.ActiveDocument.activeLayer.Copy

                                        '''Save layer'''
                                        self.ps_app.ActiveDocument.SaveAs( file_name, Options = self.options )

                                        '''Load photoshop scene history'''
                                        self.ps_app.ActiveDocument.ActiveHistoryState = saved_state
                                        self.ps_app.ActiveDocument.Paste

                                        grp.Visible = False

                    self.load_layer_visibility( layer_visible_dictionary )
                    self.save_export_data( group_data, ps_path, ps_name )



    '''
    ========================================================================
    ---->  Procedure saves Photoshops current layer setup and visibility  <----
    ========================================================================
    '''
    def save_layer_visibility( self ):
        layer_visible_dictionary = {}

        all_layers = self.ps_app.ActiveDocument.Layers

        for layer in all_layers:
            layer_visible_dictionary[layer.Name.lower()] = layer.Visible
            layer.Visible = False

        return layer_visible_dictionary



    '''
    ========================================================================
    ---->  Procedure loads Photoshops layer setup and visibility  <----
    ========================================================================
    '''
    def load_layer_visibility( self, layer_visible_dictionary ):
        all_layers = self.ps_app.ActiveDocument.Layers

        for layer in all_layers:
            for layer_name, visible in layer_visible_dictionary.iteritems():
                if layer.Name.lower() == layer_name:
                    layer.Visible = bool( visible )



    '''
    ========================================================================
    ---->  Procedure saves out all the exported data to project  <----
    ========================================================================
    '''
    def save_export_data( self, group_data, ps_path, ps_name ):
        project_name = str( self.project_combo.currentText() )

        ps_location = '{0}{1}'.format( ps_path, ps_name )

        group_data['photoshop_file'] = ps_location

        load_projects = utilities.load_json_file( '{0}{1}.project'.format( DATA_PATH, project_name ) )
        null_file = False

        if load_projects['saved_files'] == []:
            load_projects['saved_files'] = [group_data]
            null_file = True

        for project in load_projects['saved_files']:
            if project == None:
                load_projects['saved_files'] = [group_data]
                null_file = True

            else:
                try:
                    if project['photoshop_file'] == ps_location:
                        update_low_groups = set( project['low'] ).intersection( group_data['low'] )
                        update_high_groups = set( project['high'] ).intersection( group_data['high'] )

                        new_low_grps = list( set( group_data['low'] ) - set( project['low'] ) )
                        new_high_grps = list( set( group_data['high'] ) - set( project['high'] ) )

                        for low_goup in update_low_groups:
                            project['low'][low_goup] = group_data['low'][low_goup]

                        for high_goup in update_high_groups:
                            project['high'][high_goup] = group_data['high'][high_goup]

                        for grp in new_low_grps:
                            project['low'].update( {grp: group_data['low'][grp]} )

                        for grp in new_high_grps:
                            project['high'].update( {grp: group_data['high'][grp]} )

                except:
                    pass


        new_project = False

        for project in load_projects['saved_files']:
            if not null_file:
                new_project = list( set( [group_data['photoshop_file']] ) - set( [project['photoshop_file']] ) )

                if new_project == []:
                    new_project = False
                    break

        if new_project != False:
            load_projects['saved_files'].append( group_data )


        utilities.write_json_file( '{0}{1}.project'.format( DATA_PATH, project_name ), load_projects )

        save_current_ps = utilities.yes_no_dialog( self, 'Save Photoshop Files', 'Would you like to save your current Photoshop file {0}{1}?'.format( ps_path, ps_name ) )

        if save_current_ps:
            self.save_photoshop_file( ps_path, ps_name )

        self.message_report( error_level = 0,
                                     message = "Export completed!" )



    '''
    ========================================================================
    ---->  Procedure saves over current Photoshop file  <----
    ========================================================================
    '''
    def save_photoshop_file( self, ps_path, ps_name ):
        options = win32com.client.Dispatch( 'Photoshop.PhotoshopSaveOptions' )
        self.ps_app.ActiveDocument.SaveAs( '{0}{1}'.format( ps_path, ps_name ), Options = options )



    '''
    ========================================================================
    ---->  Procedure sends message reports  <----
    ========================================================================
    '''
    def message_report( self, error_level = 0, message = '' ):

        if error_level == 0:
            text_color = 'blue'

        elif error_level == 1:
            text_color = 'purple'

        elif error_level == 2:
            text_color = 'red'
            message = 'Error: {0}'.format( message )

        palette = PyQt4.QtGui.QPalette()

        palette.setColor( PyQt4.QtGui.QPalette.Text, PyQt4.QtGui.QColor( text_color ) )  # @UndefinedVariable

        self.message_line.setPalette( palette )

        self.message_line.setText( str( message ) )



'''
========================================================================
---->  Runs main class  <----
========================================================================
'''
if __name__ == '__main__':
    app = PyQt4.QtGui.QApplication( sys.argv )
    main_ui = Photoshop_Group_Exporter()
    main_ui.show()
    sys.exit( app.exec_() )






