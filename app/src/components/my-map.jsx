import React, { useEffect } from 'react'; 
import './my-map.scss';
import maplibre from 'maplibre-gl';

function MyMap() {
  let mapContainer;

  useEffect(() => {
    const myAPIKey = '05a786c10b224977937d2a9a5f16fd40'; 
    const mapStyle = 'https://maps.geoapify.com/v1/styles/osm-bright-grey/style.json';

    const initialState = {
      lng: 11,
      lat: 49,
      zoom: 4
    };

    const map = new maplibre.Map({
      container: mapContainer,
      style: `${mapStyle}?apiKey=${myAPIKey}`,
      center: [initialState.lng, initialState.lat],
      zoom: initialState.zoom
      });

  }, [mapContainer]);

  return (
    <div className="map-container" ref={el => mapContainer = el}>
    </div>
  )
}

export default MyMap;