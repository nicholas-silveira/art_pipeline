import pysideuic
import xml.etree.ElementTree as xml
from cStringIO import StringIO

import PySide.QtGui

def get_ui_handle( ui_file ):
   """
   Pablo Winant
   """
   parsed = xml.parse( ui_file )
   widget_class = parsed.find( 'widget' ).get( 'class' )
   form_class = parsed.find( 'class' ).text
   
   with open( ui_file, 'r' ) as f:
      o = ui_file()
      frame = {}
      
      pysideuic.compileUi( f, o, indent = 0 )
      pyc = compile( o.getvalue(), '<string>', 'exec' )
      exec pyc in frame
      
      # Fetch the base_class and form class based on their type in the xml from designer
      form_class = frame['Ui_{0}'.format( form_class )]
      base_class = eval( 'PySide.QtGui.{0}'.format( widget_class ) )
      
   return form_class, base_class
