// the google map that we're using for display
var map;

// An infoWindow to show the information about the incident
var infoWindow = new google.maps.InfoWindow;

// an initial location (centre of Cardiff - can't say we're not biased :-D)
var initialLocation = new google.maps.LatLng(51.481307,-3.18049860);

var geocoder = new google.maps.Geocoder();

var count = 1;

var circles = [];
var tweets = [];

var weather = ['','Fine, no wind', 'Raining, no wind', 'Snowing, no wind', 'Fine + high winds', 'Raining + high winds', 'Snowing + high winds', 'Fog or mist', 'Other', 'Unknown'  ]
var roadSurface = ['', 'Dry', 'Wet or damp', 'Snow', 'Frost or ice', 'Flood over 3cm', 'Oil or Diesel', 'Mud']

var selectedCircle;
var selectedTweet;


// initialise the map within a webpage
//
// map is inserted into 'map_location'
function setmap(map_location) {

    // initial zoom level and type of map
    var myOptions = {
        zoom: 14,
        minZoom: 12,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    };

    // create map
    map = new google.maps.Map(map_location, myOptions);

    // Geolocation to get centre of map
    // Try W3C Geolocation (Preferred)
    if(navigator.geolocation) 
    {
        browserSupportFlag = true;
        navigator.geolocation.getCurrentPosition(function(position) {
            initialLocation = new google.maps.LatLng(position.coords.latitude,position.coords.longitude);
            map.setCenter(initialLocation);
        }, function() {
            handleNoGeolocation(browserSupportFlag);
        });
    // Try Google Gears Geolocation
    } else if (google.gears) {
        browserSupportFlag = true;
        var geo = google.gears.factory.create('beta.geolocation');
        geo.getCurrentPosition(function(position) {
            initialLocation = new google.maps.LatLng(position.latitude,position.longitude);
            map.setCenter(initialLocation);
        }, function() {
            handleNoGeoLocation(browserSupportFlag);
        });
    // Browser doesn't support Geolocation
    } else {
        browserSupportFlag = false;
        handleNoGeolocation(browserSupportFlag);
    }

    google.maps.event.addListener(map, 'idle', changeBounds);
    google.maps.event.addListener(map, 'zoom_changed', changeZoom);
    getTweets();
    return map;
}

function changeZoom() {
   changeRadii();
}

function changeRadii() {
    zoom = map.getZoom();
    radius = getRadius(zoom);
    for(i in circles) {
        circles[i].setOptions({
            radius: radius,
        });
    }
}

// set the centre of the map to be Cardiff if geo-location failed
function handleNoGeolocation(errorFlag) {
    map.setCenter(initialLocation);
}

// function called when the map is moved
function changeBounds() {
    //deleteOverlays();
    getAccidents();
    hideMarkers();
    getAccidents();
    showMarkers();
}

function hideMarkers() {
    bounds = map.getBounds();
    if(circles) {
        for(i in circles) {
            if(!bounds.contains(circles[i].getCenter())) {
                circles[i].setMap(null);
            }
        }
    }
    if(tweets) {
        for(i in tweets) {
            if(!bounds.contains(tweets[i].position)) {
                tweets[i].setMap(null);
            }
        }
    }  
}

function getAccidents() {
    var bounds = map.getBounds();
    var northEast = bounds.getNorthEast();
    var southWest = bounds.getSouthWest();
    var url = "api/accidents_in_rect?ne=" + northEast.lat() + "," + northEast.lng() + "&sw=" + southWest.lat() + "," + southWest.lng() + "&Road_Surface_Conditions=3,4";
    $.getJSON(url, {}, function(data){
        for(i in data) {
            var infostring = '';
            infostring += "<div class='incident'>Time of accident: " + data[i]['datetime'] + "<br />";
            if(data[i]['Weather_Conditions'] != -1) {
                infostring += "Weather Conditions: " + weather[data[i]['Weather_Conditions']];    
            }
            infostring += "<br />"
            if(data[i]['Road_Surface_Conditions'] != -1) {
                infostring += "Road Surface Conditions: " + roadSurface[data[i]['Road_Surface_Conditions']];
            }
            infostring += "<br />"
            if(data[i]['Number_of_Vehicles'] != -1) {
                infostring += "Number of Vehicles: " + data[i]['Number_of_Vehicles'];
            }
            infostring += "<br />"
            infostring += "</div>";    
            circle = addCircle(data[i]['Latitude'], data[i]['Longitude'], data[i]['Accident_Severity'], infostring);
        }
    });
    
}

function getTweets() {
    var url = "api/freezetweets_national";
    $.getJSON(url, {}, function(data) {
        for(i in data) {
            var location = data[i]['postcode_loc'];
            var text = data[i]['clean'];
            var infostring = '';  
            infostring += "<div class='incident'>";
            infostring += "<h1>" + data[i]['author'] + "</h1>"
            infostring += "<img class='avatar' src=" + data[i]['avatar_url'] + " />"
            infostring +=  "<p class='tweet'>" + text + "</p>"
            infostring += "</div>"
            infostring += "<div class='clear'></div>"
            addTweet(location[0], location[1], text, infostring);
        }
    });
}

function showMarkers() {
    bounds = map.getBounds();
    if(circles) {
        for(i in circles) {
            if(bounds.contains(circles[i].getCenter()) && circles[i].getMap() == null) {
                circles[i].setMap(map);
            }
        }
    }
    if(tweets) {
        for(i in tweets) {
            if(bounds.contains(tweets[i].position)  && circles[i].getMap() == null) {
                tweets[i].setMap(map);
            }
        }
    }    
}

function deleteOverlays() {
    if(circles) {
        for(i in circles) {
            circles[i].setMap(null);
        }
        circles.length=0;
    }
    if(tweets) {
        for(i in tweets) {
            tweets[i].setMap(null);
        }
        tweets.length=0;
    }
}

function getMapBounds() {
    var bounds = map.getBounds();
    return bounds;
}

function getRadius(zoom) {
    switch(zoom) {
        case 12:
            return 250;
            break;
        case 13:
            return 100;
            break;
        case 14:
            return 50;
            break;
        case 15:
            return 40;
            break;
        case 16:
            return 35;
            break;
        case 17:
            return 30;
            break;
        case 18:
            return 20;
            break;
        case 19:
            return 10;
            break;
        case 20:
            return 5;
            break;
    }

}

function addTweet(lat, lng, tweet, infostring) {
    found = false;
    for(i in tweets) {
        if(tweets[i].title == tweet) {
            found = true;
        }
    }
    if(!found) {
        var image = new google.maps.MarkerImage(
            "https://si0.twimg.com/images/dev/cms/intents/bird/bird_blue/bird_32_blue.png",
            new google.maps.Size(32, 32),
            new google.maps.Point(0, 0),
            new google.maps.Point(16, 32),
            new google.maps.Size(24,24)
        );
        var selectedImage = new google.maps.MarkerImage(
            "https://si0.twimg.com/images/dev/cms/intents/bird/bird_black/bird_32_black.png",
            new google.maps.Size(32, 32),
            new google.maps.Point(0, 0),
            new google.maps.Point(16, 32),
            new google.maps.Size(24,24)
        );
        var marker = new google.maps.Marker({
            position: new google.maps.LatLng(lat, lng),
            map: map,
            title: tweet,
            icon: image,
        });
        tweets.push(marker);
        google.maps.event.addListener(marker, 'click', function(event){
            if(selectedCircle) {
                selectedCircle.setOptions({
                    strokeWeight: 1,
                })
                selectedCircle = null;
            }
            if(selectedTweet) {
                selectedTweet.setIcon(image);
            }
            selectedTweet = marker;
            selectedTweet.setIcon(selectedImage);
           $('#info').html(infostring);
        });
    }
    return marker;
}

function addCircle(lat, lng, severity, infostring) {
    var found = false;
    var position = new google.maps.LatLng(lat, lng);
    for(i in circles) {
        if(circles[i].getCenter().lat() == position.lat() && circles[i].getCenter().lng() == position.lng()) {
            found = true;
            return circles[i];
        }
    }
    if(!found) {
        var image = new google.maps.MarkerImage(
            "https://si0.twimg.com/images/dev/cms/intents/bird/bird_blue/bird_32_blue.png",
            new google.maps.Size(32, 32),
            new google.maps.Point(0, 0),
            new google.maps.Point(16, 32),
            new google.maps.Size(24,24)
        );
        var circle = new google.maps.Circle({
            center: position,
            radius: getRadius(map.getZoom()),
            strokeWeight: 1,
        });
        if(severity === 1) {
            circle.setOptions({
                fillColor: 'Red',
                fillOpacity: 0.85,
                strokeColor: 'DarkRed',
            });
        } else if(severity === 2) {
            circle.setOptions({
                fillColor: 'Orange',
                fillOpacity: 0.60,
                strokeColor: 'DarkOrange',
            });        
        }
        else if(severity === 3) {
            circle.setOptions({
                fillColor: 'Yellow',
                fillOpacity: 0.3,
                strokeColor: 'GoldenRod',
            });        
        }
        circle.setMap(map);
        google.maps.event.addListener(circle, 'click', function(event){
            if(selectedCircle) {
                selectedCircle.setOptions({
                    strokeWeight: 1,
                })
            }
            if(selectedTweet) {
                selectedTweet.setIcon(image);
                selectedTweet = null;
            }
            selectedCircle = circle;
            selectedCircle.setOptions({
                strokeWeight: 3,
            });
           $('#info').html(infostring);
        });
        circles.push(circle);
        return circle;
    }
}