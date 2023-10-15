import requests
from bs4 import BeautifulSoup

# Define the URL and headers
url = "https://online.prsu.ac.in/site/paymentstatuspost"
base_url = "https://online.prsu.ac.in"
headers = {
    "accept": "*/*",
    "accept-language": "en-US,en;q=0.9,hi;q=0.8",
    "content-type": "application/x-www-form-urlencoded; charset=UTF-8",
    "sec-ch-ua": "\"Google Chrome\";v=\"117\", \"Not;A=Brand\";v=\"8\", \"Chromium\";v=\"117\"",
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": "\"Windows\"",
    "sec-fetch-dest": "empty",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "same-origin",
    "x-requested-with": "XMLHttpRequest",
    "Referer": "https://online.prsu.ac.in/",
    "Referrer-Policy": "strict-origin-when-cross-origin"
}

# Initialize a session and retrieve CSRF token
session = requests.Session()

# Get user input for mobile number and loop count
mobile_number = input("Enter your mobile number: ")
loop_count = int(input("Enter the number of loops to complete: "))

for i in range(loop_count):
    response = session.get(base_url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    csrf_token = soup.find('meta', {'name': 'csrf-token'})['content']

    # Define the POST request data
    data = {
        "mobile": mobile_number
    }

    # Update the headers with the new CSRF token
    headers["x-csrf-token"] = csrf_token

    # Send the POST request
    response = session.post(url, headers=headers, data=data)

    # Print the response content
    print(f"Loop {i+1} - Response: {response.text}")
