import requests
from bs4 import BeautifulSoup


url = 'https://www.goodreads.com/quotes'
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

# Find all the quote elements on the page
quote_elements = soup.find_all(class_='quote')


def find_quote():
    """Loop through each quote element, format and then add to list"""
    quotes = []
    output = ""

    for quote in quote_elements:
        text = quote.find(class_='quoteText').text.strip()
        author = quote.find(class_='authorOrTitle').text.strip()
        output = f'"{text}" - {author}'
        quotes.append(output)
    return quotes
