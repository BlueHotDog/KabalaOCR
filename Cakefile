option '-t', '--tr_file [Filename]', 'path to the tif/box filename'
option '-l', '--language_file [Filename]', 'path to the tif/box filename'

task 'tr_file', 'generate tr file', (options) ->
  tr = require('./generate_tr_file_command.coffee').tr
  generate_tr_file = new tr(options.tr_file)
  generate_tr_file.execute()

task 'language_file', 'generate traineddata file', (options) ->
  traineddata_command = require('./generate_traineddata_command.coffee').trained_data
  traineddata_command = new traineddata_command(options.language_file)
  traineddata_command.execute()

task 'build', 'creates a traineddata file from all the receipts in the repository', (options) ->
	build_all_command = require('./build_all_command.coffee').build_all
	build_all_command = new build_all_command()
	build_all_command.execute()
		  
