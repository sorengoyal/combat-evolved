var map;
var drawingManager;
var polygon;;
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
    }
];
    
    //Constructor: Creates a new map. Only zoom and corrdinates a required
    map = new google.maps.Map(document.getElementById('map'),{
            center: {lat:37.805749114187385, lng: -122.4270486831665,},
            zoom: 13,
            styles: style
    });
    
    //var center = {lat:40.7413549, lng: -73.9980244};
    
    
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
    /*
    xhr.onreadystatechange = function () {
        if (xhr.readyState === 4 && xhr.status === 200) {
        var json =  JSON.parse(xhr.responseText);
            console.log(json.polygon );
            }
    }; */
    var data = JSON.stringify({"polygon": polygon});
    console.log(data)
    xhr.send(data);
}
/*
var imageMapType = new google.maps.ImageMapType({
    getTileUrl: function(coord, zoom) {
    if (zoom < 17 || zoom > 20 ||
        bounds[zoom][0][0] > coord.x || coord.x > bounds[zoom][0][1] ||
        bounds[zoom][1][0] > coord.y || coord.y > bounds[zoom][1][1]) {
          return null;
        }

    return ['overlay.png',
            zoom, '_', coord.x, '_', coord.y, '.png'].join('');
      },
      tileSize: new google.maps.Size(256, 256)
    });

    map.overlayMapTypes.push(imageMapType);
}
*/

