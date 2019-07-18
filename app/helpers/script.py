script = """function getResponse(endpoint) {
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
  let myIcon = new L.divIcon({className: 'my-div-icon'});

  for(var i = 0; i < locations.length; i++) {
    let lng = locations[i]['lng'];
    let lat = locations[i]['lat'];
    console.log(lng, + " ", + lat);
    L.marker([lat, lng], {icon: myIcon}).addTo(map);
  }
}

function failureCallback(error) {
  console.log("Error getting locations: " + error);
}


function run() {
    let accessToken = "pk.eyJ1IjoiYmVubGVobWFuIiwiYSI6ImNqeHc2YThpMjBjZXIzYnFzcjczbnRqaWoifQ.lxxzkqRpnwBXpkvbOaKrpA"
    let mymap = new L.map('mapid').setView([37.09, -95.7129], 4);

    L.tileLayer('https://{s}.basemaps.cartocdn.com/light_all/{z}/{x}/{y}{r}.png', {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors &copy; <a href="https://carto.com/attributions">CARTO</a>',
      subdomains: 'abcd',
      maxZoom: 19
    }).addTo(mymap);
    addMarkers(mymap, data)
}

if (document.readyState!='loading') run();

else if (document.addEventListener) document.addEventListener('DOMContentLoaded', run);

else document.attachEvent('onreadystatechange', function(){
    if (document.readyState=='complete') run();
});"""