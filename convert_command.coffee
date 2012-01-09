path = require('./mixins.coffee').path
ConsoleCommandBase = require("./console_command_base.coffee").base

class Convert extends ConsoleCommandBase 
  constructor: (input_filename)->
    input_filename_fullpath = path.join(process.cwd(), input_filename)
    input_filename_without_ext = path.filename_without_ext(input_filename)
    output_path = path.dirname(input_filename_fullpath)
    @commands = [
      "convertformat #{input_filename_fullpath} #{output_path}/#{input_filename_without_ext}.tiff TIFF"
      "convert -separate #{output_path}/#{input_filename_without_ext}.tiff #{output_path}/#{input_filename_without_ext}.tiff"
      ]
    @cleanup = [
      "rm #{input_filename_fullpath}"
    ]
    super(@commands, @cleanup, @output_path)
    
  
exports.convert = Convert