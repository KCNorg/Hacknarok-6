import requests
from requests.structures import CaseInsensitiveDict
import json
from categories import categories
from algos import algos
from mock import dst, pl_prsd


def error(err):
    raise Exception(err)


def get_api_key(key_name):
    with open('config.json') as config_file:
        config = json.load(config_file)
        return config['config'][key_name]


def get_data():
    with open('data.json') as data_file:
        data = json.load(data_file)
        return data['data']


def api_request(url):
    headers = CaseInsensitiveDict()
    headers["Accept"] = "application/json"
    headers["User-Agent"] = "My User Agent 1.0"
    resp = requests.get(url, headers=headers)

    return resp.json() if resp.status_code == 200 else error("API request error")


def get_wiki_views(args):
    url = "https://wikimedia.org/api/rest_v1/metrics/pageviews/per-article/" \
          f"{args[0]}.wikipedia.org/all-access/all-agents/{args[1].replace(' ', '%20')}/monthly/20220101/20220401"

    resp = api_request(url)
    views_sum = 0
    for item in resp['items']:
        views_sum += item['views']

    return views_sum


def get_places(api_key, data, radius, limit):
    url = "https://api.geoapify.com/v2/places?categories=tourism" \
          f"&filter=circle:{data['destination']['lon']},{data['destination']['lat']},{radius}&limit={limit}&apiKey={api_key}"
    return api_request(url)


def get_place_details(api_key, place_id):
    url = "https://api.geoapify.com/v2/place-details?" \
          f"id={place_id}&features=details,details.names&apiKey={api_key}"
    return api_request(url)


def get_matrix(api_key, data):
    url = f"https://api.geoapify.com/v1/routematrix?apiKey={api_key}"

    headers = CaseInsensitiveDict()
    headers["Content-Type"] = "application/json"
    resp = requests.post(url, headers=headers, data=data)

    return resp.json() if resp.status_code == 200 else error("API request error")


def parse_response(api_key, places):
    places_parsed = []

    for place in places['features']:
        place_parsed = dict()
        place_parsed['name'] = place['properties']['name']
        place_parsed['lon'] = place['properties']['lon']
        place_parsed['lat'] = place['properties']['lat']
        place_parsed['place_id'] = place['properties']['place_id']

        place_details = get_place_details(api_key, place['properties']['place_id'])

        props = place_details['features'][0]['properties']
        wiki_views = 0
        if 'wiki_and_media' in props and 'wikipedia' in props['wiki_and_media']:
            wiki_views += get_wiki_views(props['wiki_and_media']['wikipedia'].split(":"))

        place_parsed['wiki_views'] = wiki_views

        place_categories = set()
        for c in props['categories']:
            for category in categories:
                if c in categories[category]:
                    place_categories.add(category)

        place_parsed['categories'] = place_categories
        places_parsed.append(place_parsed)

    return places_parsed


def add_vertex(query, v, lon, lat, color, size):
    query += f'&marker=lonlat:{lon},{lat};color:{color};size:{size}'
    return query


def img_query(api_key, zoom, lon, lat, markers):
    markers_text = ""
    i = 0
    num = [1, 2, 3, 4, 5, 6, 7, 8, 9, 'A', 'B', 'C', 'D', 'E', 'F']
    for marker in markers:
        markers_text += f"lonlat:{marker[0]},{marker[1]};color:%23ff0000;size:medium;text:{num[i]}|"
        i += 1

    src = "https://maps.geoapify.com/v1/staticmap?style=osm-carto&width=1800&height=1800" \
          f"&center=lonlat:{lon},{lat}" \
          f"&zoom={zoom}" \
          f"&marker={markers_text[:-1]}" \
          f"&apiKey={api_key}"

    return src


def main():
    places_api_key = get_api_key('places-api-key')
    place_details_api_key = get_api_key('place-details-api-key')
    matrix_key = get_api_key('matrix-key')
    input_data = get_data()

    print(places_api_key)
    print(place_details_api_key)
    print(input_data)

    # print('tourism.sights.memorial.tank' in categories['history'])

    # places = get_places(places_api_key, input_data, 5000, 100)
    # places_parsed = parse_response(place_details_api_key, places)


    places_parsed = pl_prsd

    print(places_parsed)

    pref_categories = ['art', 'history']


    for place in places_parsed:
        attractiveness = 1
        for cat in pref_categories:
            if cat in place['categories']:
                attractiveness *= 10

        place['attractiveness'] = place['wiki_views'] * attractiveness

    places_parsed.sort(key=lambda x: x['attractiveness'], reverse=True)

    places = places_parsed[:30]

    for place in places:
        print(place['attractiveness'], place['lon'], place['lat'], place['name'], place['categories'])

    data = dict()
    data["mode"] = "walk"
    data["sources"] = [{"location": [place['lon'], place['lat']]} for place in places]
    data["targets"] = [{"location": [place['lon'], place['lat']]} for place in places]

    # data = json.dumps(data)

    # distances = get_matrix(matrix_key, data)
    distances = dst

    print(distances)


    matrix = [[0] * 30 for _ in range(30)]
    for dist_list in distances['sources_to_targets']:
        for dist in dist_list[:30]:
            # print(dist['source_index'])
            matrix[dist['source_index']][dist['target_index']] = dist['time']
            matrix[dist['target_index']][dist['source_index']] = dist['time']

    [print(x) for x in matrix]

    pins = algos([x['attractiveness'] for x in places], matrix, 10, 0.1, 9500)

    print(places_parsed)

    # suma = 0
    # for i in range(2, len(pins)):
    #     a = pins[i - 1]
    #     b = pins[i]
    #     suma += matrix[a][b]
    # suma += matrix[pins[len(pins) - 1]][0]
    #
    # print(suma)

    marks = [(places[pins[x]]['lon'], places[pins[x]]['lat']) for x in range(len(pins))]

    img = img_query('05a786c10b224977937d2a9a5f16fd40', 16, input_data['destination']['lon'], input_data['destination']['lat'], marks)
    # print(img)

    main_response = dict()

    main_response['success'] = True
    main_response['map'] = img
    main_response['places'] = []

    for index in pins:
        main_response['places'].append(places[index])
        main_response['places'][len(main_response['places']) - 1]['categories'] = list(main_response['places'][len(main_response['places']) - 1]['categories'])
        # print(places[index])
    
    return main_response


if __name__ == '__main__':
    main()
