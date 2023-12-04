from urllib.request import urlopen
from bs4 import BeautifulSoup
from urllib.request import urlopen, Request
import keys
from twilio.rest import Client

url = 'https://www.investing.com/crypto/currencies'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.3'}

req = Request(url, headers=headers)

website = urlopen(req).read()

soup = BeautifulSoup(website, 'html.parser')

print(soup.title.text)

crypto_data = soup.findAll("tr", class_="datatable_row__Hk3IV")

for rows in crypto_data[1:6]:
    td = rows.findAll('td')
    logo = td[2].text
    name = td[3].text
    price = td[4].text
    change = td[5].text
    print(logo)
    print(name)
    print(price)
    print(change)
    edit_price = float(price.replace('$', '').replace(',',''))
    edit_change = float(change.replace('+', '').replace('-','').replace('%', ''))/100

    if '-' in change:
        corresponding = edit_price + (edit_change*edit_price)
        print(f"${'%.2f'%corresponding}")

    elif '+' in change:
        corresponding = edit_price - (edit_change*edit_price)
        print(f"${'%.2f'%corresponding}")

    if name == 'Ethereum2ETH':
        if edit_price > 2000:
            client = Client(keys.accountSID, keys.authToken)
            TwilioNumber = "+18444950597"
            myCellPhone = "+19712821140"
            message = "Sell your Ethereum cryptocurrencies! It is above $2,000!!"
            textmessage = client.messages.create(to=myCellPhone, from_=TwilioNumber, 
                                     body=message)




# print(stock_data)