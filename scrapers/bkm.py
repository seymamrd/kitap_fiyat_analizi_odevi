from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

def bkm_scraper(query):
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

    try:
        url = f"https://www.bkmkitap.com/arama?q={query.replace(' ', '+')}"
        driver.get(url)

        WebDriverWait(driver, 15).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )

        first_item = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".waw-product"))
        )

        title = first_item.find_element(By.CSS_SELECTOR, "p.product-title").text.strip()

        author = first_item.find_elements(By.CSS_SELECTOR, "p.txt-title")[1].text.strip()

        publisher = first_item.find_elements(By.CSS_SELECTOR, "p.txt-title")[0].text.strip()

        price_text = first_item.find_element(By.CSS_SELECTOR, "a.waw-basket").text.strip()
        price = float(price_text.replace("TL","").replace(",",".").strip())

        # first_item zaten .waw-product divi
        link = first_item.find_element(By.CSS_SELECTOR, ".waw-product-item-area > a").get_attribute("href")


        return {
            "site": "BKM",
            "title": title, 
            "author": author, 
            "publisher":publisher, 
            "price": price,
            "link": link
            }

    finally:
        driver.quit()
    
