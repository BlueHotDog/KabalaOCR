path = require('path')

path.fullpath_filename_without_ext = (p) ->	
	"#{@dirname(p)}/#{@filename_without_ext(p)}"

path.filename_without_ext = (p) ->
	"#{@basename(p, @extname(p))}"	

exports.path = path