util = require('util')
exec = require('child_process').exec

#Usage: coffee generate_traineddata_command.coffee box_filename
#Notes: The command requires a tif and a box file with the same name
#and the tif extension should be tif and not tiff! It can run without elevation
class ConsoleCommandBase
	constructor:(@commands) ->
		@current = 0

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
		
exports.base = ConsoleCommandBase