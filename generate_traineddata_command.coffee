util = require('util')
exec = require('child_process').exec

#Usage: coffee generate_traineddata_command.coffee box_filename
#Notes: The command requires a tif and a box file with the same name
#and the tif extension should be tif and not tiff! It can run without elevation
class GenerateLanguageFileCommand
  constructor:(@box_filename) ->
    @current = 0
    @commands = ["tesseract #{@box_filename}.tif #{@box_filename} nobatch box.train",
      "unicharset_extractor #{@box_filename}.box",
      "echo #{@box_filename} 0 0 0 0 0 > font_properties",
      "mftraining -F font_properties -U unicharset #{@box_filename}.tr",
      "mftraining -F font_properties -U unicharset -O #{@box_filename}.unicharset #{@box_filename}.tr",
      "cntraining #{@box_filename}.tr",
      "mv Microfeat #{@box_filename}.Microfeat",
      "mv normproto #{@box_filename}.normproto",
      "mv pffmtable #{@box_filename}.pffmtable",
      "mv mfunicharset #{@box_filename}.mfunicharset",
      "mv inttemp #{@box_filename}.inttemp",
      "combine_tessdata #{@box_filename}."]

  print_commands: ->
    for command in @commands
      console.log(command)

  execute: ->
    @_runCommand(@commands[@current])

  _runCommand:(command) ->
    exec(command, (error, stdout, stderr) =>
        @_print_command_error(command,error,stdout,stderr) unless error is null
        @_runCommand(@_get_next_command()) unless @_last_command()
      )

  _print_command_error:(command,error, stdout, stderr) ->
    console.log("Error from command: #{command}")
    util.print('stdout: ' + stdout)
    util.print('stderr: ' + stderr)
    console.log('exec error: ' + error)

  _last_command: ->
    true if @current is @commands.length-1

  _get_next_command: ->
    @current += 1
    @commands[@current] unless @current is @commands.length

command = new GenerateLanguageFileCommand(process.argv[2])
command.execute()