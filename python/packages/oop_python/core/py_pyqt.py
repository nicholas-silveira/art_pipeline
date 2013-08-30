'''Import Extra Modules'''
import os

import PyQt4.QtCore
import PyQt4.QtGui
import PyQt4.uic

import json

import logging


def supression_warnings():
	PyQt4.uic.properties.logger.setLevel(logging.WARNING)
	PyQt4.uic.uiparser.logger.setLevel(logging.WARNING)

def window_stay_on_top( value, ui_name ):
   flags = ui_name.windowFlags()

   if value:
      ui_name.setWindowFlags( flags | PyQt4.QtCore.Qt.WindowStaysOnTopHint )

   else:
      ui_name.setWindowFlags( flags & ~PyQt4.QtCore.Qt.WindowStaysOnTopHint )

'''
========================================================================
---->  Procedure adds and removes index from given QComboBox  <----
========================================================================
'''
def add_remove_combo( combo, add = False, remove = False, data = '' ):
   if add:
      if data != '':
         combo.addItem ( data )
         list_count = combo.count()
         combo.setCurrentIndex( list_count - 1 )

   if remove:
      current_index = combo.currentIndex ()
      combo.removeItem ( current_index )

'''
========================================================================
---->  Procedure returns all items in given QComboBox  <----
========================================================================
'''
def get_combo_items( combo ):
   items = []

   count_items = combo.count()

   for i in range( count_items ):
      items.append( str( combo.itemText( i ) ) )

   return items

'''
========================================================================
---->  Procedure searches given QComboBox for passed item  <----
========================================================================
'''
def search_combo_items( combo, item ):
   count_items = combo.count()

   if count_items != 0:
      for i in range( count_items ):
         if item == str( combo.itemText( i ) ):
            item_value = i
            break

         else:
            item_value = None

      return item_value

   else:
      return None

'''
========================================================================
---->  Procedure adds items to given QTableWidget  <----
========================================================================
'''
def add_table_item( table, items ):
   row = table.rowCount()
   table.insertRow( row )

   column = 0

   for item in items:
      item = PyQt4.QtGui.QTableWidgetItem( item )
      table.setItem ( row, column, item )
      column += 1

'''
========================================================================
---->  Procedure removes selected rows from given QTableWidget  <----
========================================================================
'''
def remove_selected_table_row( table ):
   sel_rows = table.selectionModel().selectedRows()

   if sel_rows != []:
      for sel_row in reversed( sel_rows ):
         table.removeRow( sel_row.row() )

'''
========================================================================
---->  Procedure returns selected items from given QTableWidget  <----
========================================================================
'''
def get_selected_table_items( table ):
   column_count = table.columnCount()
   sel_rows = table.selectionModel().selectedRows()

   items = []

   if sel_rows != []:
      for row in sel_rows:
         for column in range( column_count ):
            items.append( str( table.item( row.row(), column ).text() ) )

   return items
'''
========================================================================
---->  Procedure sets passed directory to self.dir_line  <----
========================================================================
'''
def set_line( line, data ):
   line.setText( str( data ) )

'''
========================================================================
---->  Procedure searches for passed directory if is dosn't exist
create it  <----
========================================================================
'''
def get_directory( file_location ):
   file_directory = os.path.dirname( file_location )

   if not os.path.exists( file_directory ):
      os.makedirs( file_directory )

'''
========================================================================
---->  Procedure create a QMessageBox and will return reply  <----
========================================================================
'''
def yes_no_dialog( self, name, message ):
   reply = PyQt4.QtGui.QMessageBox.question( self, name, message,
   PyQt4.QtGui.QMessageBox.Yes | 
   PyQt4.QtGui.QMessageBox.No )

   if reply == PyQt4.QtGui.QMessageBox.Yes:
      return True

   elif reply == PyQt4.QtGui.QMessageBox.No:
      return False

'''
========================================================================
---->  Procedure writes a json data file  <----
========================================================================
'''
def write_json_file( file_location, data, *args ):

   get_directory( file_location )
   json_data = json.dumps( data, ensure_ascii = True , indent = 2 )

   data_file = open( file_location, "w" )
   data_file.write( json_data )
   data_file.close()

'''
========================================================================
---->  Procedure parses and returns json data file  <----
========================================================================
'''
def load_json_file( file_location ):
   data_file = open( file_location )
   data = json.load( data_file )

   return data
