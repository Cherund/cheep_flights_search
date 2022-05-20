import smtplib
import requests

email = YOUR-EMAIL
password = YOUR-PASSWORD
sheet_endpoint = YOUR-SHEET-ENDPOINT
USER = YOUR-USER
PASSWORD = YOUR-PASSWORD




class NotificationManager:

    def send_email(self, message):

        feedback = requests.get(url=sheet_endpoint, auth=(USER, PASSWORD))
        feedback.raise_for_status()
        email_dictionary = feedback.json()['users']
        print(email_dictionary)

        for person_data in email_dictionary:

            with smtplib.SMTP('smtp.mail.ru') as connection:
                connection.starttls()
                connection.login(email, password)
                connection.sendmail(email, person_data['email'],
                                    f'Subject:{message}')
