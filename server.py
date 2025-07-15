from flask import Flask, render_template, request
from index import get_current_weather
from waitress import serve

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

@app.route('/weather')
def get_weather():
    city = request.args.get('city')
    weather_data = get_current_weather(city)

    print(weather_data)

    # Debug dữ liệu trả về
    print("📦 Weather data:", weather_data)

    # City is not found by API
    if not weather_data['cod'] == 200:
        return render_template("city-not-found.html")

    if not weather_data or "main" not in weather_data:
        return "❌ Không lấy được dữ liệu thời tiết. Vui lòng kiểm tra lại tên thành phố."

    return render_template(
        "weather.html",
        title=weather_data["name"],
        status=weather_data["weather"][0]["description"].capitalize(),
        temp=f"{weather_data['main']['temp']:.1f}",
        feels_like=f"{weather_data['main']['feels_like']:.1f}"
    )


if __name__ == "__main__":
    serve(app, host='0.0.0.0', port=8000)
    # app.run(debug=True)