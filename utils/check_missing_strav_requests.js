const fs = require('fs');
let SOURCES

fs.readFile('imdbIDS.txt', 'utf8', (err, data) => {
    if (err) {
        console.error(err);
        return;
    }
    SOURCES = data.split(',')
    dirname = '../strav-jsons/'
    files = []
    fs.readdir(dirname, function(err, filenames) {
        if (err) {
            console.log(err);
            return;
        }
        filenames.forEach(function(filename) {
            files.push(filename.substring(0, filename.length - 5))
        });
        
        files.forEach(name => {
            console.log(name)
            const index = SOURCES.indexOf(name);
            SOURCES.splice(index, 1);
        })

        fs.writeFile('Output.txt', SOURCES.toString(), (err) => {
        
            // In case of a error throw err.
            if (err) throw err;
        })
        
    });
})



