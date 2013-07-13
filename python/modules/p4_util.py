import subprocess

def add():
   pass

def edit( files ):
   """
   Edit P4 Files
   
   *Arguments:*
      * ``Argument`` ArgDescription
   
   *Keyword Arguments:*
      * ``kwarg`` KwargDescription
   
   *Returns:*
      * ``Value`` ReturnDescription
   
   *Examples:* ::
   
      import p4
      
      p4_edit_results = p4.edit( ['//depot/unit_test/test.py'] )
      
   *Unit Test:* ::
   
      import p4_util
		
		p4_edit_results = p4_util.edit( ['//depot/unit_test/test.py'] )
		self.assertEqual( p4_edit_results, True, 'P4 Edit Failed!' )
      *Unit Test End*
   
   *Todo:*
      * Todos_optional
   
   *Author:*
      * Nicholas.Silveira, Nicholas.Silveira@gmail.com, May 19, 2013 10:12:36 PM
   """

   file_str = ' '.join( files )

   prog = subprocess.Popen( 'p4 -c projects edit ' + file_str,
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE )
   prog.communicate()

   if prog.returncode:
      raise Exception( 'program returned error code {0}'.format( prog.returncode ) )

      return False

   else:
      print '\nThese Files Are Open For Edit!'
      print '======================================='
      for file_name in files:
         print file_name

         return True

def submit( files, reopen = False, description = None ):
   prog = subprocess.Popen( 'p4 -I submit',
                            stdout = subprocess.PIPE,
                            stderr = subprocess.PIPE )
   prog.communicate()

   if prog.returncode:
      raise Exception( 'program returned error code {0}'.format( prog.returncode ) )



