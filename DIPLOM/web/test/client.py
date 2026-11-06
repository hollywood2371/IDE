import requests
import json

if __name__ == '__main__':
    # выполняем POST-запрос на сервер по эндпоинту add с параметром json
    r = requests.post('http://localhost/predict', json=['ZHO', 13, 'MEDIUM', 1, 13.0, 16, 93.899, 'Abu Dhabi Grand Prix', 2023, 1.600999999999999, -7.060999999999993, 0, 1.0, 0.2241379310344827, 1.0, 0.0, 12.0]
)
    # выводим статус запроса
    print('Status code: {}'.format(r.status_code))
    # реализуем обработку результата
    if r.status_code == 200:
        # если запрос выполнен успешно (код обработки=200),
        # выводим результат на экран
        print('Prediction: {}'.format(r.json()['prediction']))
    else:
        # если запрос завершён с кодом, отличным от 200,
        # выводим содержимое ответа
        print(r.text)