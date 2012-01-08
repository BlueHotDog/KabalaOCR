path = require('./mixins.coffee').path
ConsoleCommandBase = require("./console_command_base.coffee").base

class GenerateBoxFile extends ConsoleCommandBase 
	constructor:(input_filename, language = "super") ->
		input_filename_fullpath = path.join(process.cwd(), path.fullpath_filename_without_ext(input_filename))
		input_filename_without_ext = path.filename_without_ext(input_filename)
		output_path = path.dirname(input_filename_fullpath)
		@commands = [
			"tesseract #{input_filename} #{output_path}/#{input_filename_without_ext} batch.nochop makebox -l #{language}"
			]
		super(@commands, [], @output_path)
		
	
exports.box = GenerateBoxFile