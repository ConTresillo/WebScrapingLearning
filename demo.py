import requests
from bs4 import BeautifulSoup

url = "https://quotes.toscrape.com"
response = requests.get(url)

# Check if request was successful
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    quotes = soup.find_all('div', class_='quote')

    for i, quote in enumerate(quotes, 1):
        text = quote.find('span', class_='text').get_text()
        author = quote.find('small', class_='author').get_text()
        print(f"{i}. {text} - {author}")
else:
    print(f"Failed to retrieve page. Status code: {response.status_code}")
