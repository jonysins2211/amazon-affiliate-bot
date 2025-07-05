
import requests
import os
import telegram
from bs4 import BeautifulSoup

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG")
CHANNEL_ID = os.getenv("CHANNEL_ID")

bot = telegram.Bot(token=TELEGRAM_TOKEN)

def estrai_offerte_amazon():
    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://www.amazon.it/gp/goldbox"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    offerte = []
    for div in soup.select("div.a-section.a-text-center"):
        titolo = div.select_one("span.a-truncate-full")
        link = div.find("a", href=True)
        prezzo = div.select_one("span.a-price-whole")

        if titolo and link and prezzo:
            nome = titolo.get_text(strip=True)
            href = "https://www.amazon.it" + link["href"].split("?")[0]
            href_affiliato = href + f"?tag={AFFILIATE_TAG}"
            prezzo_txt = prezzo.get_text(strip=True) + "€"

            offerte.append({
                "titolo": nome,
                "prezzo": prezzo_txt,
                "link": href_affiliato
            })

        if len(offerte) >= 3:
            break

    return offerte

def invia_messaggi():
    offerte = estrai_offerte_amazon()

    for offerta in offerte:
        messaggio = f"📦 <b>{offerta['titolo']}</b>\n" \
                    f"💶 <b>Prezzo:</b> {offerta['prezzo']}\n\n" \
                    f"🛒 <a href='{offerta['link']}'>Acquista su Amazon</a>\n" \
                    f"📤 <a href='{offerta['link']}'>Condividi con gli amici</a>"

        bot.send_message(
            chat_id=CHANNEL_ID,
            text=messaggio,
            parse_mode=telegram.ParseMode.HTML,
            disable_web_page_preview=True
        )

if __name__ == "__main__":
    invia_messaggi()
