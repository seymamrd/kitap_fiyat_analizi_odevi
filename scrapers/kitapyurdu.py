import requests
from bs4 import BeautifulSoup


def scrape_kitapyurdu(query):
    url = f"https://www.kitapyurdu.com/index.php?route=product/search&filter_name={query.replace(' ', '+')}"
    r = requests.get(url, headers={"User-Agent":"Mozilla/5.0"})
    soup = BeautifulSoup(r.text, "html.parser")

    try:
        item = soup.select_one(".product-cr")
        title = item.select_one(".name").text.strip()

        # Yazar düzeltmesi
        author = soup.select_one("div.author a.alt span").text.strip()

        publisher = item.select_one("div.publisher a.alt span").text.strip()
        

        # Fiyat
        raw_fiyat = item.select_one(".price-new").text
        price = raw_fiyat.replace("TL","").replace(",",".").replace("\xa0", "").replace("Kitapyurdu Fiyatı:", "").strip()

        # Link düzeltmesi
        link_tag = item.select_one("a")
        if link_tag:
            link = "https://www.kitapyurdu.com" + link_tag["href"].split("?")[0]
        else:
            link = ""

        return {
            "site": "Kitap Yurdu",
            "title": title, 
            "author": author, 
            "publisher":publisher, 
            "price": price,
            "link": link
        }
    except:
        return None
