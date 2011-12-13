Command_Runner = require("./console_command_runner.coffee").command_runner

class ConsoleCommandBase
	constructor:(@commands, @cleanup_commands) ->
		@current = 0

	execute: ->
		main_commands_runner = new Command_Runner(@commands)
		main_commands_runner.on('command_runner_finished', ()=>
			@cleanup_commands_runner = new Command_Runner(@cleanup_commands)
			@cleanup_commands_runner.run()
		)
		main_commands_runner.run()
		
exports.base = ConsoleCommandBase