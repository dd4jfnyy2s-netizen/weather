import requests
import json
weather_history = []
def load_weather():
    try:
        with open("weather_history.json", "r", encoding="utf-8") as f:
            weather_history = json.load(f)
            return weather_history
    except FileNotFoundError:
        return []
    
weather_history = load_weather()

def save_weather_history():
    with open("weather_history.json", "w", encoding="utf-8") as f:
        json.dump(weather_history, f, ensure_ascii=False, indent=4)

def get_weather(latitude, longitude):
    forecast = []
    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weather_code&timezone=Asia%2FTokyo&daily=temperature_2m_max,temperature_2m_min,weather_code"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        temperature = data["current"]["temperature_2m"]
        current_weather_code = data["current"]["weather_code"]
        current_weather = convert_weather(current_weather_code)
        for i in range(3):
            date = data["daily"]["time"][i]
            max_tem = data["daily"]["temperature_2m_max"][i]
            min_tem = data["daily"]["temperature_2m_min"][i]
            weather_code = data["daily"]["weather_code"][i]
            weather = convert_weather(weather_code)
            day_data = {
                "date": date,
                "max_tem": max_tem,
                "min_tem": min_tem,
                "weather_code": weather_code,
                "weather": weather
            }
            forecast.append(day_data)
        weather_data = {
            "temperature": temperature,
            "weather": current_weather,
            "forecast": forecast
        }
        return weather_data
    except requests.RequestException:
        print("データを取得できませんでした")
        return None
    
def convert_weather(weather_code):
    weather_map = {
        0: "晴れ",
        1: "主に晴れ",
        2: "曇り",
        3: "曇り",
    }
    if 0<= weather_code <= 3:
        weather = weather_map.get(weather_code, "その他")
    elif 61 <= weather_code <= 67:
        weather = "雨"
    elif 71 <= weather_code <= 77:
        weather = "雪"
    elif 80 <= weather_code <= 82:
        weather = "にわか雨"
    elif weather_code == 95:
        weather = "雷雨"
    else:
        weather = "その他"
    return weather

def show_weather(weather_data):
    print(f"現在の気温: {weather_data['temperature']}℃")
    print(f"現在の天気: {weather_data['weather']}")
    for i, day in enumerate(weather_data["forecast"]):
        if i == 0:
            print("[今日]")
        elif i == 1:
            print("[明日]")
        elif i == 2:
            print("[明後日]")
        print(day["date"])
        print(f"最高気温: {day['max_tem']}℃")
        print(f"最低気温: {day['min_tem']}℃")
        print(day["weather"])

        advice = weather_advice(day["weather"], day["max_tem"])
        print(advice)

def weather_advice(weather, max_tem):
    if weather == "雨":
        return "→傘を持っていきましょう"
    elif max_tem >= 30:
        return "→暑いので水分補給をしましょう"
    else:
        return "→過ごしやすい天気です"

def select_city():
    print("== 登録されている都市 ==")
    for city_name in cities:
        print(city_name)

    city = input("都市名を入力してください: ")

    if city == "終了" or city == "exit":
        return None
    else:
        city_data = cities.get(city)

    if city_data is None:
        print("登録されていない都市です")
        return None
    return city, city_data

def display_weather(city, city_data):
    result = get_weather(
        city_data["latitude"],
        city_data["longitude"]
    )

    if result is not None:
        weather_data = result
        show_weather(weather_data)

        save_data = {
            "city": city,
            "weather_data": result
        }
        weather_history.append(save_data)

cities = {
    "福岡": {"latitude": 33.59, "longitude": 130.40},
    "東京": {"latitude": 35.68, "longitude": 139.69},
    "大阪": {"latitude": 34.69, "longitude": 135.50},
    "名古屋": {"latitude": 35.18, "longitude": 136.91},
    "札幌": {"latitude": 43.06, "longitude": 141.35},
    "那覇": {"latitude": 26.21, "longitude": 127.68}
}

menus = ["天気を見る", "前回の都市の天気を見る", "履歴を見る", "終了"]
last_city = None
while True:
    print("=== 天気アプリ ===")
    for i, menu in enumerate(menus, start=1):
        print(f"{i}. {menu}")

    try:
        choice = int(input("メニューを選択してください: "))
        if choice < 1 or choice > 4:
            print("メニューを1~4で入力してください")
            continue
    except ValueError:
        print("数字で入力してください")
        continue

    if choice == 1:
        selected_city = select_city()
        if selected_city is None:
            continue

        city, city_data = selected_city
        last_city = city

        display_weather(city, city_data)
    elif choice == 2:
        if last_city is None:
            print("まだ都市が選択されていません")
            continue
        print(f"{last_city}の天気データ")
        city_data = cities.get(last_city)
        display_weather(city, city_data)
    elif choice == 3:
        print("==== 天気履歴 ====")
        if not weather_history:
            print("天気の履歴がありません")
            continue
        for i, history in enumerate(weather_history, start=1):
            print(f"{i}. {history['city']}")
        try:
            history_number = int(input("履歴番号を入力してください: "))
            if history_number < 1 or history_number > len(weather_history):
                print("履歴番号を正しく入力してください")
                continue

            selected_history = weather_history[history_number - 1]
            show_weather(selected_history["weather_data"])
        except ValueError:
            print("数字で入力してください")
            continue
    elif choice ==  4:
        print("アプリを終了します")
        save_weather_history()
        break