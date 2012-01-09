path = require('./mixins.coffee').path
ConsoleCommandBase = require("./console_command_base.coffee").base

class GenerateTrFile extends ConsoleCommandBase 
	constructor:(@input_filename, @output_path = "build") ->
		input_filename_fullpath = path.join(process.cwd(), path.fullpath_filename_without_ext(@input_filename))
		input_filename_without_ext = path.filename_without_ext(@input_filename)
		@output_path = path.join(process.cwd(), @output_path)
		font_name = path.dirname_of_file(path.dirname(input_filename_fullpath))
		@commands = [
			"tesseract #{input_filename_fullpath}.tiff #{input_filename_without_ext} nobatch box.train",
			"cat #{input_filename_without_ext}.tr >> #{font_name}.tr",
			"echo #{font_name} 0 0 0 0 0 >> font_properties" #add bold setting
			]
		@cleanup_commands = [
			"rm *.txt",
			"rm #{input_filename_without_ext}.tr"
		]
		super(@commands, @cleanup_commands, @output_path)
		
	
exports.tr = GenerateTrFile		