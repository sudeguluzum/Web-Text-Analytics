from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import time
import pandas as pd

# Ürün yorum sayfası
base_url = "https://www.hepsiburada.com/maybelline-new-york-instant-anti-age-eraser-kapatici-01-light-p-HBV000003MOE3-yorumlari"

# Kaç sayfa çekilecek - 0 yaparsan tüm sayfalar çekilir
MAX_PAGE = 0  # 0 = sınırsız (son sayfaya kadar)

options = webdriver.ChromeOptions()
options.add_argument("--start-maximized")

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver.get(base_url)
time.sleep(3)

yorumlar = []
current_page = 1

while True:
    print(f"📄 {current_page}. sayfa çekiliyor...")

    time.sleep(2)

    # Yorum elemanlarını seç (Hepsiburada için doğru selector)
    elements = driver.find_elements(By.CSS_SELECTOR, "div.hermes-ReviewCard-module-KaU17BbDowCWcTZ9zzxw span")

    for e in elements:
        text = e.text.strip()
        if len(text) > 0:
            yorumlar.append(text)

    # Maksimum sayfa limitini kontrol et
    if MAX_PAGE != 0 and current_page >= MAX_PAGE:
        break

    # Sonraki sayfa butonu
    try:
        next_btn = driver.find_element(By.XPATH, "//div[text()='Sonraki']")
    except:
        print("Sonraki sayfa bulunamadı, işlem tamam.")
        break

    # Buton aktif değilse dur
    if "hermes-MobilePageHolder-module-WAVWb7mPV46ek3XEcbYY" in next_btn.get_attribute("class"):
        print("Son sayfaya gelindi.")
        break

    # Sonraki sayfaya tıkla
    driver.execute_script("arguments[0].click();", next_btn)
    time.sleep(2)

    current_page += 1

driver.quit()

# CSV'ye kaydet
df = pd.DataFrame({"yorum": yorumlar})
df.to_csv("hepsiburada_yorumlar.csv", index=False, encoding="utf-8-sig")

print(f"\n Toplam {len(yorumlar)} yorum çekildi ve hepsiburada_yorumlar.csv dosyasına kaydedildi.")
