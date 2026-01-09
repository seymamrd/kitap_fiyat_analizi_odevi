import requests
from bs4 import BeautifulSoup


def scrape_dr(query):
    url = f"https://www.dr.com.tr/search?q={query.replace(' ', '+')}"
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    try:
        item = soup.select_one(".site-container")
        title = item.select("h3.seo-heading")[0].text.strip()

        author = soup.select("h3.seo-heading")[1].text.strip()

        publisher = item.select_one(".prd-publisher")
        if publisher:
            publisher = publisher.text.strip()
        else:
            publisher = None

        raw_fiyat = item.select_one(".prd-price").text
        price = float(raw_fiyat.replace("TL","").replace(",",".").strip())

        link = "https://www.dr.com.tr" + item.select_one("a")["href"]
        
        return{
            "site": "D&R", 
            "title": title, 
            "author": author, 
            "publisher":publisher, 
            "price": price,
            "link": link
            }
    except:
        return None

