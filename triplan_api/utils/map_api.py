import requests

def text_search(text_query, latitude, longitude, api_key):
    """
    呼叫 Google Maps Places API 的 Text Search。

    :param text_query: 查詢文字 (如 "Spicy Vegetarian Food in Sydney, Australia")
    :param latitude: 中心點的緯度
    :param longitude: 中心點的經度
    :return: JSON (至多 20 筆的 place_id)
    """
    url = 'https://places.googleapis.com/v1/places:searchText'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'places.id'
    }
    payload = {
        "textQuery": text_query,
        "locationBias": {
            "circle": {
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": 10000.0
            }
        },
        "pageSize": 20
    }

    response = requests.post(url, headers=headers, json=payload)
    return response.json()

'''
locationBias: 盡量回傳在其中的地點，圓心為經緯度，半徑單位為公尺
有需要超過20筆結果再加pageToken
預設照關聯性排序，有需要照距離排序再加rankPreference
'''

##############################################################

def place_details(place_id, api_key):
    """
    呼叫 Google Maps Places API 的 Place Details。

    :param place_id: 地點的唯一 ID
    :return: JSON (類型、地址、評分、網址、評分數、名字、簡介、至多五則留言)
    """
    url = f'https://places.googleapis.com/v1/places/{place_id}?languageCode=zh-TW'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'displayName,types,formattedAddress,rating,googleMapsUri,reviews.text.text,regularOpeningHours,priceLevel,editorialSummary.text,userRatingCount'
    }

    response = requests.get(url, headers=headers)
    return response.json()

##############################################################

def routes(origin_place_id, destination_place_id, travel_mode, api_key):
    """
    呼叫 Google Maps Routes API。
    
    :param origin_place_id: 起點的 Place ID
    :param destination_place_id: 終點的 Place ID
    :param travel_mode: 交通方式（"DRIVE", "BICYCLE", "WALK", "TRANSIT", "TWO_WHEELER"）
    :param api_key: Google Maps API 金鑰
    :return: JSON (時間 秒、距離 公尺)
    """
    url = 'https://routes.googleapis.com/directions/v2:computeRoutes?languageCode=zh-TW'
    headers = {
        'Content-Type': 'application/json',
        'X-Goog-Api-Key': api_key,
        'X-Goog-FieldMask': 'routes.duration,routes.distanceMeters'
    }
    data = {
        "origin": {
            "placeId": origin_place_id
        },
        "destination": {
            "placeId": destination_place_id
        },
        "travelMode": travel_mode
    }

    response = requests.post(url, headers=headers, json=data)
    return response.json()