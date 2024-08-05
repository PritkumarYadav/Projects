import requests
import pandas as pd
import sqlite3

# Lists to store weather data
City = []
Description = []
Temperature = []
Humidity = []
Wind_Speed = []

def get_weather(city_id, api_key, cursor):
    # Convert city ID to integer (if necessary)
    city_id = int(city_id)
    
    # API URL
    url = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={api_key}"
    
    try:
        # Send GET request to the API
        response = requests.get(url)
        
        # Check if request was successful (status code 200)
        if response.status_code == 200:
            # Parse JSON response
            data = response.json()
            
            # Extract relevant weather information
            city_name = data['name']
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            
            # Print weather information
            City.append(city_name)
            Description.append(weather_description)
            Temperature.append(temperature)
            Humidity.append(humidity)
            Wind_Speed.append(wind_speed)
            
            # Insert data into the database
            cursor.execute('''
                INSERT INTO weather (City, Description, Temperature, Humidity, Wind_Speed)
                VALUES (?, ?, ?, ?, ?)
            ''', (city_name, weather_description, temperature, humidity, wind_speed))
        else:
            print(f"Failed to retrieve weather data for city ID {city_id}. Status code:", response.status_code)
    
    except Exception as e:
        print(f"An error occurred while processing city ID {city_id}:", e)

def create_database():
    # Connect to the SQLite database (creates the database file if it doesn't exist)
    conn = sqlite3.connect('weather_PK_data.db')
    cursor = conn.cursor()
    
    # Create the weather table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        City TEXT NOT NULL,
        Description TEXT NOT NULL,
        Temperature REAL NOT NULL,
        Humidity INTEGER NOT NULL,
        Wind_Speed REAL NOT NULL
    )
    ''')
    
    return conn, cursor

# Example usage
if __name__ == "__main__":
    # Read city IDs from CSV file into a DataFrame
    df = pd.read_csv('city_598.csv')
    
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = '6ac1cfabfc58105502894a1c70710a99'
    
    # Create and connect to the database
    conn, cursor = create_database()
    
    # Iterate over each row of the DataFrame
    for index, row in df.iterrows():
        city_id = row['id']
        get_weather(city_id, api_key, cursor)
    
    # Commit the transaction
    conn.commit()
    
    # Close the connection
    cursor.close()
    conn.close()
