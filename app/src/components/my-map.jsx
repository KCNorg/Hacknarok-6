import React, { useEffect } from 'react'; 
import './my-map.scss';
import maplibre from 'maplibre-gl';

function addMarker(map) {
    // Zürich Airport, icon size: 47 x 69px, shadow adds: 6px
    // lat: 47.46101649104483, lon: 8.551922366826949
    var airportIcon = document.createElement('div');
    airportIcon.classList.add("airport");

    var airportPopup = new maplibre.Popup({
        anchor: 'bottom',
        offset: [0, -64] // height - shadow
      })
      .setText('Zürich Airport');
    
    var airport = new maplibre.Marker(airportIcon, {
        anchor: 'bottom',
        // offset: [0, 6]
      })
      .setLngLat([8.551922366826949, 47.46101649104483])
      .setPopup(airportPopup)
      .addTo(map);


}

function MyMap(props) {
  let mapContainer;

  useEffect(() => {
    const myAPIKey = '05a786c10b224977937d2a9a5f16fd40'; 
    const mapStyle = 'https://maps.geoapify.com/v1/styles/osm-bright-grey/style.json';

    const initialState = {
      lng: 11,
      lat: 49,
      zoom: 10
    };

    const map = new maplibre.Map({
      container: mapContainer,
      style: `${mapStyle}?apiKey=${myAPIKey}`,
      center: [initialState.lng, initialState.lat],
      zoom: initialState.zoom
      });

    addMarker(map)

  }, [mapContainer]);

  return (
    <div className="map-container" ref={el => mapContainer = el}>
    </div>
  )
}

export default MyMap;