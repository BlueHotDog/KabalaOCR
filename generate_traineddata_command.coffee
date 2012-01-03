path = require('./mixins.coffee').path
ConsoleCommandBase = require("./console_command_base.coffee").base

class GenerateTrainedDataFile extends ConsoleCommandBase
  constructor:(language_name = "super", @output_path = "build") ->
    @output_path = path.join(process.cwd(), @output_path)

    @commands = [
      "mftraining -F font_properties -U unicharset *.tr",
      "mftraining -F font_properties -U unicharset -O #{language_name}.unicharset *.tr",
      "cntraining *.tr",
      "mv Microfeat #{language_name}.Microfeat",
      "mv normproto #{language_name}.normproto",
      "mv pffmtable #{language_name}.pffmtable",
      "mv mfunicharset #{language_name}.mfunicharset",
      "mv inttemp #{language_name}.inttemp",
      "combine_tessdata #{language_name}."]

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