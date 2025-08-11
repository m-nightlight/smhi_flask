# Flask Server - Heatwave Alert API

This folder contains all the backend server files for the Heatwave Alert iOS app.

## 📁 File Structure

```
flask-server/
├── flask_api.py          # Main Flask application
├── requirements.txt      # Python dependencies
├── nixpacks.toml        # Railway deployment configuration
├── test_railway.py      # Test script for deployment
├── RAILWAY_DEPLOYMENT.md # Deployment guide
├── .gitignore           # Git ignore rules
└── README.md            # This file
```

## 🚀 Quick Start

### Local Development
```bash
# Install dependencies
pip install -r requirements.txt

# Run the server
python flask_api.py
```

### Railway Deployment
```bash
# Deploy to Railway
git add .
git commit -m "Update Flask server"
git push
```

## 📡 API Endpoints

### Health Check
- **URL:** `/`
- **Method:** GET
- **Response:** JSON with service status

### Weather Data
- **URL:** `/data`
- **Method:** GET
- **Response:** JSON with SMHI weather data

## 🔧 Configuration

### Railway Deployment (nixpacks.toml)
The `nixpacks.toml` file configures Railway to:
- Install Python 3 and GCC
- Create a virtual environment
- Install dependencies from `requirements.txt`
- Start the server with Gunicorn

### Environment Variables
- `PORT` - Server port (Railway sets this automatically)

### SMHI API
- **Station ID:** 71420 (Göteborg A)
- **Parameters:** Temperature, humidity, wind, pressure, precipitation

## 🧪 Testing

Run the test script to verify your Railway deployment:
```bash
python test_railway.py
```

**Remember to update the `RAILWAY_URL` variable in the test script!**

## 📊 Data Format

The API returns weather data in this format:
```json
{
  "data": [
    {
      "DateTime": "2024-01-01 12:00:00",
      "Temperature (°C)": 23.5,
      "Relative Humidity (%)": 65.0,
      "Wind Speed (m/s)": 3.2,
      "Air Pressure (hPa)": 1013.0
    }
  ],
  "metrics": {
    "latest_temp": "23.5",
    "day_avg_temp": "22.1",
    "latest_time": "2024-01-01 12:00:00"
  },
  "last_update": "2024-01-01 12:00:00",
  "deployment": "railway-hobby-tier"
}
```

## 🚨 Troubleshooting

### Common Issues
1. **Connection errors** - Check Railway dashboard
2. **Timeout errors** - SMHI API might be slow
3. **Port issues** - Railway sets PORT automatically
4. **Gunicorn errors** - Check nixpacks.toml configuration

### Railway Dashboard
- Check **Deployments** tab for build status
- Check **Logs** tab for error messages
- Verify service is on **Hobby** tier

### Nixpacks Configuration
The `nixpacks.toml` file handles:
- **Setup phase:** Install Python 3 and GCC
- **Install phase:** Create venv and install dependencies
- **Start phase:** Launch with Gunicorn

## 📱 iOS App Integration

The iOS app expects data from the `/data` endpoint. Make sure your Railway URL is correctly configured in the iOS app.

## 🔄 Deployment Process

1. **Code changes** are committed to git
2. **Railway detects** the nixpacks.toml file
3. **Nixpacks builds** the environment:
   - Installs Python 3 and GCC
   - Creates virtual environment
   - Installs requirements.txt
4. **Gunicorn starts** the Flask app
5. **Health check** confirms deployment success

---

**For detailed deployment instructions, see `RAILWAY_DEPLOYMENT.md`** 