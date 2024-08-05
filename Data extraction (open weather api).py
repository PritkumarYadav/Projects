import requests
import pandas as pd 

City = []
Description = []
Temperature = []
Humidity = []
Wind_Speed = []

def get_weather(city_id, api_key):
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
            weather_description = data['weather'][0]['description']
            temperature = data['main']['temp']
            humidity = data['main']['humidity']
            wind_speed = data['wind']['speed']
            
            # Print weather information
            City.append(data['name'])
            Description.append(weather_description)
            Temperature.append(temperature)
            Humidity.append(humidity)
            Wind_Speed.append(wind_speed)
        else:
            print(f"Failed to retrieve weather data for city ID {city_id}. Status code:", response.status_code)
    
    except Exception as e:
        print(f"An error occurred while processing city ID {city_id}:", e)

# Example usage
if __name__ == "__main__":
    # Read city IDs from CSV file into a DataFrame
    df = pd.read_csv('city_list.csv')
    
    # Replace 'YOUR_API_KEY' with your actual API key
    api_key = '6ac1cfabfc58105502894a1c70710a99'
    
    # Iterate over each row of the DataFrame
    for index, row in df.iterrows():
        city_id = row['id']
        get_weather(city_id, api_key)


# Open the file with explicit encoding and specify the encoding as 'utf-8'
with open('Open_Weather_Data.csv', 'w+', encoding='utf-8') as file:
    # Write the header row
    file.write('City, Description, Temperature, Humidity, Wind_Speed\n')

    # Write data to the file
    for City_1, Description_1, Temperature_1, Humidity_1, Wind_Speed_1 in zip(City, Description, Temperature, Humidity, Wind_Speed):
        # Encode the city name and description using UTF-8 encoding
        City_1 = City_1.encode('utf-8')
        Description_1 = Description_1.encode('utf-8')
        
        # Write data to the file
        file.write(f'{City_1.decode("utf-8")},{Description_1.decode("utf-8")},{Temperature_1},{Humidity_1},{Wind_Speed_1}\n')
