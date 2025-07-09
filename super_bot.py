import requests
import os
import telegram
from bs4 import BeautifulSoup

# Load environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
AFFILIATE_TAG = os.getenv("AFFILIATE_TAG")
CHANNEL_ID = os.getenv("CHANNEL_ID")

# Initialize Telegram Bot
bot = telegram.Bot(token=TELEGRAM_TOKEN)

# Function to extract Amazon India deals
def extract_amazon_deals():
    headers = {"User-Agent": "Mozilla/5.0"}
    url = "https://www.amazon.in/gp/goldbox"
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    deals = []
    for div in soup.select("div.a-section.a-text-center"):
        title = div.select_one("span.a-truncate-full")
        link = div.find("a", href=True)
        price = div.select_one("span.a-price-whole")

        if title and link and price:
            name = title.get_text(strip=True)
            href = "https://www.amazon.in" + link["href"].split("?")[0]
            affiliate_link = href + f"?tag={AFFILIATE_TAG}"
            price_txt = price.get_text(strip=True) + "₹"

            deals.append({
                "title": name,
                "price": price_txt,
                "link": affiliate_link
            })

        if len(deals) >= 3:
            break

    return deals

# Function to send messages to Telegram channel
def send_messages():
    deals = extract_amazon_deals()

    for deal in deals:
        message = f"📦 <b>{deal['title']}</b>\n" \
                  f"💰 <b>Price:</b> {deal['price']}\n\n" \
                  f"🛒 <a href='{deal['link']}'>Buy on Amazon</a>\n" \
                  f"📤 <a href='{deal['link']}'>Share with friends</a>"

        bot.send_message(
            chat_id=CHANNEL_ID,
            text=message,
            parse_mode=telegram.ParseMode.HTML,
            disable_web_page_preview=True
        )

# Run the script
if __name__ == "__main__":
    send_messages()
