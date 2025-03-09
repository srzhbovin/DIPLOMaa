from DGI_coords import DGIGeocoder

# Замените YOUR_API_KEY на ваш актуальный API-ключ 2ГИС
API_KEY = "e3b6a70c-447c-4a24-8586-67e33b3e54d7"

# Создание экземпляра геокодера
geocoder = DGIGeocoder(api_key=API_KEY)

# Тестовый адрес в Воронеже
address = "Воронеж, проспект Революции, 30"

# Прямое геокодирование
coords = geocoder.geocode_address(address)

if coords:
    print(f"Координаты для '{address}':")
    print(f"Широта: {coords['latitude']}, Долгота: {coords['longitude']}")
else:
    print("Адрес не найден или произошла ошибка.")