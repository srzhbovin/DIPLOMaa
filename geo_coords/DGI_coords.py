import requests
from typing import Dict, Any


class DGIGeocoder:
    """
    Класс для работы с геокодером 2GIS.
    """

    def __init__(self, api_key: str) -> None:
        """
        Инициализация геокодера с указанным API-ключом.
        :param api_key: API-ключ для доступа к геокодеру 2GIS.
        """
        self.api_key: str = api_key
        self.base_url: str = "https://catalog.api.2gis.com/3.0/items/geocode"

    def geocode_address(self, address: str) -> Dict[str, Any]:
        """
        Прямое геокодирование: преобразование адреса в координаты.
        :param address: Адрес для геокодирования.
        :return: Словарь с координатами или None при ошибке.
        """
        params = {
            'q': address,
            'fields': 'items.point',
            'key': self.api_key
        }
        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()

            if data["result"]["total"] > 0:
                point = data["result"]["items"][0]["point"]
                return {
                    "latitude": point["lat"],
                    "longitude": point["lon"]
                }
            else:
                print(f"Адрес '{address}' не найден.")
                return None
        except Exception as e:
            print(f"Ошибка прямого геокодирования: {e}")
            return None