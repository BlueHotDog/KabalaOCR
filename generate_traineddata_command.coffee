path = require('./mixins.coffee').path
ConsoleCommandBase = require("./console_command_base.coffee").base

class GenerateTrainedDataFile extends ConsoleCommandBase
  constructor:(@input_filename, @output_path = "build") ->
    input_filename_without_ext = path.filename_without_ext(@input_filename)
    @output_path = path.join(process.cwd(), @output_path)

    @commands = [
      "mftraining -F font_properties -U unicharset #{input_filename_without_ext}.tr",
      "mftraining -F font_properties -U unicharset -O #{input_filename_without_ext}.unicharset #{input_filename_without_ext}.tr",
      "cntraining #{input_filename_without_ext}.tr",
      "mv Microfeat #{input_filename_without_ext}.Microfeat",
      "mv normproto #{input_filename_without_ext}.normproto",
      "mv pffmtable #{input_filename_without_ext}.pffmtable",
      "mv mfunicharset #{input_filename_without_ext}.mfunicharset",
      "mv inttemp #{input_filename_without_ext}.inttemp",
      "combine_tessdata #{input_filename_without_ext}."]

    @cleanup_commands = [
      "rm *.inttemp",
      "rm *.Microfeat",
      "rm *.normproto",
      "rm *.pffmtable",
      "rm *.tr",
      "rm font_properties",
      "rm *unicharset*"
    ]
    super(@commands, @cleanup_commands, @output_path)

exports.trained_data = GenerateTrainedDataFile