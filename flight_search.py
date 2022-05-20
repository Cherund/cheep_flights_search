import requests
import datetime
from flight_data import FlightData

TEQUILA_ENDPOINT = 'https://tequila-api.kiwi.com'
APIKEY = YOUR-API-KEY


class FlightSearch:

    def get_destination_code(self, row):
        location_endpoint = f'{TEQUILA_ENDPOINT}/locations/query'

        headers = {"apikey": APIKEY}
        params = {
            'term': row['city'],
            "location_types": "city"
        }

        response = requests.get(url=location_endpoint, headers=headers, params=params)
        airport_data = response.json()['locations']
        iata_code = airport_data[0]['code']
        return iata_code

    def search_for_flights(self, row):
        search_endpoint = f'{TEQUILA_ENDPOINT}/v2/search'
        now = datetime.datetime.now()
        half_year = now + datetime.timedelta(days=180)

        headers = {"apikey": APIKEY}
        params = {
            'fly_from': 'LON',
            'fly_to': f'{row["iataCode"]}',
            'date_from': now.strftime('%d/%m/%Y'),
            'date_to': half_year.strftime('%d/%m/%Y'),
            'nights_in_dst_from': 7,
            'nights_in_dst_to': 28,
            "flight_type": "round",
            "one_for_city": 1,
            "max_stopovers": 0,
            "curr": "USD"
        }

        response = requests.get(url=search_endpoint, headers=headers, params=params)
        response.raise_for_status()

        try:
            data = response.json()["data"][0]
        except IndexError:
            print(f'No direct flights found for {row["city"]}. Let me check with one stop over.')
            params['max_stopovers'] = 1

            try:
                data = response.json()["data"][0]
            except IndexError:
                print(f'Sorry no flights found for {row["city"]} even with stop over.')
                return None

        flight_data = FlightData(
            price=data['price'],
            origin_city=data['cityFrom'],
            origin_airport=data['flyFrom'],
            destination_city=data['cityTo'],
            destination_airport=data['flyTo'],
            out_date=data['route'][0]['local_departure'].split('T')[0],
            return_date=data['route'][1]['local_departure'].split('T')[0]
        )

        print(f'from {flight_data.origin_city} ({flight_data.origin_airport}) to '
              f'{flight_data.destination_city} ({flight_data.destination_airport}) : for ${flight_data.price}')
        return flight_data
