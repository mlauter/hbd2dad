var map;

function initialize() {
  var mapOptions = {
    zoom: 2,
    center: { lat: 2.8, lng: -187.3},
    mapTypeId: google.maps.MapTypeId.TERRAIN
  };

  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

  // Create a script tag and set the USGS URL as the source.
  var script = document.createElement('script');
  script.src = 'http://earthquake.usgs.gov/earthquakes/feed/geojsonp/2.5/week';
  var s = document.getElementsByTagName('script')[0];
  console.log(script);
  s.parentNode.insertBefore(script, s);
}

window.eqfeed_callback = function(results) {
  for (var i = 0; i < results.features.length; i++) {
    var coords = results.features[i].geometry.coordinates;
    var icon = new google.maps.MarkerImage(
        'images/bday_candle_icon.png',
        new google.maps.Size(10,52),    // size of the image
        new google.maps.Point(0,0), // origin, in this case top-left corner
        new google.maps.Point(5, 52)    // anchor, i.e. the point half-way along the bottom of the image
    );
    var marker = new google.maps.Marker({
      position: {lat: coords[1], lng: coords[0]},
      icon: icon,
      map: map,
    });
  }
}



google.maps.event.addDomListener(window, 'load', initialize);
