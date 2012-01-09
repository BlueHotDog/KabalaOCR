option '-t', '--tiff_file [Filename]', 'path to the tiff filename'
option '-l', '--language_name [name]', 'language name to generate'
option '-f', '--file [Filename]', 'name of the file'

task 'box', 'run the boxing algorithm on each reciept in the new dir', (options) ->
  

task 'convert', 'convert a file from any format to monochrome tiff', (options) ->
  convert = require("./convert_command.coffee").convert
  convert = new convert(options.file)
  convert.execute()

task 'box_file', 'generate box file', (options) ->
  box = require('./generate_box_file_command.coffee').box
  generate_box_file = new box(options.tiff_file)
  generate_box_file.execute()

task 'tr_file', 'generate tr file', (options) ->
  tr = require('./generate_tr_file_command.coffee').tr
  generate_tr_file = new tr(options.tiff_file)
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

