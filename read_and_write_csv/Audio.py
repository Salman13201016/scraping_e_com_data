import csv
import requests
from bs4 import BeautifulSoup

def scrape_links(url):
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.text
    else:
        print(f"Failed to fetch the page. Status code: {response.status_code}")
        return []

    soup = BeautifulSoup(html_content, 'html.parser')
    links = soup.find_all('a')

    link_list = []
    for link in links:
        href = link.get('href')
        if href and href.startswith('http'):
            link_list.append(href)

    return link_list

if __name__ == "__main__":
    url = 'https://www.daraz.com.bd/audio/'
    product_links = scrape_links(url)

    for link in product_links:
        print(link)

if __name__ == "__main__":
    url = 'https://www.daraz.com.bd/audio/'
    product_links = scrape_links(url)

    # Save product links to a CSV file
    with open('product_links.csv', 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['Product Links'])
        writer.writerows([[link] for link in product_links])
    
    print("Product links saved to product_links.csv")
