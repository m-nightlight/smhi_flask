import os
from flask import Flask, jsonify
import requests
from datetime import datetime, timedelta
import json

app = Flask(__name__)

@app.route('/')
def hello():
    return "SMHI Weather API - Heatwave Detection Service"

@app.route('/health')
def health():
    return jsonify({
        "status": "healthy",
        "service": "SMHI Weather API",
        "timestamp": datetime.now().isoformat()
    })

@app.route('/data')
def get_smhi_data():
    # SMHI Göteborg A station (ID: 71420)
    station_id = "71420"
    
    # Define the parameters we want
    parameters = {
        1: "Temperature (°C)",
        3: "Wind Direction (°)",
        4: "Wind Speed (m/s)",
        6: "Relative Humidity (%)",
        7: "Precipitation (mm/h)",
        9: "Air Pressure (hPa)",
        14: "Rain (mm/15min)"
    }
    
    try:
        # Fetch all parameter data
        all_data = {}
        for param_id, param_name in parameters.items():
            url = f"https://opendata-download-metobs.smhi.se/api/version/1.0/parameter/{param_id}/station/{station_id}/period/latest-months/data.json"
            response = requests.get(url, timeout=30)
            response.raise_for_status()
            data = response.json()
            all_data[param_id] = {value['date']: float(value['value']) for value in data['value']}
        
        # Process hourly data into the format expected by iOS app
        smhi_records = []
        
        # Use temperature data as the base and match other parameters
        temp_data = all_data.get(1, {})
        for timestamp_ms, temp in temp_data.items():
            # Get other parameters for the same timestamp, or use defaults if not available
            wind_direction = all_data.get(3, {}).get(timestamp_ms, 0.0)
            wind_speed = all_data.get(4, {}).get(timestamp_ms, 0.0)
            humidity = all_data.get(6, {}).get(timestamp_ms, 60.0)
            precipitation = all_data.get(7, {}).get(timestamp_ms, 0.0)
            air_pressure = all_data.get(9, {}).get(timestamp_ms, 1013.0)
            rain_15min = all_data.get(14, {}).get(timestamp_ms, 0.0)
            
            # Convert milliseconds to datetime
            date_obj = datetime.fromtimestamp(timestamp_ms / 1000)
            date_str = date_obj.strftime('%Y-%m-%d %H:%M:%S')
            
            # Create record with all weather parameters
            record = {
                "DateTime": date_str,
                "Temperature (°C)": temp,
                "Wind Direction (°)": wind_direction,
                "Wind Speed (m/s)": wind_speed,
                "Relative Humidity (%)": humidity,
                "Precipitation (mm/h)": precipitation,
                "Air Pressure (hPa)": air_pressure,
                "Rain (mm/15min)": rain_15min,
                "Indoor Humidity (%)": None
            }
            smhi_records.append(record)
        
        # Calculate metrics
        if smhi_records:
            temps = [r["Temperature (°C)"] for r in smhi_records]
            humidities = [r["Relative Humidity (%)"] for r in smhi_records]
            wind_speeds = [r["Wind Speed (m/s)"] for r in smhi_records]
            pressures = [r["Air Pressure (hPa)"] for r in smhi_records]
            
            latest_temp = temps[-1] if temps else 0
            latest_humidity = humidities[-1] if humidities else 60
            latest_wind_speed = wind_speeds[-1] if wind_speeds else 0
            latest_pressure = pressures[-1] if pressures else 1013
            latest_time = smhi_records[-1]["DateTime"] if smhi_records else ""
            
            # Calculate averages
            day_avg = sum(temps[-24:]) / min(len(temps[-24:]), 24) if temps else 0
            week_avg = sum(temps[-168:]) / min(len(temps[-168:]), 168) if temps else 0
            month_avg = sum(temps) / len(temps) if temps else 0
            
            metrics = {
                "latest_temp": str(round(latest_temp, 1)),
                "latest_humidity": str(round(latest_humidity, 1)),
                "latest_wind_speed": str(round(latest_wind_speed, 1)),
                "latest_pressure": str(round(latest_pressure, 1)),
                "latest_time": latest_time,
                "indoor_humidity": None,
                "day_avg_temp": str(round(day_avg, 1)),
                "week_avg_temp": str(round(week_avg, 1)),
                "month_avg_temp": str(round(month_avg, 1))
            }
        else:
            metrics = {
                "latest_temp": "0",
                "latest_humidity": "60",
                "latest_wind_speed": "0",
                "latest_pressure": "1013",
                "latest_time": "",
                "indoor_humidity": None,
                "day_avg_temp": "0",
                "week_avg_temp": "0",
                "month_avg_temp": "0"
            }
        
        # Create response in the format expected by iOS app
        smhi_response = {
            "data": smhi_records,
            "metrics": metrics,
            "last_update": datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        return jsonify(smhi_response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

def get_weather_description(temp):
    if temp >= 25:
        return "Hot"
    elif temp >= 20:
        return "Warm"
    elif temp >= 15:
        return "Mild"
    elif temp >= 10:
        return "Cool"
    else:
        return "Cold"

def get_weather_icon(temp):
    if temp >= 25:
        return "01d"
    elif temp >= 20:
        return "02d"
    elif temp >= 15:
        return "03d"
    else:
        return "04d"

if __name__ == '__main__':
    # Railway deployment settings
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    app.run(host='0.0.0.0', port=port, debug=debug) 