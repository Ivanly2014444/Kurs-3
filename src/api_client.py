import requests

def get_country_coordinates(country_name: str) -> list | None:
    headers_nominatim = {"User-Agent": "test-app"}
    params_nominatim = {"country": country_name, "format": "json", "limit": 1}
    openstreetmap_url = "https://nominatim.openstreetmap.org/search"

    response = requests.get(
        url=openstreetmap_url,
        params=params_nominatim,
        headers=headers_nominatim
    )
    data = response.json()

    if data:
        return data[0].get("boundingbox")
    return None

def get_airplanes_in_country(boundingbox: list) -> list:

    url = "https://opensky-network.org/api/states/all?"

    params = {
        "lamin": float(boundingbox[0]),
        "lamax": float(boundingbox[1]),
        "lomin": float(boundingbox[2]),
        "lomax": float(boundingbox[3])
    }

    response = requests.get(url=url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data.get("states", [])
    return []