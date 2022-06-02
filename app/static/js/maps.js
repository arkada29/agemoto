function myMap(){
    // var mapProp= {
    // center:new google.maps.LatLng(-7.733214725641418, 110.3932098432415),
    // zoom:18,
    // };
    var myLatlng = {lat:-7.733383122994405, lng:110.39315303531252};
    map = new google.maps.Map(document.getElementById("googleMap"),{
        zoom:18,
        center:myLatlng,
        mapTypeId: google.maps.MapTypeId.ROADMAP
    });

    var marker;
    const infowindow = new google.maps.InfoWindow({});

    marker = new google.maps.Marker({
        position: myLatlng,
        map,
        title: 'address',
        // animation:google.maps.Animation.BOUNCE
    });

    google.maps.event.addListener(marker,'click',function() {
    //   map.setZoom(9);
    //   map.setCenter(marker.getPosition());
        const content = document.createElement("div");
        const nameElement = document.createElement("h4");
        nameElement.textContent = 'Ada-Dev Team';
        content.appendChild(nameElement)

        const placeElement = document.createElement("p");
        placeElement.textContent = 'Location : Jl. Dayu Baru No. 8'
        content.appendChild(placeElement)

        infowindow.setContent(content)
        infowindow.open(map, marker);
    });
};

