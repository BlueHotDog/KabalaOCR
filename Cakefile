option '-t', '--tr_file [Filename]', 'path to the tif/box filename'
option '-l', '--language_name [name]', 'language name to generate'

task 'tr_file', 'generate tr file', (options) ->
  tr = require('./generate_tr_file_command.coffee').tr
  generate_tr_file = new tr(options.tr_file)
  generate_tr_file.execute()

task 'language', 'generate traineddata file', (options) ->
  traineddata_command = require('./generate_traineddata_command.coffee').trained_data
  traineddata_command = new traineddata_command(options.language_name)
  traineddata_command.execute()

task 'build', 'creates a traineddata file from all the receipts in the repository', (options) ->
	build_all_command = require('./build_all_command.coffee').build_all
	build_all_command = new build_all_command()
	build_all_command.execute()

task 'cleanup', 'cleans the build directory', ->
  cleanup_command = require('./cleanup_build_dir_command.coffee').cleanup_build_dir
  cleanup_command = new cleanup_command()
  cleanup_command.execute()
		  
