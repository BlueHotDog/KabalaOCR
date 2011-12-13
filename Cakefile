option '-t', '--tr_file [Filename]', 'path to the tif/box filename'

task 'tr_file', 'generate tr file', (options) ->
  tr = require('./generate_tr_file_command.coffee').tr
  generate_tr_file = new tr(options.tr_file)
  generate_tr_file.execute()

