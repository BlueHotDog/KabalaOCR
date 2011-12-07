fs = require('fs')
exec = require('child_process').exec
async = require('async')

class Runner
	constructor: (@receiptDir, @extension = ".tiff", @commandsDir = process.cwd()) ->
		
	scan: (path = "receipts", cb = -> ) ->
		
		files = fs.readdirSync(path)
		f = (file, cb) => @generateTRFile(file, path, cb)
		async.forEach(files, f, (err) -> console.log "error:\t#{err}")
		cb()			
	
	generateTRFile: (file, path, cb) =>
		currentFile = "#{path}/#{file}"
		stats = fs.statSync(currentFile)
		@scan(currentFile, cb) if stats.isDirectory()
		@runCommand("generate_tr_file_command", [currentFile], cb) if @getExt(currentFile) is @extension

	getExt: (path) ->
		i = path.lastIndexOf('.')
		if i<0 then '' else path.substr(i)

	runCommand: (file, params, cb) =>
		params = params.join(" ")

		exec("/usr/local/bin/coffee #{@commandsDir}/#{file}.coffee #{params}", 
			(err,stdout,stderr)-> 
				console.log stdout
				console.log stderr
				cb()
			)

		
command = new Runner()
command.scan("#{process.cwd()}/#{process.argv[2]}")		