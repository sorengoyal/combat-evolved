var overlay;
USGSOverlay.prototype = new google.maps.OverlayView();

function initMap() {
    style = [
    {
        "stylers": [
            {
                "visibility": "on"
            },
            {
                "saturation": -100
            },
            {
                "gamma": 0.54
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "water",
        "stylers": [
            {
                "color": "#4d4946"
            }
        ]
    },
    {
        "featureType": "poi",
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "poi",
        "elementType": "labels.text",
        "stylers": [
            {
                "visibility": "simplified"
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "geometry.fill",
        "stylers": [
            {
                "color": "#ffffff"
            }
        ]
    },
    {
        "featureType": "road.local",
        "elementType": "labels.text",
        "stylers": [
            {
                "visibility": "simplified"
            }
        ]
    },
    {
        "featureType": "water",
        "elementType": "labels.text.fill",
        "stylers": [
            {
                "color": "#ffffff"
            }
        ]
    },
    {
        "featureType": "transit.line",
        "elementType": "geometry",
        "stylers": [
            {
                "gamma": 0.48
            }
        ]
    },
    {
        "featureType": "transit.station",
        "elementType": "labels.icon",
        "stylers": [
            {
                "visibility": "off"
            }
        ]
    },
    {
        "featureType": "road",
        "elementType": "geometry.stroke",
        "stylers": [
            {
                "gamma": 7.18
            }
        ]
    }];
    var map;
    var drawingManager;
    var polygon;;
    //Constructor: Creates a new map. Only zoom and corrdinates a required
    map = new google.maps.Map(document.getElementById('map'),{
            center: {lat:37.805749114187385, lng: -122.3170486831665,},
            zoom: 13,
            styles: style
    });
    
    drawingManager = new google.maps.drawing.DrawingManager({
        drawingMode: google.maps.drawing.OverlayType.POLYGON,
        drawingControl: true,
        drawingControlOptions: {
            position:google.maps.ControlPosition.TOP_LEFT,
            drawingModes: [
                google.maps.drawing.OverlayType.POLYGON
            ]
        }
    });
    drawingManager.setMap(map)

    drawingManager.addListener('overlaycomplete', function(event) {
        // First, check if there is an existing polygon.
        // If there is, get rid of it and remove the markers
        if (polygon) {
          polygon.setMap(null);
          path = null;
        }
        // Switching the drawing mode to the HAND (i.e., no longer drawing).
        drawingManager.setDrawingMode(null);
        // Creating a new editable polygon from the overlay.
        polygon = event.overlay;
        polygon.setEditable(false);
        path = polygon.getPath().b;
        console.log(path);
        var sLat = path[0].lat(), nLat = path[0].lat(); //lat goes from -90 to +90 (south to north)
        var wLng = path[0].lng(), eLng = path[0].lng(); //lng goes from -180 to +180 (west to east)
        //The coordinates are set to maximum extent possible
        for(var i = 1; i < path.length; i++){
            if(path[i].lat() < sLat){
                sLat = path[i].lat();
            }
            if(path[i].lat() > nLat){
                nLat = path[i].lat();
            }
            if(path[i].lng() < wLng){
                wLng = path[i].lng();
            }
            if(path[i].lng() > eLng){
                eLng = path[i].lng();
            }
        }
        var swLatLng = new google.maps.LatLng({lat: sLat, lng: wLng});
        var neLatLng = new google.maps.LatLng({lat: nLat, lng: eLng});
        var bounds = new google.maps.LatLngBounds(swLatLng, neLatLng);
        map.fitBounds(bounds);
        sendPolygon(path, function(){
          var srcImage = 'file0.png';
          inner = document.getElementsByClassName("inner")[0];
          inf = document.getElementById("information");
          inner.setAttribute("style", "width:30rem; height: 15rem");
          inf.innerHTML = "";
          var img = document.createElement('img');
          img.src = "graph.png";
          img.style.width = '100%';
          img.style.height = '100%';
          img.style.position = 'relative';
          inf.appendChild(img)
          overlay = new USGSOverlay(bounds, srcImage, map);
        });
        
        // The custom USGSOverlay object contains the USGS image,
        // the bounds of the image, and a reference to the map.
        //poll();
        
    });
    
}
/*        
function populateInfoWindow(marker, infoWindow){
    if(infoWindow.marker != marker){
        infoWindow.marker = marker;
        infoWindow.setContent('<div>' + marker.title + '</div>');
        infoWindow.open(map, marker);
        infoWindow.addListener('closeclick', function(){
            infoWindow.marker == null;
        });
    }        
}
*/
function sendPolygon(polygon, callback) {
    var xhr = new XMLHttpRequest();
    var url = window.location.origin + "/polygon";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json");
    var data = JSON.stringify({"polygon": polygon});
    console.log(data)
    xhr.onreadystatechange = function() { 
        if (xhr.readyState == 4 && xhr.status == 200)
            console.log(xhr.responseText);
            callback();
    }
    xhr.send(data);
}
/*
function displayImage(bounds){
  var bounds = {
          17: [[20969, 20970], [50657, 50658]],
          18: [[41939, 41940], [101315, 101317]],
          19: [[83878, 83881], [202631, 202634]],
          20: [[167757, 167763], [405263, 405269]]
        };

        var imageMapType = new google.maps.ImageMapType({
          getTileUrl: function(coord, zoom) {
            if (zoom < 17 || zoom > 20 ||
                bounds[zoom][0][0] > coord.x || coord.x > bounds[zoom][0][1] ||
                bounds[zoom][1][0] > coord.y || coord.y > bounds[zoom][1][1]) {
              return null;
            }

            return ['',
                zoom, '_', coord.x, '_', coord.y, '.png'].join('');
          },
          tileSize: new google.maps.Size(256, 256)
        });

        map.overlayMapTypes.push(imageMapType);
}
*/

function httpGetAsync(url, callback) {
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.onreadystatechange = function() { 
        if (xmlHttp.readyState == 4 && xmlHttp.status == 200)
            callback(xmlHttp.responseText);
    }
    xmlHttp.open("GET", url, true); // true for asynchronous 
    xmlHttp.send(null);
}

function poll(){
  var url = window.location.origin + "/poll";
  var status = 0;
  httpGetAsync(url, function(text){
      status = JSON.parse(text).status;
      console.log(status);
      if(status < 25){
        setTimeout(poll, 1500);
      }
  });
}
/** @constructor */
function USGSOverlay(bounds, image, mymap) {
  // Initialize all properties.
  this.bounds_ = bounds;
  this.image_ = image;
  this.map_ = mymap;
  // Define a property to hold the image's div. We'll
  // actually create this div upon receipt of the onAdd()
  // method so we'll leave it null for now.
  this.div_ = null;
  // Explicitly call setMap on this overlay.
  this.setMap(mymap);
}

/**
 * onAdd is called when the map's panes are ready and the overlay has been
 * added to the map.
 */
USGSOverlay.prototype.onAdd = function() {
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
  this.div_ = div;
  // Add the element to the "overlayLayer" pane.
  var panes = this.getPanes();
  panes.overlayLayer.appendChild(div);
};

USGSOverlay.prototype.draw = function() {
  // We use the south-west and north-east
  // coordinates of the overlay to peg it to the correct position and size.
  // To do this, we need to retrieve the projection from the overlay.
  var overlayProjection = this.getProjection();
  // Retrieve the south-west and north-east coordinates of this overlay
  // in LatLngs and convert them to pixel coordinates.
  // We'll use these coordinates to resize the div.
  console.log(this.bounds_);
  var sw = overlayProjection.fromLatLngToDivPixel(this.bounds_.getSouthWest());
  var ne = overlayProjection.fromLatLngToDivPixel(this.bounds_.getNorthEast());
  console.log('sw' + sw);
  console.log('ne' + ne);
  // Resize the image's div to fit the indicated dimensions.
  var div = this.div_;
  div.style.left = sw.x + 'px';
  div.style.top = ne.y + 'px';
  div.style.width = (ne.x - sw.x) + 'px';
  div.style.height = (sw.y - ne.y) + 'px';
  console.log(div);
};

// The onRemove() method will be called automatically from the API if
// we ever set the overlay's map property to 'null'.
USGSOverlay.prototype.onRemove = function() {
  this.div_.parentNode.removeChild(this.div_);
  this.div_ = null;
};

google.maps.event.addDomListener(window, 'load', initMap);
