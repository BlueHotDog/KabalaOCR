var util = require('util'),
	exec = require('child_process').exec,
	child;

// executes tesseract [lang].[fontname].exp[num].tif [lang].[fontname].exp[num] batch.nochop makebox
child = exec("tesseract "+process.cwd()+"/"+process.argv[2]+".tiff "+process.cwd()+"/"+process.argv[2]+" batch.nochop makebox", function (error, stdout, stderr) {
	util.print('stdout: ' + stdout);
	util.print('stderr: ' + stderr);
	if (error !== null) {
		console.log('exec error: ' + error);
	}
});