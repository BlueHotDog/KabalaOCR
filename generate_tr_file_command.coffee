ConsoleCommandBase = require("./console_command_base.coffee").base

class GenerateTrFile extends ConsoleCommandBase 
	constructor:(@box_filename) ->
		i = @box_filename.lastIndexOf('.')
		@box_filename = @box_filename.substr(0,i)
		@commands = [
			"tesseract #{@box_filename}.tiff #{@box_filename} nobatch box.train",
			"unicharset_extractor #{@box_filename}.box",
			"echo #{@box_filename} 0 0 0 0 0 > font_properties" #add bold setting
			]
		super(@commands)
		
command = new GenerateTrFile(process.argv[2])
command.execute()
		