import requests
from bs4 import BeautifulSoup
from pprint import pprint
from typing import NamedTuple, Set

Advert = NamedTuple('Advert', [('title', str), ('price', str), ('link', str)])
OLX_URL: str = "https://olx.ua"

def search_by_keyword(keyword: str, base_url: str=OLX_URL, pages: int=1) -> Set[Advert]:
    adverts: Set[Advert] = set()
    parsed_keyword: str = '-'.join(keyword.split())
    search_query: str = f'{base_url}/list/q-{parsed_keyword}/'

    for i in range(1, pages + 1):
        resp = requests.get(f'{search_query}?page={i}')
        soup = BeautifulSoup(resp.text, 'lxml')

        offers = soup.find_all('div', class_='offer-wrapper')
        for offer in offers:
            title_tag = offer.find('td', class_='title-cell').find('a')
            price_tag = offer.find('p', class_='price')
            
            title = title_tag.text.strip() if title_tag else None
            link = title_tag.get('href') if title_tag else None
            price = price_tag.text.strip() if price_tag else None
            if title and price and link:
                # Search ignore case
                if keyword.lower() in title.lower():
                    advert = Advert(title=title, price=price, link=link)
                    adverts.add(advert)
    
    return adverts

if __name__ == '__main__':
    pprint(search_by_keyword("iphone 5", OLX_URL, pages=1))