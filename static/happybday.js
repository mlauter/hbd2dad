var map;

function initialize() {
  var mapOptions = {
    zoom: 3,
    center: { lat: 35.434588, lng: -40.777965},
    mapTypeId: google.maps.MapTypeId.TERRAIN
  };

  map = new google.maps.Map(document.getElementById('map-canvas'),
      mapOptions);

  var contentString = '<div id="content">'+
      '<div id="siteNotice">'+
      '</div>'+
      '<h1 id="firstHeading" class="firstHeading">Happy birthday Dad!</h1>'+
      '<div id="bodyContent">'+
      '<p>At (almost) any given moment, ' +
      'someone, somewhere in the world '+
      'is wishing someone else '+
      'a happy birthday... '+
      'on Twitter. '+
      'Watch happy birthday tweets appear live '+
      'on this map.</p>'+
      '<p>Love, Miriam</p>'+
      '</div>'+
      '</div>';

  var infowindow = new google.maps.InfoWindow({
      content: contentString,
      position: { lat: 35.434588, lng: -40.777965},
      draggable: true,
      maxWidth: 150
  });

  infowindow.open(map)

  // Set the firebase reference
  var coordsRef = new Firebase('https://happybirthdaydad.firebaseio.com/processed_coords');

  coordsRef.on('child_added', function(childSnapshot, prevChildName) {
    // code to handle new child.
    var lng = childSnapshot.child(0).val()
    var lat = childSnapshot.child(1).val()
    var icon = new google.maps.MarkerImage(
        'images/bday_candle_icon.png',
        new google.maps.Size(10,52),    // size of the image
        new google.maps.Point(0,0), // origin, in this case top-left corner
        new google.maps.Point(5, 52)    // anchor, i.e. the point half-way along the bottom of the image
    );
    var marker = new google.maps.Marker({
      position: {lat: lat, lng: lng},
      icon: icon,
      map: map,
    });
  });
}

google.maps.event.addDomListener(window, 'load', initialize);
