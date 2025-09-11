import os
import sys
import django
from playwright.sync_api import sync_playwright
import re


# Абсолютен път до Django settings.py
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../..'))
sys.path.append(PROJECT_ROOT)

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from backend.products.models import TravelOffer



def clean_itinerary(text):
    # Премахва повече от един празен ред
    lines = text.splitlines()
    cleaned_lines = []
    previous_blank = False

    for line in lines:
        stripped = line.strip()
        if stripped == "":
            if not previous_blank:
                cleaned_lines.append("")  # добавя само един празен ред
            previous_blank = True
        else:
            cleaned_lines.append(stripped)
            previous_blank = False

    return "\n".join(cleaned_lines)



def clean_text_block(text: str) -> str:
    if not text:
        return ""
    text = text.replace("\xa0", " ").replace("\t", " ")
    text = re.sub(r"[ ]{2,}", " ", text)  # свива двойните спейсове
    text = re.sub(r"\n\s*\n", "\n", text)  # маха празни редове
    return text.strip()



def scrape_offer():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        # url = "https://www.2mko.com/ekskurzia/potchivka-dominikana/1998"
        url = "https://www.2mko.com/ekskurzia/rio-de-zhanejro-iguasu-i-buenos-ajres-oformena-grupa/987"
        page.goto(url)

        # Заглавие
        title = page.locator("h1").text_content().strip()

        destination_raw = page.locator(".offer-info", has_text="Маршрут").text_content().strip()
        destination = destination_raw.split("Маршрут:")[-1].strip()


        transport_raw = page.locator(".offer-info", has_text="Вид транспорт").text_content().strip()
        transport = transport_raw.split("Вид транспорт:")[-1].strip()

        # Продължителност
        duration_raw = page.locator(".offer-info", has_text="Продължителност").text_content().strip()
        duration_days = 10
        duration_nights = 8
        if "дни" in duration_raw and "нощи" in duration_raw:
            try:
                parts = duration_raw.split(":")[1].strip().split("/")
                duration_days = int(parts[0].strip().split()[0])
                duration_nights = int(parts[1].strip().split()[0])
            except:
                pass  # fallback to default

        # Дата и цена
        date_text = page.locator("table.dates tr.dates-info td").nth(0).text_content().strip()
        price_text = page.locator("table.dates tr.dates-info td.price").text_content().strip()
        price_bgn = float(price_text.split("лв")[0].strip().replace(",", "").replace(" ", ""))
        price_eur = float(price_text.split("€")[0].split()[-1].strip().replace(",", ""))

        # Телефони
        phones = page.locator("div.offer-contact a")
        phone_numbers = ", ".join([phones.nth(i).text_content().strip() for i in range(phones.count())])

        # Изображение
        # image_url = page.locator(".offer-main-image").get_attribute("src")

        # Изображение от background-image
        style_attr = page.locator(".offer-main-image").get_attribute("style")
        import re
        match = re.search(r"url\(['\"]?(.*?)['\"]?\)", style_attr or "")
        if match:
            relative_url = match.group(1)
            image_url = f"https://www.2mko.com/{relative_url}"
        else:
            image_url = None


        # Натискаме бутона за програмата
        # page.click("a.anons-btn")
        # page.wait_for_selector(".programa", timeout=10000)
        # itinerary = page.locator(".programa").text_content().strip()
        # Вземаме програмата директно от DOM
        # itinerary = page.locator("#anonsbegin").text_content().strip()
        raw_itinerary = page.locator("#anonsbegin").text_content().strip()
        itinerary = clean_itinerary(raw_itinerary)

        # --- НОВИТЕ СЕЛЕКТОРИ ---
        # Цената включва
        price_includes = [
            clean_text_block(li.text_content())
            for li in page.locator("div.resp-tab-content ul").nth(0).locator("li").all()
        ]

        # Цената не включва
        price_excludes = [
            clean_text_block(li.text_content())
            for li in page.locator("div.resp-tab-content ul").nth(1).locator("li").all()
        ]

        # Депозит
        deposit_text = None
        try:
            deposit_block = page.locator("div.resp-tab-content", has_text="Депозит")
            deposit_text = clean_text_block(deposit_block.text_content())
        except:
            pass

        # Минимален брой участници
        min_participants = None
        try:
            min_block = page.locator("div.resp-tab-content", has_text="Минимален брой")
            min_text = clean_text_block(min_block.text_content())
            match = re.search(r"(\d+)", min_text)
            if match:
                min_participants = int(match.group(1))
        except:
            pass

        # Промо цена
        promo_price = None
        try:
            promo_block = page.locator("div.resp-tab-content", has_text="Промоционалната цена")
            promo_text = clean_text_block(promo_block.text_content())
            match = re.search(r"(\d[\d\s]*)\s*лв", promo_text)
            if match:
                promo_price = int(match.group(1).replace(" ", ""))
        except:
            pass


# New
        required_documents = []
        try:
            docs_block = page.locator("div.resp-tab-content", has_text="НЕОБХОДИМИ ДОКУМЕНТИ")
            raw_docs = clean_text_block(docs_block.text_content())
            # Разделяме по държави
            for section in raw_docs.split("НЕОБХОДИМИ ДОКУМЕНТИ"):
                if "Аржентина" in section or "Бразилия" in section:
                    required_documents.append(section.strip())
        except:
            pass



        # Създаваме речник с данните
        offer = {
            "title": title,
            "destination": destination,
            "transport": transport,
            "duration_days": duration_days,
            "duration_nights": duration_nights,
            "departure_date": date_text,
            "price_bgn": price_bgn,
            "price_eur": price_eur,
            "phone_numbers": phone_numbers,
            "itinerary": itinerary,
            "image_url": image_url,
            "source_url": url,

            "promo_price": promo_price,
            "deposit_text": deposit_text,
            "min_participants": min_participants,
            "price_includes": price_includes,
            "price_excludes": price_excludes,

            "required_documents": required_documents,


        }

        browser.close()
        return offer

# Примерно извикване
offer_data = scrape_offer()
for key, value in offer_data.items():
    print(f"{key}: {value}")



import csv

# Запис в CSV файл
with open("offer_output.csv", mode="w", newline="", encoding="utf-8") as file:
    writer = csv.DictWriter(file, fieldnames=offer_data.keys())
    writer.writeheader()
    writer.writerow(offer_data)
