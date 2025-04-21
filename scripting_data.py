from playwright.sync_api import sync_playwright
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import logging
import time
import json

logging.basicConfig(level=logging.INFO, format="🔍 %(message)s")


SEARCH_URL = "https://www.opentable.com/s?dateTime=2025-04-21T19%3A00%3A00&covers=1&latitude=37.532536&longitude=-121.976059&term=Fremont&shouldUseLatLongSearch=true"

# -------------
# get name of restaurant
# -------------


def get_name(soup):
    try:
        name_tag = soup.find("h1", class_="E-vwXONV9nc-")
        return name_tag.get_text(strip=True) if name_tag else "Unknown"
    except Exception:
        return "Unknown"


# -------------
# get photo url
# -------------


def get_photo_url(soup):
    try:
        banner_div = soup.find("div", class_="KA0zRX5Kt1Q-")
        if banner_div:
            img_tag = banner_div.find("img")
            return img_tag["src"] if img_tag and img_tag.get("src") else "No photo URL"
        return "No photo section"
    except Exception:
        return "Error fetching photo"


# -------------
# get description
# -------------
def get_description(soup):
    try:
        desc_tag = soup.find(
            "span", class_="l9bbXUdC9v0- ZatlKKd1hyc- ukvN6yaH1Ds- l-AMWW5ZrIg-"
        )
        return desc_tag.get_text(strip=True) if desc_tag else "No description found."
    except Exception:
        return "No description found."


# -------------
# get address
# -------------
def get_address_and_map(soup):
    try:
        section = soup.find("section", class_="h-fXgjNfWDc-")
        a_tag = section.find("a", href=True)
        map_url = a_tag["href"] if a_tag else "Unknown"

        address_tag = section.find("p")
        address = (
            address_tag.get_text(strip=True).replace("\n", ", ")
            if address_tag
            else "Unknown"
        )

        return address, map_url
    except Exception:
        return "Unknown", "Unknown"


# -------------
# get hours of operation
# -------------
def get_hours_of_operation(soup):
    try:
        sections = soup.find_all("div", class_="ugL-ExXtGrk-")
        for section in sections:
            title = section.find("span", class_="_0p64hHgVLY4-")
            if title and "Hours of operation" in title.get_text():
                content_div = section.find("div", class_="-XkftahGV5Y-")
                return content_div.get_text(separator="\n", strip=True)
        return "Unknown"
    except Exception:
        return "Unknown"


# -----------------
# get price range
# -----------------
def get_price_range(soup):
    try:
        sections = soup.find_all("div", class_="ugL-ExXtGrk-")
        for section in sections:
            title = section.find("span", class_="_0p64hHgVLY4-")
            if title and "Price" in title.get_text():
                content_div = section.find("div", class_="-XkftahGV5Y-")
                return content_div.get_text(strip=True)
        return "Unknown"
    except Exception:
        return "Unknown"


# -------------
# get cuisine
# -------------
def get_cuisine(soup):
    try:
        sections = soup.find_all("div", class_="ugL-ExXtGrk-")
        for section in sections:
            title = section.find("span", class_="_0p64hHgVLY4-")
            if title and "Cuisines" in title.get_text():
                content_div = section.find("div", class_="-XkftahGV5Y-")
                return content_div.get_text(strip=True)
        return "Unknown"
    except Exception:
        return "Unknown"


# -------------
# get rating
# -------------
def get_rating(soup):
    try:
        rating_tag = soup.find("span", class_="m1KNa9XKCHY-")
        return rating_tag.get_text(strip=True) if rating_tag else "Unknown"
    except Exception:
        return "Unknown"


# -------------
# get all reviews
# -------------
def get_all_reviews(page) -> list:
    all_reviews = []
    last_first_review = ""

    while True:
        html = page.content()
        soup = BeautifulSoup(html, "html.parser")
        review_items = soup.select('li[data-test="reviews-list-item"]')

        if not review_items:
            break

        first_review_text = review_items[0].get_text(strip=True)

        # ⛔ Prevent infinite loop on repeating page
        if first_review_text == last_first_review:
            break
        last_first_review = first_review_text

        for review in review_items:
            try:
                # 📝 Review text
                text_tag = review.select_one(
                    "span.l9bbXUdC9v0-.ZatlKKd1hyc-.ukvN6yaH1Ds-"
                )
                review_text = (
                    text_tag.get_text(strip=True) if text_tag else "No review text"
                )

                # 🙋 Reviewer name
                name_tag = review.select_one("p.RUDcRcUiZI4-.C7Tp-bANpE4-")
                reviewer_name = (
                    name_tag.get_text(strip=True) if name_tag else "Anonymous"
                )

                # ⭐ Rating
                rating_tag = review.select_one("li.-k5xpTfSXac- span")
                rating = rating_tag.get_text(strip=True) if rating_tag else "N/A"

                all_reviews.append(
                    {"reviewer": reviewer_name, "rating": rating, "text": review_text}
                )
            except Exception as e:
                all_reviews.append(
                    {
                        "reviewer": "Error",
                        "rating": "Error",
                        "text": f"Failed to parse: {e}",
                    }
                )

        # ⏭️ Try to click 'Next'
        next_btn = page.query_selector('a[aria-label="Go to the next page"]')
        if next_btn and "disabled" not in (next_btn.get_attribute("class") or ""):
            try:
                next_btn.click()
                page.wait_for_selector(
                    "li[data-test='reviews-list-item']", timeout=2000
                )
            except:
                break  # break if next page fails to load
        else:
            break

    return all_reviews


# -------------------
# collect all restsaurant links
# -------------------
def collect_all_restaurant_links(page) -> list:
    logging.info("📋 Collecting all restaurant links across pages...")
    all_links = set()
    page_number = 1
    last_first_link = ""

    while True:
        logging.info(f"📄 Scraping page #{page_number}...")

        # Scroll to bottom to trigger lazy loading
        for _ in range(5):
            page.mouse.wheel(0, 2500)
            time.sleep(0.5)

        # Wait and extract restaurant cards
        try:
            page.wait_for_selector("a[data-test='res-card-name']", timeout=5000)
            cards = page.query_selector_all("a[data-test='res-card-name']")
        except Exception:
            logging.warning("⚠️ Could not find restaurant cards.")
            break

        new_links = [
            el.get_attribute("href")
            for el in cards
            if el.get_attribute("href") and el.get_attribute("href").startswith("https")
        ]

        logging.info(f"🔗 Found {len(new_links)} links on this page.")
        if not new_links:
            logging.info("🛑 No links found — stopping.")
            break

        # Prevent infinite loop by checking the first link
        first_link = new_links[0]
        if first_link == last_first_link:
            logging.info("🌀 Same first link detected — likely looping. Breaking.")
            break
        last_first_link = first_link

        before = len(all_links)
        all_links.update(new_links)
        after = len(all_links)

        if after == before:
            logging.info("🛑 No new unique links added — breaking loop.")
            break

        # Check if "next button container" exists and is not disabled
        next_container = page.query_selector("div.TkpxbcBbu80-")
        next_btn = page.query_selector('a[aria-label="Go to the next page"]')

        if (
            next_container
            and next_btn
            and "disabled" not in (next_btn.get_attribute("class") or "")
        ):
            try:
                logging.info("⏭️ Clicking next page...")
                next_btn.click()

                # Scroll again after clicking
                for _ in range(3):
                    page.mouse.wheel(0, 2500)
                    time.sleep(0.5)

                # Wait for next set of cards
                page.wait_for_selector("a[data-test='res-card-name']", timeout=5000)
                page_number += 1
            except Exception as e:
                logging.warning(f"⚠️ Failed to click next page: {e}")
                break
        else:
            logging.info("✅ No more pages or next button disabled.")
            break

    return list(all_links)


# -------------------
# scrape restaurant
# -------------------


# Place this outside scrape_restaurant_names
def scrape_single_restaurant(href: str):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        try:
            page.goto(href, wait_until="domcontentloaded", timeout=10000)
            soup = BeautifulSoup(page.content(), "html.parser")

            name = get_name(soup)
            photo_url = get_photo_url(soup)
            description = get_description(soup)
            address, map_url = get_address_and_map(soup)
            hours = get_hours_of_operation(soup)
            price = get_price_range(soup)
            cuisine = get_cuisine(soup)
            rating = get_rating(soup)
            reviews = get_all_reviews(page)

            logging.info(f"➡️ {name} | Reviews: {len(reviews)}")
            return {
                "name": name,
                "photo_url": photo_url,
                "description": description,
                "address": address,
                "map_url": map_url,
                "hours": hours,
                "price": price,
                "cuisine": cuisine,
                "rating": rating,
                "reviews": reviews,
            }
        except Exception as e:
            logging.warning(f"⚠️ Error scraping {href}: {e}")
            return {"error": str(e), "href": href}
        finally:
            browser.close()


# Then modify scrape_restaurant_names like this:
def scrape_restaurant_names():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        logging.info("🌐 Navigating to search page...")
        page.goto(SEARCH_URL, wait_until="domcontentloaded")

        try:
            page.click("button.save-preference-btn-handler", timeout=5000)
            logging.info("🍪 Accepted cookies.")
        except:
            logging.info("✅ No cookie prompt.")

        links = collect_all_restaurant_links(page)
        logging.info(f"📦 Found {len(links)} restaurants.")

        browser.close()  # Close main page before spawning threads

    # 🚀 Parallel scraping
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = list(executor.map(scrape_single_restaurant, links))

    logging.info(f"✅ Finished scraping {len(results)} restaurants.")

    with open("scraped_restaurants.json", "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    logging.info("📝 Scraped data saved to scraped_restaurants.json")


if __name__ == "__main__":
    logging.info("🚀 Starting name + URL scraper...")
    scrape_restaurant_names()
