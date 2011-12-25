path = require('./mixins.coffee').path
ConsoleCommandBase = require("./console_command_base.coffee").base

class CleanupBuildDirCommand extends ConsoleCommandBase
	constructor:(@build_dir = 'build') ->
		@build_dir = path.join(process.cwd(), @build_dir)

		@commands = [
			"rm -rf #{@build_dir}",
			"mkdir #{@build_dir}"
		]
		super(@commands)
		
exports.cleanup_build_dir = CleanupBuildDirCommand