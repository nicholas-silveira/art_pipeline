import json 



'''
========================================================================
---->  Save Json File  <----
========================================================================
'''
def save_json( file_name, data, *args ):
	json_data = json.dumps( data, ensure_ascii = True , indent = 2 )

	data_file = open( file_name.replace( '\\', '/' ), "w" )
	data_file.write( json_data )
	data_file.close()

'''
========================================================================
---->  Load Json File  <----
========================================================================
'''
def load_json( file_name ):
	data_file = open( file_name.replace( '\\', '/' ) )
	data = json.load( data_file )

	return data
