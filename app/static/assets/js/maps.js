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
            center: {lat:37.805749114187385, lng: -122.4270486831665,},
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
        sendPolygon(path);
    });
    
}
        
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

function sendPolygon(polygon) {
    var xhr = new XMLHttpRequest();
    var url = window.location.origin + "/polygon";
    xhr.open("POST", url, true);
    xhr.setRequestHeader("Content-type", "application/json");
    var data = JSON.stringify({"polygon": polygon});
    console.log(data)
    xhr.send(data);
}

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


