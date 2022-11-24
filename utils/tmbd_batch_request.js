const axios = require("axios");
const fs = require('fs');
let SOURCES
fs.readFile('imdbIDS.txt', 'utf8', (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  SOURCES = data.split(',')
  const API_KEY = '6ba4780de0e336f12b138a8b9a3ec494'

  // itera SOURCES y guarda un json para cada respuesta de cada request
  SOURCES.forEach((SOURCE) => {
    const options = {
      method: 'GET',
      url: 'https://api.themoviedb.org/3/find/'+SOURCE+'?api_key='+API_KEY+'&external_source=imdb_id',
    };
    
    axios.request(options).then(function (response) {
        var jsonContent = JSON.stringify(response.data,null,3);
        fs.writeFile('../tmdb-jsons/'+SOURCE+'.json', jsonContent, 'utf8', function (err) {
            if (err) {
                console.log("An error occured while writing JSON Object to File.");
                return console.log(err);
            }
        
            console.log("JSON file has been saved.");
        });
    }).catch(function (error) {
      console.error(error);
    });
  });
});