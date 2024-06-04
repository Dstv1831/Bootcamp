import smtplib
import requests
from bs4 import BeautifulSoup
import os
URL = 'https://www.amazon.com.au/Optimum-Nutrition-Standard-Chocolate-Kilograms/dp/B07B2W7FN9/ref=sr_1_4_pp?crid=36R4RE3P1RVRE&dib=eyJ2IjoiMSJ9.eSDJWXA6TjXU-NwfTNkByLW5mWDbtuJR-peWlMuqP_E3psBqZfZ2xFEYb3DEMivV6ldSUUtN1vu6eT01wHA-pI2p10ekZ-zr9NQvb8Ntq21gvyLVxbJY3UGqUj1kUjJ9g8K7GYY8kSmH6EVsTZqef3w5FNdtu52M8islVl2JYZZFIVQRaBjIV_tHYO20LBhkw5r7WwrBUOZCPSulkPXMBE_MOo2vI3-bq3D7FuPa9jNMutIq_oyH0wwqDxVl1Iv56iHss6u1rkbIceT2TCLaDRHCC9r1fOWLlyF1FDSa_9c.f-yRvOUo7smOwpE5BO5PEgTrFCjauveYoyEDIITbvg4&dib_tag=se&keywords=optimum%2Bnutrition%2Bgold%2Bstandard&qid=1717463832&s=health&sprefix=optimu%2Chpc%2C291&sr=1-4&th=1'

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 '
                  'Safari/537.36 Edg/125.0.0.0',
    'Accept-Language': 'en-US,en;q=0.9,en-AU;q=0.8'
}
response = requests.get(url=URL, headers=headers)

soup = BeautifulSoup(response.content, "lxml")

price_tag = soup.find(name='span', id='sns-base-price').find(name='span', class_="a-price-whole")
price = int(price_tag.get_text().strip('.'))
title_tag = soup.find(name='span', id="productTitle")
title = title_tag.get_text().strip()

if price <= 150:
    message = f"Subject: Protein Price Alert! \n\n {title} is now ${price}. \n\n {URL}"
    with smtplib.SMTP("smtp.gmail.com", port=587) as connection:
        connection.starttls()
        connection.login(user=os.environ.get('SENDER'), password=os.environ.get('PASSWORD'))
        connection.sendmail(
            from_addr=os.environ.get('SENDER'),
            to_addrs=os.environ.get('RECEIVER'),
            msg=message)
