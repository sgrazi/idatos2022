const axios = require("axios");
const fs = require('fs');
const SOURCES = [
  "tt0045061",
  "tt0043265",
  "tt0040506",
  "tt0032455",
  "tt0023427",
  "tt9071322",
  "tt7979580",
  "tt7668870",
  "tt7131622",
  "tt3896198",
  "tt3682448",
  "tt3521164",
  "tt3416742",
  "tt3397884",
  "tt3076658",
  "tt2802154",
  "tt2582782",
  "tt2431286",
  "tt2103281",
  "tt1899353",
  "tt1855199",
  "tt1517451",
  "tt1403865",
  "tt1323594",
  "tt1306980",
  "tt1250777",
  "tt1242422",
  "tt1210166",
  "tt1189073",
  "tt0878804",
  "tt0876563",
  "tt0829482",
  "tt0814314",
  "tt0765443",
  "tt0486655",
  "tt0475276",
  "tt0455590",
  "tt0454848",
  "tt0452623",
  "tt0441773",
  "tt0421082",
  "tt0416449",
  "tt0416320",
  "tt0409459",
  "tt0399295",
  "tt0387564",
  "tt0344510",
  "tt0340377",
  "tt0315733",
  "tt0307901",
  "tt0289879",
  "tt0277027",
  "tt0265666",
  "tt0241527",
  "tt0230600",
  "tt0181865",
  "tt0144084",
  "tt0128445",
  "tt0121766",
  "tt0120863",
  "tt0120762",
  "tt0119116",
  "tt0118929",
  "tt0117631",
  "tt0112864",
  "tt0112579",
  "tt0104952",
  "tt0101410",
  "tt0099674",
  "tt0097757",
  "tt0095705",
  "tt0093870",
  "tt0093409",
  "tt0091064",
  "tt0088680",
  "tt0082694",
  "tt0075860",
  "tt0072251",
  "tt0070034",
  "tt0063374",
  "tt0061852",
  "tt0059646",
  "tt0056869",
  "tt0053459",
  "tt0048545",
  "tt0047437",
  "tt0045793",
  "tt0029583",
  "tt0026029",
  "tt0024184"
]

// itera SOURCES y guarda un json para cada respuesta de cada request
SOURCES.forEach((SOURCE) => {
  const options = {
    method: 'GET',
    url: 'https://utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com/idlookup',
    params: {source_id: SOURCE, source: 'imdb', country: 'us'},
    headers: {
      'X-RapidAPI-Key': 'key aca',
      'X-RapidAPI-Host': 'utelly-tv-shows-and-movies-availability-v1.p.rapidapi.com'
    }
  };
  
  axios.request(options).then(function (response) {
      var jsonContent = JSON.stringify(response.data,null,3);
      fs.writeFile('../utelly-jsons/'+SOURCE+'.json', jsonContent, 'utf8', function (err) {
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