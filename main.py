from data_manager import DataManager
from flight_search import FlightSearch
from notification_manager import NotificationManager

search = FlightSearch()
data_manager = DataManager()
sheet_data = data_manager.get_destination_data()
notification_manager = NotificationManager()

for row in sheet_data:
    print(row)
    if row['iataCode'] == '':
        from flight_search import FlightSearch
        search = FlightSearch()
        row['iataCode'] = search.get_destination_code(row)
        data_manager.put_iata_code(row)

    flight = search.search_for_flights(row)

    try:
        if flight.price < row['lowestPrice']:
            message = f'Cheap flight to {flight.destination_city}' \
                      f'\n\nOnly {flight.price} to fly from {flight.origin_city} ({flight.origin_airport}) ' \
                      f'to {flight.destination_city} ({flight.destination_airport}) from {flight.out_date} to ' \
                      f'{flight.return_date}'
            notification_manager.send_email(message)
    except AttributeError:
        pass


