from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import json


def fetchPage():
    URL = 'https://ex.indead.com/jobs?q=programming&start=0'

    with sync_playwright() as p:
        browser = p.chromium.launch()
        context = browser.new_context(user_agent="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36")
        page = context.new_page()
        page.goto(URL)
        page.screenshot(path='indeed.png', full_page=True)

        content = page.content()
        soup = BeautifulSoup(content, 'html.parser')

        # with open("indeed.html", 'w') as file:
        #     file.write(soup.prettify())
        
        listing = soup.select('.resultContent')
        jobs = []

        for list in listing:
            title = list.select('.jobTitle')[0].get_text()
            company_name = list.select('[data-testid="company-name"]')[0].get_text()
            location = list.select('[data-testid="text-location"]')[0].get_text()
            jobs.append({
                'Title': title,
                'Company Name': company_name,
                'Location': location
            })
        with open('jobs.json', 'w') as file:
            json.dump(jobs, file, indent=2)

        print("Jobs saved to JSON file")
        browser.close()

fetchPage()
