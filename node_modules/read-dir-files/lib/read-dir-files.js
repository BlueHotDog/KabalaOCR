var fs = require('fs'),
    path = require('path'),
    async = require('async');

//
// ### function readDirFiles(dir, encoding, recursive, callback)
// #### @dir {string} Directory to read files from
// #### @encoding {string} Files encoding. **Optional.**
// #### @recursive {boolean} Recurse into subdirectories? **Optional**, default `true`.
// #### @callback {function} Callback. **Optional.**
// Asynchronously reads all files from `dir` and returns them to the callback
// in form:
//
//     {
//       dir: {
//         file0: <Buffer ...>,
//         file1: <Buffer ...>,
//         sub: {
//          file0: <Buffer ...>
//        }
//      }
//    }
//
// Following calling conventions are supported:
//
//     readDirFiles(dir)
//     readDirFiles(dir, 'utf8')
//     readDirFiles(dir, 'utf8', true)
//     readDirFiles(dir, true)
//
// With or without callback.
//
var readDirFiles = module.exports = function (dir, encoding, recursive, callback) {
  var result = {}

  callback = arguments[arguments.length - 1];
  typeof callback == "function" || (callback = null);

  if (typeof encoding == "boolean") {
    recursive = encoding;
    encoding = null;
  }
  typeof recursive == "undefined" && (recursive = true);
  typeof encoding == "string" || (encoding = null);

  fs.readdir(dir, function (err, entries) {
    if (err) return (callback && callback(err));

    async.forEach(entries, function (entry, next) {
      var entryPath = path.join(dir, entry);
      fs.stat(entryPath, function (err, stat) {
        if (err) return next(err);

        if (stat.isDirectory()) {
          return (recursive || next()) && readDirFiles(
            entryPath, 
            encoding,
            function (err, entries) {
              if (err) return next(err);
              result[entry] = entries;
              next();
            }
          );
        }
        fs.readFile(entryPath, encoding, function (err, content) {
          if (err) return next(err);
          result[entry] = content;
          next();
        });
      });
    }, function (err) {
      callback && callback(err, result);
    });
  });
};

