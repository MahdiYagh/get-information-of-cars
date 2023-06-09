#Get info

import requests
from bs4 import BeautifulSoup
import sqlite3

# create database
conn = sqlite3.connect('cars.db')
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS cars (make TEXT, model TEXT, year INTEGER, mileage INTEGER, price INTEGER)')

# get user input
make = input('Enter make of the car: ')
url = f'https://www.truecar.com/used-cars-for-sale/listings/{make}/'

# scrape data and store in database
try:
    response = requests.get(url)
    response.raise_for_status()
    soup = BeautifulSoup(response.content, 'html.parser')
    cars = soup.find_all('div', {'class': 'vehicle-card'})

    for i in range(min(20, len(cars))):
        car = cars[i]
        make = car.find('span', {'class': 'vehicle-header-make'}).text.strip()
        model = car.find('span', {'class': 'vehicle-header-model'}).text.strip()
        year = int(car.find('span', {'class': 'vehicle-card-year'}).text.strip())
        mileage = int(car.find('span', {'class': 'vehicle-card-mileage'}).text.strip().replace(',', ''))
        price = int(car.find('span', {'class': 'vehicle-card-price'}).text.strip().replace('$', '').replace(',', ''))
        cursor.execute("INSERT INTO cars VALUES (?, ?, ?, ?, ?)", (make, model, year, mileage, price))
        conn.commit()
        print(f"Added {make} {model} {year} with {mileage} miles for ${price} to the database")
except requests.exceptions.RequestException as e:
    print(f"Error scraping data: {e}")

# close database connection
conn.close()
