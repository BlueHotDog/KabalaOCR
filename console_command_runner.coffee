util = require('util')
exec = require('child_process').exec
emitter = require('events').EventEmitter

class ConsoleCommandRunner extends emitter
	constructor:(@commands, @working_dir) ->
    @current = 0

	print_commands: ->
		for command in @commands
			console.log(command)

	run: ->
		@_runCommand(@commands[@current])
		
	_runCommand:(command) ->
    exec(command, {cwd: @working_dir}, (error, stdout, stderr) =>
        @_print_command_error(command,error,stdout,stderr) unless error is null
        if @_last_command()
          @emit('command_runner_finished')
        else
          @_runCommand(@_get_next_command())
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

exports.command_runner = ConsoleCommandRunner