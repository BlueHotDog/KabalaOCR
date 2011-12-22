path = require('./mixins.coffee').path
ConsoleCommandBase = require("./console_command_base.coffee").base

class GenerateTrFile extends ConsoleCommandBase 
	constructor:(@input_filename, @output_path = "build") ->
		input_filename_fullpath = path.join(process.cwd(), path.fullpath_filename_without_ext(@input_filename))
		input_filename_without_ext = path.filename_without_ext(@input_filename)
		@output_path = path.join(process.cwd(), @output_path)

		@commands = [
			"tesseract #{input_filename_fullpath}.tiff #{input_filename_without_ext} nobatch box.train",
			"unicharset_extractor #{input_filename_fullpath}.box",
			"echo #{input_filename_without_ext} 0 0 0 0 0 > font_properties" #add bold setting
			]
		@cleanup_commands = [
			"rm *.txt"
		]
		super(@commands, @cleanup_commands, @output_path)
		
	
exports.tr = GenerateTrFile		