const axios = require("axios");
const fs = require('fs');
let SOURCES
fs.readFile('imdbIDS.txt', 'utf8', (err, data) => {
  if (err) {
    console.error(err);
    return;
  }
  SOURCES = data.split(',')
  SOURCES = SOURCES.slice(196,297) // Streaming Availability permite 100 al dia
  // const API_KEY = '094d2f444emsh7cc38e76be5a61ap1e0f04jsn39d63fc80a46'
  // const API_KEY = 'e038b7cca5mshe4eb72c1425d861p14a01djsn5bcd857b29c5'
  // const API_KEY = '6ca81a2933msh2f51c982f78285ap18f520jsn4ce451d8bb9f'

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
        fs.writeFile('../strav-jsons/'+SOURCE+'.json', jsonContent, 'utf8', function (err) {
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