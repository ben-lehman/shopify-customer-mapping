function getResponse(endpoint) {
  console.log("Getting Response")
  return fetch(endpoint)
      .then(function(response) {
        return response.json();
      });
}

function logLocations(locations) {
  console.log("logging.");
  // console.log(locations);
  for(var i = 0; i < locations.length; i++) {
    console.log(locations[i]['name']);
  }
}

function addMarkers(map, locations) {
  for(var i = 0; i < locations.length; i++) {
    let lng = locations[i]['longitude'];
    let lat = locations[i]['latitude'];
    console.log(lng, + " ", + lat);
    console.log(map);
    L.marker([lat, lng]).addTo(map);
  }
}

function failureCallback(error) {
  console.log("Error getting locations: " + error);
}


function run() {
    let accessToken = "pk.eyJ1IjoiYmVubGVobWFuIiwiYSI6ImNqeHc2YThpMjBjZXIzYnFzcjczbnRqaWoifQ.lxxzkqRpnwBXpkvbOaKrpA"
    let mymap = new L.map('mapid').setView([37.09, -95.7129], 4);

    L.tileLayer(`https://api.tiles.mapbox.com/v4/{id}/{z}/{x}/{y}.png?access_token=${accessToken}`, {
      attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors, <a href="https://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="https://www.mapbox.com/">Mapbox</a>',
      maxZoom: 18,
      id: 'mapbox.streets',
      accessToken: 'your.mapbox.access.token'
    }).addTo(mymap);

    let endpoint = 'http://localhost:5000/api/orders'

    let loc_response = getResponse(endpoint);
    loc_response.then(addMarkers.bind(null, mymap), failureCallback);

}

// in case the document is already rendered
if (document.readyState!='loading') run();
// modern browsers
else if (document.addEventListener) document.addEventListener('DOMContentLoaded', run);
// IE <= 8
else document.attachEvent('onreadystatechange', function(){
    if (document.readyState=='complete') run();
});
