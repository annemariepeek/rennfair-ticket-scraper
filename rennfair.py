import requests
import smtplib
from bs4 import BeautifulSoup
import time
import smtplib
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# URL of the website
url = "https://www.gatemastertickets.com/store/index_event_schedule.aspx?id=32&date=10%2f1%2f2024&CompanyID=GM223&clear=true"
headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36'}

api_key = os.getenv('OPENAI_API_KEY')
# Email Notification Function
def send_notification(subject, body):
    sender_email = os.getenv('SENDER_EMAIL')
    receiver_email = [os.getenv('RECEIVER_EMAIL1'), os.getenv('RECEIVER_EMAIL2')]
    password = os.getenv('APP_PASSWORD')

    message = f"Subject: {subject}\n\n{body}\nBUY TICKETS NOW!!!!"

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, message)
    print("email sent")

# Function to check the hovermsg attribute
def check_availability():
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    # Find the element by id for the specific date (e.g., Cal10122024 for October 12, 2024)
    element = soup.find("div", {"id": "Cal10122024"}) # October 12, 2024
    element2 = soup.find("div", {"id": "Cal10132024"}) # October 13, 2024

    if element or element2:
        hover_message1 = element.get("hovermsg")
        hover_message2 = element2.get("hovermsg")

        noAvailMsg = "Sorry, there is no availability for this date."
        if hover_message1 != noAvailMsg or hover_message2 != noAvailMsg:
            send_notification("RENNFAIR Tickets Available!", "")
            return True
    return False

# Continuously check for changes every 60 seconds
while True:
    check_availability()
    time.sleep(60)  # Wait for 1 minute before checking again
