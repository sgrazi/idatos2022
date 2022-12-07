const axios = require("axios");
const fs = require('fs');
let SOURCES
fs.readFile('imdbIDS.txt', 'utf8', (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  SOURCES = data.split(',')
  SOURCES = SOURCES.slice(400,500) // Streaming Availability permite 100 al dia
  // const API_KEY = ''
  // const API_KEY = ''
  // const API_KEY = ''

  // itera SOURCES y guarda un json para cada respuesta de cada request
  var promise = Promise.resolve();
  SOURCES.forEach(function (SOURCE) {
    promise = promise.then(function () {


      const options = {
        method: 'GET',
        url: 'https://streaming-availability.p.rapidapi.com/get/basic',
        params: {country: 'us', imdb_id: SOURCE, output_language: 'en'},
        headers: {
          'X-RapidAPI-Key': API_KEY,
          'X-RapidAPI-Host': 'streaming-availability.p.rapidapi.com'
        }
      };
      // wait random time under 2 seconds because of API restrictions
      const start = Date.now();
      let now = start;
      while (now - start < Math.floor(Math.random() * 5000)) {
        now = Date.now();
      }
  
      axios.request(options).then(function (response) {  
        var jsonContent = JSON.stringify(response.data,null,3);
        fs.writeFile('../../data/strav-jsons/'+SOURCE+'.json', jsonContent, 'utf8', function (err) {
            if (err) {
                console.log("An error occured while writing JSON Object to File.");
                return console.log(err);
            }
            console.log("JSON file has been saved.");
        });
      }).catch(function (error) {
        // retry
        console.log("retry:" + error)
      });


      return new Promise(function (resolve) {
        setTimeout(resolve, 1000);
      });
    });
  });

  promise.then(function () {
    console.log('Loop finished.');
  });

});