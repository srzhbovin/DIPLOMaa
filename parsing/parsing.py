import cianparser
from typing import Union, List
import pandas as pd


class CianParserModule:
    def __init__(self, location: str = 'Воронеж') -> None:
        """
        Инициализация парсера указанным городом.
        :param location: Название города для сбора данных.
        """
        self.location: str = location
        self.parser: cianparser.CianParser = None

    def parser_settings(self) -> cianparser.CianParser:
        """
        Заполнение парсера указанным городом.
        :return: Объект парсера.
        """
        self.parser = cianparser.CianParser(location=self.location)
        return self.parser

    def get_flats(
            self,
            deal_type: str = 'sale',
            rooms: Union[str, int] = 'all',
            additional_settings: dict = None
    ) -> List[dict]:
        """
        Парсинг данных о квартирах со всех страниц и возвращение в виде списка словарей.
        :param deal_type: Тип сделки.
        :param rooms: Количество комнат.
        :param additional_settings: Дополнительные настройки поиска.
        :return: Список словарей с данными о квартирах.
        """
        if self.parser is None:
            self.parser_settings()

        all_data: List[dict] = []  # Список для хранения всех данных
        start_page = additional_settings.get("start_page", 1)
        end_page = additional_settings.get("end_page", 54)

        current_page = start_page
        empty_pages_counter = 0  # Счетчик последовательных пустых страниц
        max_empty_pages = 8  # Максимальное количество пустых страниц подряд

        while current_page <= end_page:
            print(f"Сбор данных со страницы {current_page}...")

            try:
                # Получаем данные со страницы без повторных попыток
                page_data = self.parser.get_flats(
                    deal_type=deal_type,
                    rooms=rooms,
                    with_saving_csv=False,  # Отключаем сохранение на каждой странице
                    additional_settings={"start_page": current_page, "end_page": current_page}
                )

                if not page_data:  # Если данные пустые, увеличиваем счетчик пустых страниц
                    empty_pages_counter += 1
                    print(f"Страница {current_page} пуста. Подсчитано {empty_pages_counter} пустых страниц подряд.")
                    if empty_pages_counter >= max_empty_pages:  # Прекращаем, если слишком много пустых страниц
                        print(f"Прерывание сбора данных из-за {max_empty_pages} последовательных пустых страниц.")
                        break
                else:
                    empty_pages_counter = 0  # Сбрасываем счетчик при наличии данных

                all_data.extend(page_data)  # Добавляем данные со страницы в общий список
                print(f"Успешно собрано {len(page_data)} объявлений со страницы {current_page}.")

            except Exception as e:
                print(f"Ошибка при загрузке страницы {current_page}: {e}")
                # Пропускаем текущую страницу и продолжаем дальше
                print(f"Пропускаем страницу {current_page} и переходим к следующей.")

            current_page += 1  # Переходим к следующей странице

        print(f"Собрано всего {len(all_data)} объявлений для {rooms}-комнатных квартир.")
        return all_data


# Функция для сбора данных для одного города
def collect_data_for_city(city_name: str, rooms_list: List[Union[str, int]], additional_settings: dict):
    parser = CianParserModule(location=city_name)
    all_city_data = []  # Список для хранения всех данных для данного города

    for room in rooms_list:
        print(f"Сбор данных для {room}-комнатных квартир в городе {city_name}...")
        try:
            room_data = parser.get_flats(
                deal_type="sale",  # Тип сделки: продажа
                rooms=room,  # Количество комнат
                additional_settings=additional_settings  # Дополнительные настройки
            )
            if room_data:
                all_city_data.extend(room_data)
                print(f"Собрано {len(room_data)} объявлений для {room}-комнатных квартир.")
            else:
                print(f"Для {room}-комнатных квартир данные не найдены.")
        except Exception as e:
            print(f"Ошибка при сборе данных для {room}-комнатных квартир: {e}")

    # Сохранение всех данных для города в один CSV-файл
    if all_city_data:
        filename = f"cian_flats_{city_name}_all_rooms.csv"
        df = pd.DataFrame(all_city_data)
        df.to_csv(filename, index=False, encoding="utf-8-sig")
        print(f"Данные для города {city_name} сохранены в файл: {filename}")
    else:
        print(f"Для города {city_name} данные не были собраны.")


# Настройки поиска
additional_settings = {
    "start_page": 1,
    "end_page": 54,  # Максимальное количество страниц
}

# Список городов для сбора данных
cities_list = ["Красноярск"]

# Список типов квартир для сбора данных
rooms_list = [1, 2, 3, 4, 5, 'studio']

# Сбор данных для каждого города
for city in cities_list:
    collect_data_for_city(city, rooms_list, additional_settings)

print("Сбор данных завершен.")