import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

# Telegram Bot API credentials
telegram_token = 'YOUR_TELEGRAM_BOT_TOKEN'
channel_username = 'CHANNEL_USERNAME'

# Initialize Selenium WebDriver
driver = webdriver.Chrome('/path/to/chromedriver')  # Replace with the path to your chromedriver executable
driver.get('https://web.whatsapp.com')

# Wait for the user to scan the QR code and log in to WhatsApp Web
input('Press Enter once you are logged in to WhatsApp Web: ')

def forward_to_whatsapp(message):
    # Find the chat input field
    chat_input = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//div[@class="_3u328 copyable-text selectable-text"]')))
    
    # Clear the input field
    chat_input.clear()
    
    # Type the message
    chat_input.send_keys(message)
    
    # Press Enter to send the message
    chat_input.send_keys(Keys.RETURN)

def poll_telegram_channel():
    # Continuously poll the Telegram channel for new messages
    last_update_id = 0

    while True:
        try:
            # Send request to Telegram Bot API to get updates
            response = requests.get(f'https://api.telegram.org/bot{telegram_token}/getUpdates?offset={last_update_id+1}')
            data = response.json()

            # Process received messages
            for result in data['result']:
                message = result.get('message')
                if message and 'text' in message:
                    # Extract the text from the message
                    text = message['text']
                    
                    # Forward the message to WhatsApp
                    forward_to_whatsapp(text)

                # Update the last_update_id
                last_update_id = result['update_id']

            # Wait for a few seconds before polling again
            time.sleep(5)
        
        except Exception as e:
            print('An error occurred:', e)

if __name__ == '__main__':
    poll_telegram_channel()
