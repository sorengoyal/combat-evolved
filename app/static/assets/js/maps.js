var map;
function initMap() {
    //Constructor: Creates a new map. Only zoom and corrdinates a required
    map = new google.maps.Map(document.getElementById('map'),{
            center: {lat:40.7413549, lng: -73.9980244},
            zoom: 20
    });
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