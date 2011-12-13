util = require('util')
exec = require('child_process').exec
ConsoleCommandBase = require("./console_command_base.coffee").base

#Usage: coffee generate_traineddata_command.coffee box_filename
#Notes: The command requires a tif and a box file with the same name
#and the tif extension should be tif and not tiff! It can run without elevation
class TrainedDataGenerator extends ConsoleCommandBase
  constructor:(@box_filename) ->
    @commands = [
      "mftraining -F font_properties -U unicharset #{@box_filename}.tr",
      "mftraining -F font_properties -U unicharset -O #{@box_filename}.unicharset #{@box_filename}.tr",
      "cntraining #{@box_filename}.tr",
      "mv Microfeat #{@box_filename}.Microfeat",
      "mv normproto #{@box_filename}.normproto",
      "mv pffmtable #{@box_filename}.pffmtable",
      "mv mfunicharset #{@box_filename}.mfunicharset",
      "mv inttemp #{@box_filename}.inttemp",
      "combine_tessdata #{@box_filename}."]
    super(@commands)

exports.trained_data = TrainedDataGenerator