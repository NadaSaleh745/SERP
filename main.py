from bs4 import BeautifulSoup
import requests
import pandas as pd
import csv
import os
from datetime import datetime


def file_exists_with_same_content(file_path, header, data):
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='UTF8') as file:
            reader = csv.reader(file)
            file_content = list(reader)

        if file_content == [header] + data:
            return True
    return False


headers = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                  "AppleWebKit/537.36 (KHTML, like Gecko)"
                  " Chrome/131.0.0.0 Safari/537.36"
}

keywords = input("Enter your keywords: ")
numPages = int(input("Enter the number of pages to scrape: "))
numResults = int(input("Enter the number of results per page: "))

Header = ['id', 'Page', 'Website', 'URL']
file_path = 'SERP.csv'
data = []
with open(file_path, 'w', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(Header)

    for page in range(numPages):
        start = page * numResults
        url = f'https://www.google.com/search?q={keywords}&start={start}&num={numResults}'
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.findAll('div', {'class': 'tF2Cxc'})
            print(f"Page {page + 1}: ")
            result_count = len(results)

            for idx, result in enumerate(results, start=1):
                pageName = result.find('h3')
                link = result.find('a', href=True)
                if pageName and link:
                    name = pageName.text.strip()
                    url = link['href']
                    website = url.split('/')[2] if 'http' in url else "No Website"

                    print(f"{idx}. Page: {name}, Website: {website}, URL: {url}")

                    data.append(([idx, name, website, url]))

            if result_count < numResults:
                print(f"Warning: Only {result_count} results found on page {page + 1}")

        else:
            print(f"Failed to retrieve results for page {page + 1}. Status code: {response.status_code}")

if file_exists_with_same_content(file_path, Header, data):
    print(f"The file '{file_path}' already exists with the same content.")
else:
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    new_file_path = f'SERP_{timestamp}.csv'
    with open(new_file_path, 'w', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(Header)
        writer.writerows(data)
    print(f"New file '{new_file_path}' created successfully!")

