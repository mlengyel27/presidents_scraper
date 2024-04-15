# This code uses BeautifulSoup to build customizable corpora from the website of The American Presidency Project 
# Users can input a president whose speeches they wish to collect, the filename and the location of the corpus files

import requests
from bs4 import BeautifulSoup
import os
import re
import time
import random

# customizable parameters
# president_number = "5" number of president
# filepath =  location of newly created corpora
# title_as_filename = if true filename will be autoincremented ID + title of document
# title_included = true/false = include/exclude title of document in the textfiles

def tapp_scraper(president_number, filepath,  title_as_filename, title_included):
    pres_number = int(president_number) + 200256
    base_url = "https://www.presidency.ucsb.edu/"
    # using the advanced query page, since the presidents' individual pages are dynamic, could not be scraped with bs4
    pres_page_url = f"https://www.presidency.ucsb.edu/advanced-search?field-keywords=&field-keywords2=&field-keywords3=&from%5Bdate%5D=&to%5Bdate%5D=&person2={pres_number}&items_per_page=25&page="

    # Initialize lists needed
    urls = []
    hrefs = []
    full_urls = []

    page_counter = 0
    while True:
        url = f"{pres_page_url}{page_counter}" # iterate through all the pages of the category
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        td_tags = soup.find_all('td', class_='views-field views-field-title')

        # Iterate over each 'td' tag and find 'a' tags within them
        hrefs = [td.find('a')['href'] for td in td_tags if td.find('a')]
    
        if not hrefs: #break the loop after last page
            break
        else:
            page_counter += 1
            urls.append(url)

        # Extract the references from the a tag on the pages and reconstruct their full URL
        for href in hrefs:
            full_url = f"{base_url}{href}"
            full_urls.append(full_url)
        
        time.sleep(random.uniform(1, 4)) # mimic human-like behaviour

    # Write the URLs to a file
    with open('presidents_urls.txt', 'w', encoding='utf-8') as out_file:
        for url in full_urls:
            out_file.write(url + '\n')

    # Create a new directory named after the president + autoincremented ID
    print(pres_page_url)
    pres_name_response = requests.get(pres_page_url)
    soup = BeautifulSoup(pres_name_response.text, 'html.parser')
    pres_name = soup.find('td', class_='views-field views-field-field-docs-person text-nowrap')
    folder_name = f"{president_number}_{pres_name.get_text (strip = True).replace(' ', '_')}"
    out_file_path = os.path.join(filepath, folder_name)
    os.makedirs(out_file_path, exist_ok=True)
    print(folder_name)

    # Create files named in order, report back on success and failure ratio
    file_counter = 0
    failure_counter = 0
    success_counter = 0
    for full_url in full_urls:
        file_counter += 1
        # Scrape title and body on each page
        response_type = requests.get(full_url)
        soup_type = BeautifulSoup(response_type.text, 'html.parser')
        title = soup_type.find('div', class_='field-ds-doc-title')
        body = soup_type.find('div', class_='field-docs-content')
        if title is not None and title_as_filename:
            title_text = title.get_text(strip=True)
            # clean title and shorten if necessary
            new_file_name_formatted = re.sub(r'[^\w\s\\/]+', '', title_text.replace(' ', '_')).replace('\r', '').replace('\n', '').replace('/', '')
            if len(new_file_name_formatted) + len(filepath) + len(folder_name)+ len('_') + len('txt') < 250:
                new_file_name = new_file_name_formatted
            else:
                new_file_name = new_file_name_formatted[:110]
        elif not title_as_filename:
            new_file_name = f'{folder_name}{file_counter}'

        with open(os.path.join(out_file_path, f'{file_counter}_{new_file_name}.txt'), 'w', encoding='utf-8') as out_file:
            # check if there is a title and body, write result in file
                if title_included == True:
                    if title and body:
                        title_text = title.get_text(strip=True)
                        body_text = body.get_text(strip=True)
                        out_file.write(f"{title_text}\n{body_text}\n")
                        success_counter += 1
                    else:
                        out_file.write(f"Title, body not found for {full_url}\n")
                        failure_counter += 1
                else:
                    if  body:
                        body_text = body.get_text(strip=True)
                        out_file.write(f"{body_text}\n")
                        success_counter += 1
                    else:
                        out_file.write(f"Body not found for {full_url}\n")
                        failure_counter += 1


    print("Number of texts failed to retrieve for", president_number, ": " ,failure_counter)
    print("Number of texts retrieved", president_number, ": " , success_counter)

# scrape speeches for first 10 presidents
for i in range(1,10):
    tapp_scraper(i, 'filepath', title_as_filename = True, title_included = False)
