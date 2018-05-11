(function ($) {
  var map,                                      // This is the Google map
    clientMarker,                               // The current marker when we are following a single client
    overlay,                                    // Map Image Overlay
    clientUncertaintyCircle,                    // The circle describing that client's location uncertainty
    lastEvent,                                  // The last scheduled polling task
    lastInfoWindowMac,                          // The last Mac displayed in a marker tooltip
    allMarkers = [],                            // The markers when we are in "View All" mode
    lastMac = "",                               // The last requested MAC to follow
    infoWindow = new google.maps.InfoWindow(),  // The marker tooltip
    markerImage = new google.maps.MarkerImage('/static/blue_circle.png',
      new google.maps.Size(15, 15),
      new google.maps.Point(0, 0),
      new google.maps.Point(4.5, 4.5)),
    rotation='';

      CMXOverlay.prototype = new google.maps.OverlayView();


      eventSource = new EventSource("/notification_stream");
      eventSource.onmessage = function(e) {
        var client = JSON.parse(e.data);
        track(client.notifications["0"]);
      }

  // Removes all markers
  function clearAll() {
    clientMarker.setMap(null);
    clientUncertaintyCircle.setMap(null);
    lastInfoWindowMac = "";
    var m;
    while (allMarkers.length !== 0) {
      m = allMarkers.pop();
      if (infoWindow.anchor === m) {
        lastInfoWindowMac = m.mac;
      }
      m.setMap(null);
    }
  }

  // Plots the location and uncertainty for a single MAC address
  function track(client) {
    if (client !== null && client.geoCoordinate !== null && !(typeof client.geoCoordinate === 'undefined') && client.locationMapHierarchy === hierarchy) {
      var pos = new google.maps.LatLng(client.geoCoordinate.latitude, client.geoCoordinate.longitude);

      if (client.ssid != null) {
        ssidStr = " with SSID '" + client.ssid + "'";
      } else {
        ssidStr = "";
      }
      if (client.locationMapHierarchy != null && client.locationMapHierarchy
        !== "") {
        floorStr = " at '" + client.locationMapHierarchy + "'"
      } else {
        floorStr = "";
      }
      var confidenceFactor = client.confidenceFactor/10;
      $('#last-mac').text(client.deviceId + " " + ssidStr +
        " last seen on " + client.lastSeen + floorStr +
        " with uncertainty " + confidenceFactor.toFixed(1) + " feet");

      var whichMarker = allMarkers.find(function (whichMarker) {
        if (whichMarker.mac === client.deviceId) {
          whichMarker.setMap(map);
          whichMarker.setPosition(pos);
        }
      });

      //In case it's a new client
      if (typeof whichMarker === 'undefined'){
        addMarker(client);
      }


    } else {
      $('#last-mac').text("Client '" + lastMac + "' could not be found");
    }
  }

  // Looks up a single MAC address
  function lookup(mac) {
    $.getJSON('/clients/' + mac, function (response) {
      track(response);
    });
  }

  // Adds a marker for a single client within the "view all" perspective
  function addMarker(client) {
    if (client !== null && client.geoCoordinate !== null && !(typeof client.geoCoordinate === 'undefined' && client.locationMapHierarchy === hierarchy)){
      var m = new google.maps.Marker({
        position: new google.maps.LatLng(client.geoCoordinate.latitude, client.geoCoordinate.longitude),
        map: map,
        mac: client.deviceId,
        icon: markerImage
      });
      google.maps.event.addListener(m, 'click', function () {
        infoWindow.setContent("<div>" + client.deviceId + "</div> (<a class='client-filter' href='#' data-mac='" +
          client.deviceId + "'>Follow this client)</a>");
        infoWindow.open(map, m);
      });
      if (client.deviceId === lastInfoWindowMac) {
        infoWindow.open(map, m);
      }
      var pos = new google.maps.LatLng(client.geoCoordinate.latitude, client.geoCoordinate.longitude);
      //map.setCenter(pos);
      clientMarker.setMap(map);
      clientMarker.setPosition(pos);
      allMarkers.push(m);
    }
  }


  // Displays markers for all clients
  function trackAll() {
    clearAll();
    var clients = JSON.parse(clientsraw);
    clientUncertaintyCircle.setMap(null);
    for (var i = 0, len = clients.length; i < len; i++) {
      addMarker(clients[i]);
    }
  }


  // This is called after the DOM is loaded, so we can safely bind all the
  // listeners here.
  function initialize() {
    srcImage = '/static/' + mapImages[0].imageName;
    hierarchy = mapImages[0].hierarchy;
    gpsMarkers = mapImages[0].gpsMarkers;

    var bottomleft = new google.maps.LatLng(41.356150, 2.134081);
    var topleft = new google.maps.LatLng(41.356321, 2.134551);
    var bottomright = new google.maps.LatLng(41.355349, 2.134653);
    var topright = new google.maps.LatLng(41.355513, 2.135130);

    var imageMapWidth = google.maps.geometry.spherical.computeDistanceBetween(bottomleft,bottomright);

    var imageMapHeight = google.maps.geometry.spherical.computeDistanceBetween(bottomleft, topleft);

    //var imageMapCenter = google.maps.geometry.spherical.interpolate(new google.maps.LatLng(gpsMarkers.bottomleft), new google.maps.LatLng(gpsMarkers.topright)), 0.5);

    var imageMapCenter = google.maps.geometry.spherical.interpolate(bottomleft,topright, 0.5);


    var bottomMapHeading = google.maps.geometry.spherical.computeHeading(bottomleft,bottomright)-90;


    rotation = "rotate(" + bottomMapHeading.toString() + "deg)"

    var leftSide = google.maps.geometry.spherical.computeOffset(imageMapCenter, imageMapWidth/2, 270);


    var swBound = google.maps.geometry.spherical.computeOffset(leftSide, imageMapHeight/2, 180);


    var rightSide = google.maps.geometry.spherical.computeOffset(imageMapCenter, imageMapWidth/2, 90);


    var neBound = google.maps.geometry.spherical.computeOffset(rightSide, imageMapHeight/2, 0);


    var mapOptions = {
      zoom: 18,
      center: imageMapCenter
    };

    var bounds = new google.maps.LatLngBounds(
      swBound,
      neBound);


    map = new google.maps.Map(document.getElementById('map-canvas'), mapOptions);

    clientMarker = new google.maps.Marker({
      position: imageMapCenter,
      icon: markerImage
    });
    clientUncertaintyCircle = new google.maps.Circle({
      position: imageMapCenter
    });

    overlay = new CMXOverlay(bounds, srcImage, map);

    trackAll();

  }

  /** @constructor */

  function CMXOverlay(bounds, image, map) {

    // Initialize all properties.
    this.bounds_ = bounds;
    this.image_ = image;
    this.map_ = map;

    // Define a property to hold the image's div. We'll
    // actually create this div upon receipt of the onAdd()
    // method so we'll leave it null for now.
    this.div_ = null;

    // Explicitly call setMap on this overlay.
    this.setMap(map);
  }

  /**
   * onAdd is called when the map's panes are ready and the overlay has been
   * added to the map.
   */
  CMXOverlay.prototype.onAdd = function() {

    var div = document.createElement('div');
    div.style.borderStyle = 'none';
    div.style.borderWidth = '0px';
    div.style.position = 'absolute';


    // Create the img element and attach it to the div.
    var img = document.createElement('img');
    img.src = this.image_;
    img.style.width = '100%';
    img.style.height = '100%';
    img.style.position = 'absolute';
    div.appendChild(img);
    div.style.transform = rotation;

    this.div_ = div;

    // Add the element to the "overlayLayer" pane.
    var panes = this.getPanes();
    panes.overlayLayer.appendChild(div);
  };

  CMXOverlay.prototype.draw = function() {

    // We use the south-west and north-east
    // coordinates of the overlay to peg it to the correct position and size.
    // To do this, we need to retrieve the projection from the overlay.
    var overlayProjection = this.getProjection();

    // Retrieve the south-west and north-east coordinates of this overlay
    // in LatLngs and convert them to pixel coordinates.
    // We'll use these coordinates to resize the div.
    var sw = overlayProjection.fromLatLngToDivPixel(this.bounds_.getSouthWest());
    var ne = overlayProjection.fromLatLngToDivPixel(this.bounds_.getNorthEast());

    // Resize the image's div to fit the indicated dimensions.
    var div = this.div_;
    div.style.left = sw.x + 'px';
    div.style.top = ne.y + 'px';
    div.style.width = (ne.x - sw.x) + 'px';
    div.style.height = (sw.y - ne.y) + 'px';
  };

  // The onRemove() method will be called automatically from the API if
  // we ever set the overlay's map property to 'null'.
  CMXOverlay.prototype.onRemove = function() {
    this.div_.parentNode.removeChild(this.div_);
    this.div_ = null;
  };

  // Call the initialize function when the window loads
  $(window).load(initialize);
  //google.maps.event.addDomListener(window, 'load', initialize);


  //If has gps coordinates and "on world map" selected, google map view only


  //If has gps coordinates and "overlay floor map" selected, google map view + floor overlay


  //If doesn't have gps coordinates "on world map" is not an check box option and only show image map and devices on that map


}(jQuery));
