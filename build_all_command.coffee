path = require('./mixins.coffee').path
ConsoleCommandBase = require("./console_command_base.coffee").base
Cleanup_Build_Dir = require("./cleanup_build_dir_command.coffee").cleanup_build_dir
loadit = require("loadit")
_ = require("underscore")


#supermarkets: [supermarket]
#supermarket:
	#name: ''
	#receipts: [receipt]		
#receipt:
	#tiff_file: ''
	#box_file: ''

class BuildAllCommand
	constructor:(@receipts_dir = 'receipts', @supermarkets = []) ->
		@receipts_dir = path.join(process.cwd(), @receipts_dir)

	execute: ->
		cleanup_build_dir = new Cleanup_Build_Dir()
		cleanup_build_dir.execute()
		cleanup_build_dir.on('command_finished', () =>
			loadit.load(@receipts_dir, /.tiff|.box$/i, (err, files) =>
				console.log(err) if err
				@all_files = files
				@_build_all()
			)
		)

	_build_all: ->
		@_match_receipt_image_and_box_pairs()

	_match_receipt_image_and_box_pairs: ->
		_.each(@all_files, (receipts, supermarket) =>
			@supermarkets[supermarket] =
				receipts: []
			_.each(receipts, (ignore_dirs, files) =>
				
			)
		)
		
exports.build_all = BuildAllCommand