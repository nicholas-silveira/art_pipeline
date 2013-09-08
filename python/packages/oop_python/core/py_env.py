import sys
import os

import oop_maya.core


def get_paths():
   return sys.path

def add_paths( paths ):
   added_paths = []
   
   for path in paths:
      if path in sys.path:
         oop_maya.core.warning( "{0} already exists!".format( path ) )
         
      else:
         if os.path.exists( path ):
            path = path.replace( '\\', '/' )
            sys.path.append( path )
            added_paths.append( path )
            
         else:
            oop_maya.core.error( "{0} doesn't exist!".format( path ) )

   return added_paths

def remove_paths( paths ):
   removed_paths = []
   
   for path in paths:
      sys.path.remove( path )
      removed_paths.append( path )

   return removed_paths
