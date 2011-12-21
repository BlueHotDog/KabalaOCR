util = require('util')
exec = require('child_process').exec
path = require('./mixins.coffee').path
ConsoleCommandBase = require("./console_command_base.coffee").base

#Usage: coffee generate_traineddata_command.coffee box_filename
#Notes: The command requires a tif and a box file with the same name
#and the tif extension should be tif and not tiff! It can run without elevation
class TrainedDataGenerator extends ConsoleCommandBase
  constructor:(@input_filename, @output_path = "build") ->
    input_filename_path = path.fullpath_filename_without_ext(@input_filename)
    input_filename_without_ext = path.filename_without_ext(@input_filename)
    @output_path = path.join(process.cwd(), @output_path)

    @commands = [
      "mftraining -F #{@output_path}/font_properties -U #{@output_path}/unicharset #{@output_path}/#{input_filename_without_ext}.tr",
      "mftraining -F #{@output_path}/font_properties -U #{@output_path}/unicharset -O #{@output_path}/#{input_filename_without_ext}.unicharset #{@output_path}/#{input_filename_without_ext}.tr",
      "cntraining #{@output_path}/#{input_filename_without_ext}.tr",
      "mv Microfeat #{@output_path}/#{input_filename_without_ext}.Microfeat",
      "mv normproto #{@output_path}/#{input_filename_without_ext}.normproto",
      "mv pffmtable #{@output_path}/#{input_filename_without_ext}.pffmtable",
      "mv mfunicharset #{@output_path}/#{input_filename_without_ext}.mfunicharset",
      "mv inttemp #{@output_path}/#{input_filename_without_ext}.inttemp",
      "combine_tessdata #{@output_path}/#{input_filename_without_ext}."]
    super(@commands)

exports.trained_data = TrainedDataGenerator