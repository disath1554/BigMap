import requests
from io import BytesIO
from PIL import Image

# Показать карту (BytesIO)
def get_map(params):
    api_server = "http://static-maps.yandex.ru/1.x/"
    response = requests.get(api_server, params=params)

    if not response:
        print("Ошибка выполнения запроса map")
        sys.exit(1)

    # Сформируем изображение из строки байт
    image = Image.open(BytesIO(response.content)).convert("RGB")
    fname = 'map1.png'
    image.save(fname)
    return fname
    
    