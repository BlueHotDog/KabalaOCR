util = require('util')
exec = require('child_process').exec

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

  execute: ->
    @_runCommand(@commands[@current])

  _runCommand:(command) ->
    exec(command, (error, stdout, stderr) =>
        unless error is null
          console.log("Error from command: #{command}")
          util.print('stdout: ' + stdout)
          util.print('stderr: ' + stderr)
          console.log('exec error: ' + error)

        @_runCommand(@_get_next_command()) unless @current is @commands.length-1
      )

  _get_next_command: ->
    @current += 1
    @commands[@current] unless @current is @commands.length

  print_commands: ->
    for command in @commands
      console.log(command)

command = new GenerateLanguageFileCommand(process.argv[2])
command.execute()