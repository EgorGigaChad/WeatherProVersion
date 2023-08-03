import requests
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QLineEdit, QVBoxLayout, QRadioButton, QPushButton, QMessageBox
from PyQt5.QtGui import QPalette, QLinearGradient, QColor
from PyQt5.QtCore import Qt

# Ваш API ключ OpenWeatherMap
API_KEY = "1bed10ff70b2b87e72cdf1ec288f619b"


# Функция для получения прогноза погоды
def get_weather_forecast(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)
    data = response.json()
    return data


# Функция для анализа прогноза погоды и рекомендаций по одежде
def analyze_weather(weather_data, units):
    # Проверяем, что данные о погоде получены успешно
    if "main" not in weather_data or "weather" not in weather_data:
        QMessageBox.critical(None, "Ошибка", "Ошибка при получении данных о погоде")
        return

    temperature = weather_data["main"]["temp"]
    humidity = weather_data["main"]["humidity"]
    wind_speed = weather_data["wind"]["speed"]
    pressure = weather_data["main"]["pressure"]

    # Преобразование единиц измерения
    if units == "F":
        temperature = (temperature * 9/5) + 32
        wind_speed = wind_speed * 2.237

    # Анализ погоды и рекомендации по одежде
    if temperature < 15:
        recommendation = "Холодно: куртка, шапка, шарф и перчатки."
    elif temperature < 20:
        recommendation = "Прохладно: легкая куртка или свитер."
    else:
        recommendation = "Тепло: футболка и шорты."

    # Вывод прогноза погоды и дополнительной информации
    result = f"Температура: {temperature}°C\n"
    result += f"Влажность: {humidity}%\n"
    result += f"Скорость ветра: {wind_speed} м/c\n"
    result += f"Атмосферное давление: {pressure} гПа\n"
    result += f"Рекомендации: {recommendation}"

    QMessageBox.information(None, "Прогноз погоды", result)


# Создание графического интерфейса
app = QApplication([])
window = QWidget()
window.setWindowTitle("Погодный прогноз")

# Создание метки и поля ввода для названия города
label = QLabel("Введите название города:")
entry = QLineEdit()

# Создание радиокнопок для выбора единиц измерения
radio_btn_celsius = QRadioButton("Цельсий")
radio_btn_celsius.setChecked(True)
radio_btn_fahrenheit = QRadioButton("Фаренгейт")

# Создание кнопки для получения погоды
button = QPushButton("Получить погоду")
button.clicked.connect(lambda: analyze_weather(get_weather_forecast(entry.text()), "C" if radio_btn_celsius.isChecked() else "F"))

# Создание вертикального макета и добавление элементов
layout = QVBoxLayout()
layout.addWidget(label)
layout.addWidget(entry)
layout.addWidget(radio_btn_celsius)
layout.addWidget(radio_btn_fahrenheit)
layout.addWidget(button)

# Установка макета для окна
window.setLayout(layout)

# Установка градиентного заднего фона
gradient = QLinearGradient(0, 0, 0, window.height())
gradient.setColorAt(0, QColor(250, 12, 245))
gradient.setColorAt(1, QColor(12, 255, 96))
palette = QPalette()
palette.setBrush(QPalette.Window, gradient)
window.setPalette(palette)

# Стилизация кнопок
button.setStyleSheet("QPushButton { background-color: #FF0000; color: #FFFFFF; border-radius: 5px; padding: 10px; }"
                     "QPushButton:hover { background-color: #FF6666; }"
                     "QPushButton:pressed { background-color: #990000; }")

window.show()

# Запуск главного цикла обработки событий
app.exec_()