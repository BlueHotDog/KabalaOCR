ConsoleCommandBase = require("./console_command_base.coffee").base
path = require('./mixins.coffee').path

class GenerateTrFile extends ConsoleCommandBase 
	constructor:(@input_filename, @output_path = "build") ->
		@input_filename_path = path.fullpath_filename_without_ext(@input_filename)
		input_filename_without_ext = path.filename_without_ext(@input_filename)
		@output_path = path.join(process.cwd(), @output_path)

		@commands = [
			"tesseract #{@input_filename_path}.tiff #{@output_path}/#{input_filename_without_ext} nobatch box.train",
			"unicharset_extractor -D #{@output_path} #{@input_filename_path}.box",
			"echo #{input_filename_without_ext} 0 0 0 0 0 > #{@output_path}/font_properties" #add bold setting
			]
		@cleanup_commands = ["cd ."]
		# 	"rm #{@output_path}/*.txt",
		# 	"rm #{@output_path}/*font_properties",
		# 	"rm #{@output_path}/*unicharset"
		# ]
		super(@commands, @cleanup_commands)	
		
	
exports.tr = GenerateTrFile		