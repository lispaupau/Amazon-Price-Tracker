import requests
from bs4 import BeautifulSoup
import smtplib
import lxml
import os
import dotenv

dotenv.load_dotenv()

URL = 'https://www.amazon.com/dp/B075CWJ3T8?ref_=cm_sw_r_cp_ud_ct_FM9M699VKHTT47YD50Q6&th=1'
MY_EMAIL = os.environ.get('email')
PASSWORD = os.environ.get('password')
TO_EMAIL = 'enter email to send'

headers = {
    'User-Agent':
        'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept-Language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7'
}
response = requests.get(url=URL, headers=headers).text

soup = BeautifulSoup(response, 'html.parser')
price = float(soup.find('span', class_='a-offscreen').get_text().split('$')[1])
product_name = soup.find('span', class_='a-size-large product-title-word-break').get_text()

if price <= 100:
    with smtplib.SMTP('smtp.inbox.ru') as connection:
        connection.starttls()
        connection.login(user=MY_EMAIL, password=PASSWORD)
        connection.sendmail(from_addr=MY_EMAIL, to_addrs=TO_EMAIL, msg=f'{product_name}\nprice:{price}\n{URL}')