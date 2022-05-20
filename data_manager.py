import requests

sheet_endpoint = YOUR_SHEET_ENDPOINT
USER = YOUR-USER
PASSWORD = YOUR-PASSWORD

class DataManager:

    def __int__(self):
        self.sheet_data = {}

    def get_destination_data(self):
        sheet_response = requests.get(url=sheet_endpoint, auth=(USER, PASSWORD))
        sheet_response.raise_for_status()
        self.sheet_data = sheet_response.json()['prices']
        return self.sheet_data

    def put_iata_code(self, row):
        new_data = {'price':
                        {'iataCode': row['iataCode']}
                        }
        requests.put(url=f'{sheet_endpoint}/{row["id"]}', json=new_data, auth=(USER, PASSWORD))
