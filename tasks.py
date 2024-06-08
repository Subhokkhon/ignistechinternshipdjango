import requests
from bs4 import BeautifulSoup
from celery import shared_task
from .models import ScrapingJob

@shared_task
def scrape_coin_data_task(job_id, coins):
    job = ScrapingJob.objects.get(job_id=job_id)
    job.status = 'IN_PROGRESS'
    job.save()

    results = []
    for coin in coins:
        try:
            result = scrape_coin_data(coin)
            results.append({"coin": coin, "output": result})
        except Exception as e:
            results.append({"coin": coin, "error": str(e)})

    job.result = {"tasks": results}
    job.status = 'COMPLETED'
    job.save()

def scrape_coin_data(coin):
    url = f"https://coinmarketcap.com/currencies/{coin}/"
    response = requests.get(url)
    if response.status_code != 200:
        raise Exception("Failed to retrieve data")

    soup = BeautifulSoup(response.content, 'html.parser')
    # Example scraping logic, this will need to be adjusted based on actual page structure
    price = soup.find('div', class_='priceValue').text.strip().replace('$', '').replace(',', '')
    price_change = soup.find('span', class_='sc-15yy2pl-0 kAXKAX').text.strip().replace('%', '')
    # Add more fields as required...

    data = {
        "price": float(price),
        "price_change": float(price_change),
        # Add more fields as required...
    }
    return data
