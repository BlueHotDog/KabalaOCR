var vows    = require('vows'),
    assert  = require('assert'),
    loadit  = require('../loadit'),
    dir     = __dirname + '/folder1',
    regex   = /.js$/i;

vows.describe('loadit callback').addBatch({
    'Load property': {
        topic: function() {
            return loadit.load;
        },
        
        'is defined as a function' : function(loadFn) {
            assert.deepEqual(typeof(loadFn), 'function');
        },
        
        'when called' : {
            topic : function() {
                loadit.load(dir, regex, this.callback);
            },
            
            'does not result in an error' : function(err, files) {
                assert.isNull(err);
            },
            
            'results in an array of .js files': function(err, files) {
                assert.isArray(files);
            },
            
            'has at least one file': function(err, files) {
                assert.isNotZero(files.length);
            },
            
            'equals all js files': function(err, files) {
                assert.deepEqual(files.sort(), [__dirname + '/folder1/file1.js', __dirname + '/folder1/folder2/folder3/file3.js'].sort());
            },
            
            'file1 has been loaded': function(err, files) {
                assert.deepEqual(global.FILE1TEST, true);
            }
        }
    }
}).export(module);