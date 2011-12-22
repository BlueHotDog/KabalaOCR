Command_Runner = require("./console_command_runner.coffee").command_runner

class ConsoleCommandBase
	constructor:(@commands, @cleanup_commands = [], @working_dir = null) ->

	execute: ->
		main_commands_runner = new Command_Runner(@commands, @working_dir)
		main_commands_runner.on('command_runner_finished', ()=>
        @cleanup_commands_runner = new Command_Runner(@cleanup_commands, @working_dir)
        @cleanup_commands_runner.run()
		) if @cleanup_commands.length > 0
		main_commands_runner.run()
		
exports.base = ConsoleCommandBase