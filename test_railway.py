#!/usr/bin/env python3
"""
Test script to verify Railway deployment is working
"""

import requests
import json
from datetime import datetime

def test_railway_deployment():
    # Replace this with your actual Railway URL
    # It should look like: https://your-app-name.railway.app
    RAILWAY_URL = "https://your-app-name.railway.app"  # Update this!
    
    try:
        print(f"Testing Railway deployment at: {RAILWAY_URL}")
        print("=" * 50)
        
        # Test the main data endpoint
        response = requests.get(f"{RAILWAY_URL}/data", timeout=30)
        
        if response.status_code == 200:
            data = response.json()
            print("✅ API is working!")
            print(f"📊 Latest temperature: {data.get('metrics', {}).get('latest_temp', 'N/A')}°C")
            print(f"⏰ Last update: {data.get('last_update', 'N/A')}")
            print(f"📈 Data points: {len(data.get('data', []))}")
            
            # Check if we have recent data
            if data.get('data'):
                latest_record = data['data'][-1]
                print(f"🌡️ Latest reading: {latest_record.get('Temperature (°C)', 'N/A')}°C")
                print(f"💧 Humidity: {latest_record.get('Relative Humidity (%)', 'N/A')}%")
                print(f"💨 Wind Speed: {latest_record.get('Wind Speed (m/s)', 'N/A')} m/s")
            
        else:
            print(f"❌ API returned status code: {response.status_code}")
            print(f"Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Connection failed - check your Railway URL")
        print("Make sure to update the RAILWAY_URL variable in this script")
    except requests.exceptions.Timeout:
        print("❌ Request timed out - Railway might be starting up")
    except Exception as e:
        print(f"❌ Error: {e}")

def get_railway_url_help():
    print("\n" + "=" * 50)
    print("🔧 To find your Railway URL:")
    print("1. Go to railway.app and log in")
    print("2. Select your project")
    print("3. Go to 'Settings' tab")
    print("4. Look for 'Domains' section")
    print("5. Copy the URL (should look like: https://your-app-name.railway.app)")
    print("6. Update the RAILWAY_URL variable in this script")
    print("=" * 50)

if __name__ == "__main__":
    test_railway_deployment()
    get_railway_url_help() 