import requests

BASE_URL = "https://itunes.apple.com/search"

APPS = [
    "wildberries",
    "ozon",
    "lamoda",
    "aliexpress",
    "amazon shopping",
    "яндекс маркет"
]


def get_app_data(app_name: str):
    params = {
        "term": app_name,
        "entity": "software",
        "limit": 1
    }

    response = requests.get(BASE_URL, params=params)

    response.raise_for_status()

    data = response.json()

    if data["resultCount"] == 0:
        return None

    return data["results"][0]


if __name__ == "__main__":

    for app in APPS:

        result = get_app_data(app)

        print(f"\n{app}")

        if result:

            print(result["trackName"])
            print(result["averageUserRating"])
            print(result["userRatingCount"])