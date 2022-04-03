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


    # places_parsed = [{'name': 'Kościół pw. Świętych Stanisława i Wacława', 'lon': 19.935455391368265, 'lat': 50.05465045, 'place_id': '5176034c1a7bef33405909a2f4f5fe064940f00102f901764e1305000000009203304b6fc59b6369c3b3c5822070772e20c59a7769c49974796368205374616e6973c582617761206920576163c582617761', 'wiki_views': 14427, 'categories': {'architecture', 'history'}, 'attractiveness': 14427}, {'name': 'Kościół pw. Matki Bożej Częstochowskiej', 'lon': 19.880505540403167, 'lat': 50.003297, 'place_id': '515cbd6c7968e13340590444233b6c004940f00102f901c4c960080000000092032c4b6fc59b6369c3b3c5822070772e204d61746b6920426fc5bc656a20437ac49973746f63686f77736b69656a', 'wiki_views': 149, 'categories': {'architecture', 'history'}, 'attractiveness': 149}, {'name': 'Kościół pw. Wniebowzięcia Najświętszej Marii Panny', 'lon': 19.939448463898756, 'lat': 50.0616547, 'place_id': '5164a88e4c7ef0334059c1acaa78e4074940f00102f90143b58f01000000009203384b6fc59b6369c3b3c5822070772e20576e6965626f777a69c499636961204e616ac59b7769c49974737a656a204d617269692050616e6e79', 'wiki_views': 19110, 'categories': {'architecture', 'history'}, 'attractiveness': 19110}, {'name': 'Kościół pw. Świętego Wojciecha Biskupa i Męczennika', 'lon': 19.93774373235741, 'lat': 50.060888399999996, 'place_id': '51d063a1d710f03340595db91d37cb074940f00102f90149a4be01000000009203394b6fc59b6369c3b3c5822070772e20c59a7769c4997465676f20576f6a636965636861204269736b7570612069204dc499637a656e6e696b61', 'wiki_views': 3132, 'categories': {'architecture', 'history'}, 'attractiveness': 3132}, {'name': 'Kaplica pw. Świętych Jana Chrzciciela i Jana Ewangelisty', 'lon': 19.96971360962275, 'lat': 50.088837749999996, 'place_id': '513ecf64263ff8334059491373095f0b4940f00102f9018fa484370000000092033a4b61706c6963612070772e20c59a7769c49974796368204a616e61204368727a63696369656c612069204a616e61204577616e67656c69737479', 'wiki_views': 299, 'categories': {'architecture', 'history'}, 'attractiveness': 299}, {'name': 'Park Jordana', 'lon': 19.916063073630845, 'lat': 50.06271435, 'place_id': '51e15936488eea3340596fff427104084940f00102f90153357f010000000092030c5061726b204a6f7264616e61', 'wiki_views': 3131, 'categories': {'nature'}, 'attractiveness': 31310}, {'name': 'Kolegium Śląskie', 'lon': 19.92497433316842, 'lat': 50.060558, 'place_id': '519513009acaec3340592d73cfe6be074940f00102f9015b045707000000009203124b6f6c656769756d20c59a6cc485736b6965', 'wiki_views': 750, 'categories': {'history'}, 'attractiveness': 750}, {'name': 'Kościół pw. Bożego Ciała', 'lon': 19.9448288931872, 'lat': 50.049762900000005, 'place_id': '5109c7efb8e7f1334059771b91975f064940f00102f90115fbfb010000000092031d4b6fc59b6369c3b3c5822070772e20426fc5bc65676f20436961c58261', 'wiki_views': 2956, 'categories': {'architecture', 'history'}, 'attractiveness': 2956}, {'name': 'Kościół pw. Świętej Katarzyny Aleksandryjskiej i Świętej Małgorzaty', 'lon': 19.94090549852525, 'lat': 50.0492845, 'place_id': '51bed24a57e4f0334059ec3deb454f064940f00102f9016bcf56020000000092034b4b6fc59b6369c3b3c5822070772e20c59a7769c49974656a204b617461727a796e7920416c656b73616e6472796a736b69656a206920c59a7769c49974656a204d61c582676f727a617479', 'wiki_views': 2807, 'categories': {'architecture', 'history'}, 'attractiveness': 2807}, {'name': 'Kościół pw. Świętej Agnieszki', 'lon': 19.93971205391791, 'lat': 50.05126435, 'place_id': '51a994703992f03340592afc0f2d90064940f00102f901e6d15602000000009203224b6fc59b6369c3b3c5822070772e20c59a7769c49974656a2041676e6965737a6b69', 'wiki_views': 899, 'categories': {'architecture', 'history'}, 'attractiveness': 899}, {'name': 'Kościół pw. Świętego Marka', 'lon': 19.937698964252213, 'lat': 50.06455875, 'place_id': '514bfe1e3e10f0334059a1fca05942084940f00102f901588c58020000000092031f4b6fc59b6369c3b3c5822070772e20c59a7769c4997465676f204d61726b61', 'wiki_views': 805, 'categories': {'architecture', 'history'}, 'attractiveness': 805}, {'name': 'Kościół pw. Świętego Mikołaja', 'lon': 19.947171663414725, 'lat': 50.06087395, 'place_id': '517569b2fc7bf2334059b1188041cb074940f00102f901991e5902000000009203234b6fc59b6369c3b3c5822070772e20c59a7769c4997465676f204d696b6fc582616a61', 'wiki_views': 1028, 'categories': {'architecture', 'history'}, 'attractiveness': 1028}, {'name': 'Fort 31 "Święty Benedykt"', 'lon': 19.95805847641593, 'lat': 50.0427452, 'place_id': '51d7e0604a43f5334059a4cfa1aa78054940f00102f9017e601b050000000092031b466f72742033312022c59a7769c49974792042656e6564796b7422', 'wiki_views': 1421, 'categories': {'architecture', 'history'}, 'attractiveness': 1421}, {'name': 'Kościół pw. Świętego Krzyża', 'lon': 19.943341533221002, 'lat': 50.06336195, 'place_id': '5138cbb5317ef13340599646f6e41c084940f00102f901b4183a08000000009203214b6fc59b6369c3b3c5822070772e20c59a7769c4997465676f204b727a79c5bc61', 'wiki_views': 1929, 'categories': {'architecture', 'history'}, 'attractiveness': 1929}, {'name': 'Kościół pw. Świętej Barbary', 'lon': 19.939828630113645, 'lat': 50.061311599999996, 'place_id': '51e2a8617999f033405932bdc91dd9074940f00102f90199493f08000000009203204b6fc59b6369c3b3c5822070772e20c59a7769c49974656a2042617262617279', 'wiki_views': 1381, 'categories': {'architecture', 'history'}, 'attractiveness': 1381}, {'name': 'Kościół pw. Najświętszego Serca Pana Jezusa', 'lon': 19.948837846148923, 'lat': 50.062099700000005, 'place_id': '5154b6b0afe6f233405956450e21f3074940f00102f9015b5f1409000000009203304b6fc59b6369c3b3c5822070772e204e616ac59b7769c49974737a65676f2053657263612050616e61204a657a757361', 'wiki_views': 569, 'categories': {'architecture', 'history'}, 'attractiveness': 569}, {'name': 'Kościół pw. Świętego Franciszka z Asyżu w Krakowie', 'lon': 19.936092126665912, 'lat': 50.05921945, 'place_id': '51ec980c7ba2ef3340595011ce9394074940f00102f901cf39f10b000000009203384b6fc59b6369c3b3c5822070772e20c59a7769c4997465676f204672616e6369737a6b61207a20417379c5bc752077204b72616b6f776965', 'wiki_views': 4215, 'categories': {'architecture', 'history'}, 'attractiveness': 4215}, {'name': 'Kościół pw. Nawiedzenia Najświętszej Maryi Panny', 'lon': 19.93192211525424, 'lat': 50.065144950000004, 'place_id': '51a8b8bd1e94ee334059304e543e56084940f00102f901c818210c000000009203354b6fc59b6369c3b3c5822070772e204e61776965647a656e6961204e616ac59b7769c49974737a656a204d617279692050616e6e79', 'wiki_views': 0, 'categories': {'architecture', 'history'}, 'attractiveness': 0}, {'name': 'Kościół pw. Najświętszego Salwatora', 'lon': 19.912344162857146, 'lat': 50.053426200000004, 'place_id': '51816771fc8ee9334059e76fffa2d6064940f00102f901ded9d20d000000009203284b6fc59b6369c3b3c5822070772e204e616ac59b7769c49974737a65676f2053616c7761746f7261', 'wiki_views': 1155, 'categories': {'architecture', 'history'}, 'attractiveness': 1155}, {'name': 'Symulator tramwaju', 'lon': 19.9951818, 'lat': 50.0758809, 'place_id': '510d93043cc4fe3340598abb1e77b6094940f00103f90150fc173f0100000092031253796d756c61746f72207472616d77616a75', 'wiki_views': 0, 'categories': set(), 'attractiveness': 0}, {'name': 'Barbakan', 'lon': 19.94145102617512, 'lat': 50.0654581, 'place_id': '51b4f2c7ac0df1334059c5eb2a4161084940f00101f90154f3ce000000000092030842617262616b616e', 'wiki_views': 7770, 'categories': {'architecture', 'history'}, 'attractiveness': 7770}, {'name': 'Zarys Bramy Szewskiej', 'lon': 19.933112366342662, 'lat': 50.063366599999995, 'place_id': '513cc91cdfdeee334059b0551c101c084940f00101f9018a655c00000000009203155a61727973204272616d7920537a6577736b69656a', 'wiki_views': 340, 'categories': {'history'}, 'attractiveness': 340}, {'name': 'Kamienica Czeczotki', 'lon': 19.935207563963782, 'lat': 50.061300200000005, 'place_id': '51ad9113805cef334059527c288dd8074940f00101f901509e1f00000000009203134b616d69656e69636120437a65637a6f746b69', 'wiki_views': 373, 'categories': {'history'}, 'attractiveness': 373}, {'name': 'Bastion III "Kleparz"', 'lon': 19.937053219360877, 'lat': 50.0750199, 'place_id': '51fc97d9a714f03340594a34cdc59f094940f00101f901b77d1b000000000092031542617374696f6e2049494920224b6c657061727a22', 'wiki_views': 795, 'categories': {'architecture', 'history'}, 'attractiveness': 795}, {'name': 'Błonia', 'lon': 19.910682426469606, 'lat': 50.05985065, 'place_id': '513da0ebf902e9334059e0631ec9a5074940f00102f901f8337f010000000092030742c5826f6e6961', 'wiki_views': 3320, 'categories': set(), 'attractiveness': 3320}, {'name': 'Wieża Ratuszowa', 'lon': 19.936414898451858, 'lat': 50.06148585, 'place_id': '5105c46db0b8ef3340597b98f170de074940f00102f9011a587f0100000000920310576965c5bc612052617475737a6f7761', 'wiki_views': 2894, 'categories': {'architecture', 'history'}, 'attractiveness': 2894}, {'name': 'Kościół pw. Świętego Floriana', 'lon': 19.94326892911674, 'lat': 50.0675425, 'place_id': '517efda1677af133405914b37fa4a5084940f00102f9011c44be01000000009203224b6fc59b6369c3b3c5822070772e20c59a7769c4997465676f20466c6f7269616e61', 'wiki_views': 3185, 'categories': {'architecture', 'history'}, 'attractiveness': 3185}, {'name': 'Dworek Białoprądnicki', 'lon': 19.94089504999999, 'lat': 50.09283125, 'place_id': '51e1b77c7fdef0334059652df6e4e10b4940f00102f901865ad6010000000092031744776f72656b20426961c5826f7072c485646e69636b69', 'wiki_views': 0, 'categories': {'architecture'}, 'attractiveness': 0}, {'name': 'Kościół pw. Świętego Michała Archanioła i Świętego Stanisława Biskupa', 'lon': 19.937628356746295, 'lat': 50.0482346, 'place_id': '51a983f2f908f0334059fb34abba2c064940f00102f90112fbfb010000000092034f4b6fc59b6369c3b3c5822070772e20c59a7769c4997465676f204d69636861c582612041726368616e696fc58261206920c59a7769c4997465676f205374616e6973c582617761204269736b757061', 'wiki_views': 4936, 'categories': {'architecture', 'history'}, 'attractiveness': 4936}, {'name': 'Synagoga Remuh', 'lon': 19.947293916647524, 'lat': 50.0526493, 'place_id': '512de71a0c81f233405998012c37bd064940f00102f9011afbfb010000000092030e53796e61676f67612052656d7568', 'wiki_views': 1680, 'categories': {'architecture', 'history'}, 'attractiveness': 1680}, {'name': 'Brama Floriańska', 'lon': 19.941352705250004, 'lat': 50.06485575000001, 'place_id': '517e00fc81fcf0334059347958374d084940f00102f901628c5802000000009203114272616d6120466c6f726961c584736b61', 'wiki_views': 4217, 'categories': {'architecture', 'history'}, 'attractiveness': 4217}, {'name': 'Szara Kamienica', 'lon': 19.938527867391027, 'lat': 50.0610704, 'place_id': '513e8825d943f0334059a0c4d7c2d0074940f00102f901ffaa58020000000092030f537a617261204b616d69656e696361', 'wiki_views': 945, 'categories': {'history'}, 'attractiveness': 945}, {'name': 'Arka Pana', 'lon': 20.0293431527762, 'lat': 50.085004, 'place_id': '51b57c155b8207344059a2e346fee00a4940f00102f901b3f159020000000092030941726b612050616e61', 'wiki_views': 3047, 'categories': {'architecture', 'history'}, 'attractiveness': 3047}, {'name': 'Cmentarz Podgórski (stary)', 'lon': 19.959105383140805, 'lat': 50.0418538, 'place_id': '513a7e98068ef5334059f2f58c4d5e054940f00102f9019816fd040000000092031b436d656e7461727a20506f6467c3b372736b692028737461727929', 'wiki_views': 795, 'categories': {'history'}, 'attractiveness': 795}, {'name': 'Teatr im. Juliusza Słowackiego', 'lon': 19.943065943839876, 'lat': 50.0639468, 'place_id': '51d2f38edd6bf13340596d17ca4c2f084940f00102f901befb2c090000000092031f546561747220696d2e204a756c6975737a612053c5826f7761636b6965676f', 'wiki_views': 8811, 'categories': {'art', 'history'}, 'attractiveness': 88110}, {'name': 'Kościół pw. Świętego Bartłomieja', 'lon': 19.93354893275861, 'lat': 50.042211449999996, 'place_id': '5117914a39feee334059ef3dc13c67054940f00102f90142277009000000009203264b6fc59b6369c3b3c5822070772e20c59a7769c4997465676f2042617274c5826f6d69656a61', 'wiki_views': 390, 'categories': {'architecture', 'history'}, 'attractiveness': 390}, {'name': 'Kopiec Kościuszki', 'lon': 19.8933483, 'lat': 50.0549163, 'place_id': '51eb6f6479b2e43340594c0e4f7f07074940f00103f901cfd37a0d000000009203124b6f70696563204b6fc59b636975737a6b69', 'wiki_views': 10703, 'categories': {'nature', 'history'}, 'attractiveness': 107030}, {'name': 'Pałac Jerzmanowskich', 'lon': 19.99482583246359, 'lat': 50.01947345000001, 'place_id': '5101f2330eadfe334059b658308b7e024940f00102f901c9ad1b2e000000009203155061c5826163204a65727a6d616e6f77736b696368', 'wiki_views': 403, 'categories': {'architecture', 'history'}, 'attractiveness': 403}, {'name': 'Pomnik Józefa Dietla', 'lon': 19.936759, 'lat': 50.059086, 'place_id': '51d13b1570cfef334059f29e492190074940f00103f9014f966f5a00000000920315506f6d6e696b204ac3b37a65666120446965746c61', 'wiki_views': 424, 'categories': {'history'}, 'attractiveness': 424}, {'name': 'Krypta pod Wieżą Srebrnych Dzwonów', 'lon': 19.9352391, 'lat': 50.0544944, 'place_id': '51c37064d46bef33405977b427acf9064940f00103f901cb5eda75000000009203254b727970746120706f6420576965c5bcc4852053726562726e79636820447a776f6ec3b377', 'wiki_views': 7243, 'categories': {'history'}, 'attractiveness': 7243}, {'name': 'Studzienka Badylaka', 'lon': 19.9369161, 'lat': 50.0623975, 'place_id': '518a98c8bbd9ef3340593cb829a4fc074940f00103f901c4720d9500000000920313537475647a69656e6b6120426164796c616b61', 'wiki_views': 502, 'categories': set(), 'attractiveness': 502}, {'name': 'Piotr Skrzynecki', 'lon': 19.9357975, 'lat': 50.0617718, 'place_id': '51b52dca6c90ef3340598f336923e8074940f00103f901241480950000000092031050696f747220536b727a796e65636b69', 'wiki_views': 490, 'categories': {'history'}, 'attractiveness': 490}, {'name': 'Pantograf Cafe', 'lon': 19.9954248, 'lat': 50.0750489, 'place_id': '5198a0e128d4fe3340597b56cc339b094940f00103f901dc87aaa80000000092030e50616e746f677261662043616665', 'wiki_views': 0, 'categories': {'history'}, 'attractiveness': 0}, {'name': 'Wahadło Foucaulta', 'lon': 19.93868, 'lat': 50.0569478, 'place_id': '51c7681d554df0334059f415c4104a074940f00103f901b94a9bda000000009203125761686164c5826f20466f756361756c7461', 'wiki_views': 0, 'categories': set(), 'attractiveness': 0}, {'name': 'Cerkiew Zaśnięcia Najświętszej Marii Panny', 'lon': 19.9412887, 'lat': 50.0630285, 'place_id': '512898d64bf8f0334059b8e65f5111084940f00103f901acc1b1d70100000092032e4365726b696577205a61c59b6e69c499636961204e616ac59b7769c49974737a656a204d617269692050616e6e79', 'wiki_views': 1450, 'categories': {'architecture', 'history'}, 'attractiveness': 1450}, {'name': 'Balon', 'lon': 19.9357564, 'lat': 50.0463192, 'place_id': '51d0053fbb8def334059c9639bc9ed054940f00103f901ebc429190200000092030542616c6f6e', 'wiki_views': 0, 'categories': set(), 'attractiveness': 0}, {'name': 'Plac Bohaterów Getta', 'lon': 19.95438111538139, 'lat': 50.0467232, 'place_id': '5136932e6452f433405962094bcdfa054940f00102f901e8e18b0100000000920315506c616320426f6861746572c3b377204765747461', 'wiki_views': 2459, 'categories': {'history'}, 'attractiveness': 2459}, {'name': 'Kościół pw. Niepokalanego Serca Najświętszej Marii Panny', 'lon': 19.930927133087586, 'lat': 50.05874985, 'place_id': '51411a79f54fee33405980e8906c85074940f00102f901b480bf010000000092033d4b6fc59b6369c3b3c5822070772e204e6965706f6b616c616e65676f205365726361204e616ac59b7769c49974737a656a204d617269692050616e6e79', 'wiki_views': 360, 'categories': {'architecture', 'history'}, 'attractiveness': 360}, {'name': 'Kościół pw. Świętego Jana Chrzciciela i Świętego Jana Ewangelisty', 'lon': 19.938947253459645, 'lat': 50.063137749999996, 'place_id': '51d8bde2685ef033405992224bdf14084940f00102f901858c5802000000009203484b6fc59b6369c3b3c5822070772e20c59a7769c4997465676f204a616e61204368727a63696369656c61206920c59a7769c4997465676f204a616e61204577616e67656c69737479', 'wiki_views': 1438, 'categories': {'architecture', 'history'}, 'attractiveness': 1438}, {'name': 'Kościół pw. Najświętszego Serca Pana Jezusa', 'lon': 19.92768226312704, 'lat': 50.060461000000004, 'place_id': '5159ddcfd87fed3340598a21ea9dbd074940f00102f901971a5902000000009203304b6fc59b6369c3b3c5822070772e204e616ac59b7769c49974737a65676f2053657263612050616e61204a657a757361', 'wiki_views': 535, 'categories': {'architecture', 'history'}, 'attractiveness': 535}, {'name': 'Kościół pw. Świętego Franciszka Salezego', 'lon': 19.936954023833113, 'lat': 50.0683031, 'place_id': '517f19073adcef3340598758fe21be084940f00102f901a61a59020000000092032d4b6fc59b6369c3b3c5822070772e20c59a7769c4997465676f204672616e6369737a6b612053616c657a65676f', 'wiki_views': 880, 'categories': {'architecture', 'history'}, 'attractiveness': 880}, {'name': 'Kościół pw. Niepokalanego Poczęcia Najświętszej Maryi Panny', 'lon': 19.95145012181267, 'lat': 50.062469300000004, 'place_id': '51efeec3f593f3334059d4254b57fd074940f00102f901023a5902000000009203414b6fc59b6369c3b3c5822070772e204e6965706f6b616c616e65676f20506f637ac499636961204e616ac59b7769c49974737a656a204d617279692050616e6e79', 'wiki_views': 1445, 'categories': {'architecture', 'history'}, 'attractiveness': 1445}, {'name': 'Kościół Świętego Marcina', 'lon': 19.938622984601736, 'lat': 50.05589835, 'place_id': '51b0a43fef48f03340591bbc498827074940f00102f901051c70070000000092031d4b6fc59b6369c3b3c58220c59a7769c4997465676f204d617263696e61', 'wiki_views': 1242, 'categories': {'architecture', 'history'}, 'attractiveness': 1242}, {'name': 'Kościół Zwiastowania Najświętszej Maryi Panny', 'lon': 19.92994968454639, 'lat': 50.061964700000004, 'place_id': '515201f63b13ee33405982d5084eee074940f00102f901e12b210c000000009203324b6fc59b6369c3b3c582205a77696173746f77616e6961204e616ac59b7769c49974737a656a204d617279692050616e6e79', 'wiki_views': 930, 'categories': {'architecture', 'history'}, 'attractiveness': 930}, {'name': 'Kościół pw. Niepokalanego Poczęcia Najświętszej Maryi Panny', 'lon': 19.95234684800529, 'lat': 50.068553, 'place_id': '51a8b330c5ccf333405999b42f7fc5084940f00102f9011617220c000000009203414b6fc59b6369c3b3c5822070772e204e6965706f6b616c616e65676f20506f637ac499636961204e616ac59b7769c49974737a656a204d617279692050616e6e79', 'wiki_views': 746, 'categories': {'architecture', 'history'}, 'attractiveness': 746}, {'name': 'Tupolew Tu-134A', 'lon': 19.989685077045056, 'lat': 50.0793171, 'place_id': '511b9a43bb5cfd334059519eefb9260a4940f00102f901c94159120000000092030f5475706f6c65772054752d31333441', 'wiki_views': 0, 'categories': {'history'}, 'attractiveness': 0}, {'name': 'ruiny fortu 47½ "Sudół"', 'lon': 19.985591456546928, 'lat': 50.1032225, 'place_id': '514e1fdc864bfc33405913d9cd99380d4940f00102f901a15f14150000000092031a7275696e7920666f727475203437c2bd2022537564c3b3c58222', 'wiki_views': 296, 'categories': {'architecture', 'history'}, 'attractiveness': 296}, {'name': 'Antoni Fertner', 'lon': 19.9566028, 'lat': 50.0751805, 'place_id': '511443cdebe3f4334059932fbd839f094940f00103f901a4d1bd730000000092030e416e746f6e6920466572746e6572', 'wiki_views': 0, 'categories': {'history'}, 'attractiveness': 0}, {'name': 'Grób Szymborskich', 'lon': 19.9553985, 'lat': 50.0744644, 'place_id': '51c02500ff94f43340595725a80c88094940f00103f901a604c073000000009203124772c3b36220537a796d626f72736b696368', 'wiki_views': 0, 'categories': {'history'}, 'attractiveness': 0}, {'name': 'Krypta św. Leonarda', 'lon': 19.935589, 'lat': 50.0548629, 'place_id': '51527fbdc282ef334059d86d5bbf05074940f00103f9012c29da75000000009203144b727970746120c59b772e204c656f6e61726461', 'wiki_views': 3070, 'categories': {'history'}, 'attractiveness': 3070}, {'name': 'Krzyż Najświętszej Maryi Panny Matki Kościoła', 'lon': 19.9316289, 'lat': 50.0969667, 'place_id': '512982493b7fee3340596c6da167690c4940f00103f901b1642b7f000000009203324b727a79c5bc204e616ac59b7769c49974737a656a204d617279692050616e6e79204d61746b69204b6fc59b63696fc58261', 'wiki_views': 0, 'categories': {'history'}, 'attractiveness': 0}, {'name': 'Pomnik Ignacego Jana Paderewskiego', 'lon': 19.9502033, 'lat': 50.0663071, 'place_id': '51200d028640f3334059bbc943c07c084940f00103f9018112868800000000920322506f6d6e696b2049676e616365676f204a616e612050616465726577736b6965676f', 'wiki_views': 109, 'categories': {'history'}, 'attractiveness': 109}, {'name': 'Silva Rerum', 'lon': 19.957612, 'lat': 50.0412364, 'place_id': '51d6415e0f26f53340599481fd3b47054940f00103f9012b57998d0000000092030b53696c766120526572756d', 'wiki_views': 301, 'categories': {'art'}, 'attractiveness': 3010}, {'name': 'Jakowlew Jak-40', 'lon': 19.9914243, 'lat': 50.0781465, 'place_id': '51adf5a0fbcdfd33405933af59b4000a4940f00103f901f4a78aba0000000092030f4a616b6f776c6577204a616b2d3430', 'wiki_views': 0, 'categories': {'history'}, 'attractiveness': 0}, {'name': 'Mil Mi-8PS', 'lon': 19.9904302, 'lat': 50.0768761, 'place_id': '5181f865d58cfd33405966757613d7094940f00103f901bd688bba0000000092030a4d696c204d692d385053', 'wiki_views': 0, 'categories': {'history'}, 'attractiveness': 0}, {'name': 'Judah', 'lon': 19.948361, 'lat': 50.0503135, 'place_id': '5145cd57c9c7f2334059b25239ac70064940f00103f90110247fbd000000009203054a75646168', 'wiki_views': 0, 'categories': {'art'}, 'attractiveness': 0}, {'name': 'E.M. Lilien', 'lon': 19.9489258, 'lat': 50.0509255, 'place_id': '51a5541dcdecf2334059b6500dba84064940f00103f90159d1ba030100000092030b452e4d2e204c696c69656e', 'wiki_views': 0, 'categories': {'art'}, 'attractiveness': 0}, {'name': 'Kamienica Molendowska', 'lon': 19.940130145642776, 'lat': 50.0628507, 'place_id': '518be48458b0f03340597ba85fa30b084940f00101f901968a9700000000009203154b616d69656e696361204d6f6c656e646f77736b61', 'wiki_views': 68, 'categories': {'history'}, 'attractiveness': 68}, {'name': 'Kamienica Pod Jagnięciem', 'lon': 19.93550801330085, 'lat': 50.06180295, 'place_id': '510246b22b78ef334059df04722fe9074940f00101f90183a79300000000009203194b616d69656e69636120506f64204a61676e69c4996369656d', 'wiki_views': 120, 'categories': {'history'}, 'attractiveness': 120}, {'name': 'Zakrzówek', 'lon': 19.909501664466546, 'lat': 50.0365491, 'place_id': '519653630611e9334059b0150988b4044940f00101f9014a3e72000000000092030a5a616b727ac3b377656b', 'wiki_views': 3431, 'categories': {'nature'}, 'attractiveness': 34310}, {'name': 'Ogrody Królewskie', 'lon': 19.937701261307225, 'lat': 50.05464645, 'place_id': '51608209da02f03340596c4fe1dbf9064940f00101f901a1705b00000000009203124f67726f6479204b72c3b36c6577736b6965', 'wiki_views': 496, 'categories': {'nature'}, 'attractiveness': 4960}, {'name': 'Kościół św. Michała', 'lon': 19.93509211778855, 'lat': 50.0540324, 'place_id': '51b75de2ee67ef3340594270084bea064940f00101f901f1b15a00000000009203184b6fc59b6369c3b3c58220c59b772e204d69636861c58261', 'wiki_views': 840, 'categories': {'architecture', 'history'}, 'attractiveness': 840}, {'name': 'Mury miejskie Krakowa', 'lon': 19.9419159123649, 'lat': 50.0647741, 'place_id': '51ca9a971202f133405946a4c21c4d084940f00101f90121115500000000009203154d757279206d69656a736b6965204b72616b6f7761', 'wiki_views': 2182, 'categories': set(), 'attractiveness': 2182}, {'name': 'relikty bastionu V "Lubicz"', 'lon': 19.959998259433963, 'lat': 50.0650435, 'place_id': '514a9f6915a0f53340594d0227ec68084940f00101f9019a7d3d000000000092031b72656c696b74792062617374696f6e75205620224c756269637a22', 'wiki_views': 637, 'categories': {'architecture', 'history'}, 'attractiveness': 637}, {'name': 'Kościół św. Jerzego', 'lon': 19.93482731904083, 'lat': 50.053647999999995, 'place_id': '51385220dd4aef334059c0b1832dde064940f00101f90163ee3b00000000009203174b6fc59b6369c3b3c58220c59b772e204a65727a65676f', 'wiki_views': 668, 'categories': {'architecture', 'history'}, 'attractiveness': 668}, {'name': 'Rynek Główny', 'lon': 19.935947926355013, 'lat': 50.061516499999996, 'place_id': '512318ae5ff6ef3340598ac84f9be3074940f00101f9010a0732000000000092030e52796e656b2047c582c3b3776e79', 'wiki_views': 10683, 'categories': set(), 'attractiveness': 10683}, {'name': 'Kamienica Bidermanowska', 'lon': 19.938819241200697, 'lat': 50.061249450000005, 'place_id': '51e70f296556f03340599ce6441ed7074940f00101f90109063200000000009203174b616d69656e6963612042696465726d616e6f77736b61', 'wiki_views': 150, 'categories': {'history'}, 'attractiveness': 150}, {'name': 'Fort reditowy 12 (IVa) "Luneta Warszawska"', 'lon': 19.946637256983657, 'lat': 50.07791805, 'place_id': '515cdd6eeb61f23340599eb90ea6f9094940f00101f90159e42f000000000092032a466f72742072656469746f777920313220284956612920224c756e65746120576172737a6177736b6122', 'wiki_views': 872, 'categories': {'architecture', 'history'}, 'attractiveness': 872}, {'name': 'Pałac Zbaraskich', 'lon': 19.93671602684276, 'lat': 50.0607024, 'place_id': '51b862ab8ac7ef33405919916c4fc5074940f00101f901f93c2900000000009203115061c5826163205a62617261736b696368', 'wiki_views': 1043, 'categories': {'history'}, 'attractiveness': 1043}, {'name': 'Zamek Królewski na Wawelu', 'lon': 19.936022259529473, 'lat': 50.0544051, 'place_id': '51bfb71bd6c4ef3340594f29b22ef9064940f00101f90163a622000000000092031a5a616d656b204b72c3b36c6577736b69206e6120576177656c75', 'wiki_views': 24575, 'categories': {'architecture'}, 'attractiveness': 24575}, {'name': 'Kamienica Zacherlowska', 'lon': 19.938370525812932, 'lat': 50.0625979, 'place_id': '51f7af42ec37f0334059919e9f0603084940f00101f9018f871f00000000009203164b616d69656e696361205a61636865726c6f77736b61', 'wiki_views': 177, 'categories': {'history'}, 'attractiveness': 177}, {'name': 'Kamienica Pod Konikiem', 'lon': 19.937731092757076, 'lat': 50.0627995, 'place_id': '516e97f82e0cf033405960dad0ae09084940f00101f9018c871f00000000009203164b616d69656e69636120506f64204b6f6e696b69656d', 'wiki_views': 199, 'categories': {'history'}, 'attractiveness': 199}, {'name': 'Kamienica Pod Jeleniem', 'lon': 19.93717941740538, 'lat': 50.062975449999996, 'place_id': '519f401245efef334059d5f04db10f084940f00101f9018b871f00000000009203164b616d69656e69636120506f64204a656c656e69656d', 'wiki_views': 292, 'categories': {'history'}, 'attractiveness': 292}, {'name': 'Pałac Pod Baranami', 'lon': 19.935021954490907, 'lat': 50.061629249999996, 'place_id': '51cbf11dc36eef3340595dcb5a37e3074940f00101f901106c1200000000009203135061c582616320506f6420426172616e616d69', 'wiki_views': 1087, 'categories': {'history'}, 'attractiveness': 1087}, {'name': 'Collegium Maius', 'lon': 19.933403528881612, 'lat': 50.06165525, 'place_id': '51eaabbdcb07ef334059ab304038e4074940f00101f901f74403000000000092030f436f6c6c656769756d204d61697573', 'wiki_views': 3333, 'categories': {'architecture', 'history'}, 'attractiveness': 3333}, {'name': 'Collegium Novum', 'lon': 19.933235139716004, 'lat': 50.06086415, 'place_id': '51669ca258dfee33405944264ef0ca074940f00101f901f64403000000000092030f436f6c6c656769756d204e6f76756d', 'wiki_views': 2678, 'categories': {'history'}, 'attractiveness': 2678}, {'name': 'Floriańska', 'lon': 19.9402823, 'lat': 50.063437, 'place_id': '51a5ade02bb7f03340593655f4761f084940f00102f901f4df3c000000000092030b466c6f726961c584736b61', 'wiki_views': 0, 'categories': set(), 'attractiveness': 0}, {'name': 'Sukiennice', 'lon': 19.937348815057142, 'lat': 50.061692199999996, 'place_id': '51a2317161f6ef3340598c3c62a5e5074940f00102f901d0dd62010000000092030a53756b69656e6e696365', 'wiki_views': 15415, 'categories': {'architecture', 'history'}, 'attractiveness': 15415}, {'name': 'Diabelski Most', 'lon': 19.9011831, 'lat': 50.0533107, 'place_id': '51352ed27aaee633405903600402d3064940f00102f901b4e362010000000092030e44696162656c736b69204d6f7374', 'wiki_views': 640, 'categories': {'architecture'}, 'attractiveness': 640}, {'name': 'Baszta Sandomierska', 'lon': 19.935095275862075, 'lat': 50.05281905, 'place_id': '5135794e7261ef334059183040dac2064940f00102f9011e598501000000009203134261737a74612053616e646f6d696572736b61', 'wiki_views': 816, 'categories': {'architecture', 'history'}, 'attractiveness': 816}, {'name': 'Brama Wazów', 'lon': 19.934837133950246, 'lat': 50.05477225, 'place_id': '51e218b0e750ef3340597e9f18c602074940f00102f901365a85010000000092030c4272616d612057617ac3b377', 'wiki_views': 369, 'categories': {'architecture', 'history'}, 'attractiveness': 369}, {'name': 'Jednostka Ratowniczo-Gaśnicza PSP nr 1 w Krakowie', 'lon': 19.943241179898468, 'lat': 50.05994235, 'place_id': '51cfd5fd8678f1334059e3f50653ac074940f00102f90166df5602000000009203324a65646e6f73746b61205261746f776e69637a6f2d4761c59b6e69637a6120505350206e7220312077204b72616b6f776965', 'wiki_views': 184, 'categories': {'architecture', 'history'}, 'attractiveness': 184}, {'name': 'Kościół pw. Świętego Kazimierza Królewicza', 'lon': 19.936230887154693, 'lat': 50.0648696, 'place_id': '5194550dc6adef334059e6257fd04d084940f00102f9015a8c5802000000009203304b6fc59b6369c3b3c5822070772e20c59a7769c4997465676f204b617a696d6965727a61204b72c3b36c657769637a61', 'wiki_views': 1202, 'categories': {'architecture', 'history'}, 'attractiveness': 1202}, {'name': 'Collegium Minus', 'lon': 19.933600390397856, 'lat': 50.0611775, 'place_id': '51b381278fffee3340590986f89dd4074940f00102f901688c58020000000092030f436f6c6c656769756d204d696e7573', 'wiki_views': 423, 'categories': {'history'}, 'attractiveness': 423}, {'name': 'Pałac Pod Krzysztofory', 'lon': 19.936369003523268, 'lat': 50.06288885, 'place_id': '51f9cbd9e3aeef3340592673f95b0c084940f00102f901848c5802000000009203175061c582616320506f64204b727a79737a746f666f7279', 'wiki_views': 1590, 'categories': {'history'}, 'attractiveness': 1590}, {'name': 'Kościół pw. Świętego Józefa', 'lon': 19.93978012804358, 'lat': 50.058145100000004, 'place_id': '512b388ae195f0334059de1d574270074940f00102f901fbaa5802000000009203214b6fc59b6369c3b3c5822070772e20c59a7769c4997465676f204ac3b37a656661', 'wiki_views': 659, 'categories': {'architecture', 'history'}, 'attractiveness': 659}, {'name': 'Dom Włoski', 'lon': 19.93862939961048, 'lat': 50.060834150000005, 'place_id': '51a62a815f44f033405913fb011bca074940f00102f90100ab58020000000092030b446f6d2057c5826f736b69', 'wiki_views': 491, 'categories': {'history'}, 'attractiveness': 491}, {'name': 'Kamienica Pod Jaszczurami', 'lon': 19.938299384512618, 'lat': 50.06073605, 'place_id': '515874fa173cf0334059acbea500c6074940f00102f90101ab5802000000009203194b616d69656e69636120506f64204a61737a637a7572616d69', 'wiki_views': 241, 'categories': {'history'}, 'attractiveness': 241}, {'name': 'Kamienica Bonerowska', 'lon': 19.938244852464784, 'lat': 50.06067365, 'place_id': '51e7108f0533f03340594b742f12c4074940f00102f90102ab5802000000009203144b616d69656e69636120426f6e65726f77736b61', 'wiki_views': 585, 'categories': {'history'}, 'attractiveness': 585}, {'name': 'Kamienica Fontanowska', 'lon': 19.938117969189655, 'lat': 50.060367850000006, 'place_id': '5165c6062b29f033405903519cbdb9074940f00102f90105ab5802000000009203154b616d69656e69636120466f6e74616e6f77736b61', 'wiki_views': 120, 'categories': {'history'}, 'attractiveness': 120}]
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
    print(img)

    for index in pins:
        print(places[index])


if __name__ == '__main__':
    main()
