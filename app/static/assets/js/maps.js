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
            center: {lat:40.7413549, lng: -73.9980244},
            zoom: 20,
            styles: style
    });
    debugger;
    var center = {lat:40.7413549, lng: -73.9980244};
    var locations = [
            {title: "Neil Ave Apartments", location:{lat:40.7413549, lng:-73.998024}},
            {title: "Top Right Kill", location:{lat:40.7413559, lng:-73.998034}},
            {title: "Open Heart Surgery", location:{lat:40.7413539, lng:-73.998014}},
            {title: "Kill Bill Vol 2", location:{lat:40.7413539, lng:-73.998034}},
            {title: "Ninety Percenty Kill Rate", location:{lat:40.7413559, lng:-73.998014}}
            ];
    var infoWindow = new google.maps.InfoWindow();
    var markers = [];
    for(var i = 0; i < locations.length; i++){
        var marker = new google.maps.Marker({
        position: locations[i].location,
        map: map,
        title: locations[i].title,
        animation: google.maps.Animation.DROP,
        id: i
        });
        marker.addListener('click', function(){
            populateInfoWindow(this, infoWindow);
        });
        markers.push(marker);
    }
    
    
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
    
    document.getElementById('toggle-drawing').addEventListener('click', function() {
          toggleDrawing(drawingManager);
        });
    var path = null;
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
          // Searching within the polygon.
          path = polygon.getPath().b;
          for(var i = 0; i < path.length; i++){
            console.log(path[i].lat() + ',' + path[i].lng());
            }
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

function toggleDrawing(drawingManager) {
        if (drawingManager.map) {
          drawingManager.setMap(null);
          // In case the user drew anything, get rid of the polygon
          if (polygon !== null) {
            polygon.setMap(null);
          }
        } else {
          drawingManager.setMap(map);
        }
      }



