import requests
import re
import os
import csv

bil_url = "https://www.billboard.com/charts/billboard-200"

bil_directory = "podatki"

frontpage_filename = "glavna.html"

csv_filename = "bil.csv"

def download_url_to_string(url):
    try:
        r = requests.get(url)
        # del kode, ki morda sproži napako
    except requests.exceptions.ConnectionError:
        # koda, ki se izvede pri napaki
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        return "Ne deluje"
    # nadaljujemo s kodo če ni prišlo do napake
    return r.text
    
def save_string_to_file(text, directory, filename):
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
        return None

def save_frontpage():
    text = download_url_to_string(bil_url)
    save_string_to_file(text, bil_directory, frontpage_filename)
    return None


def read_file_to_string(directory, filename):
    path = os.path.join(directory, filename)
    with open(path, 'r') as file_in:
        return file_in.read()

def page_to_ads(page):
    ads = []
    #prvi_ad = []                               #TO ZDEJ ŠTIMA(MAL GRDO THO)
    #zadnji_ad = []
    #prvi album je malce posebno predstavljen
    prvi_ad = [ujem.group(0) for ujem in re.finditer(r'<div class="container container--no-background chart-number-one">(.*?)<div class="ad-container leaderboard leaderboard--top">', page, re.DOTALL)]
    zadnji_ad = [mec.group(0) for mec in re.finditer(r'data-rank="200"(.*?)WEEKS ON CHART', page, re.DOTALL)]
    for i in range(2, 200): 
        for ujemanje in re.finditer(r'(data-rank="{}".*?)data-rank="{}"'.format(i, i+1), page, re.DOTALL):
            ads.append(ujemanje.group(1))
    return prvi_ad + ads + zadnji_ad

def get_dict_from_ad_block(block):
    rx = re.compile(r'data-rank="(?P<rank>\d+)".*data-artist="(?P<artist>.*)" data-title="(?P<title>.*)" data-has-content'
                    r'.*<div class="chart-list-item__last-week">(?P<last_week>\d+)</div>'
                    r'.*<div class="chart-list-item__weeks-at-one">(?P<peek_position>\d+)</div>'
                    r'.*<div class="chart-list-item__weeks-on-chart">(?P<weeks_on_chart>\d+)</div>',
                    re.DOTALL)
    rx_nove = re.compile(r'data-rank="(?P<rank>\d+)".*data-artist="(?P<artist>.*)" data-title="(?P<title>.*)" data-has-content', re.DOTALL)
    try:
        data = re.search(rx, block)
        ad_dict = data.groupdict()
        ad_dict["last_week"] = int(ad_dict["last_week"])
        ad_dict["peek_position"] = int(ad_dict["peek_position"])
        ad_dict["weeks_on_chart"] = int(ad_dict["weeks_on_chart"])
    except:
        data = re.search(rx_nove, block)
        ad_dict = data.groupdict()
        ad_dict["last_week"] = "None"
        ad_dict["peek_position"] = "None"
        ad_dict["weeks_on_chart"] = "None"
    return ad_dict

def ads_from_file(directory, filename, page):
    ads = []
    #prvi album je malce posebno predstavljen
    prvi_ad = [ujem.group(0) for ujem in re.finditer(r'<div class="container container--no-background chart-number-one">(.*?)<div class="ad-container leaderboard leaderboard--top">', page, re.DOTALL)]
    zadnji_ad = [mec.group(0) for mec in re.finditer(r'data-rank="200"(.*?)WEEKS ON CHART', page, re.DOTALL)]
    for i in range(2, 200): 
        for ujemanje in re.finditer(r'(data-rank="{}".*?)data-rank="{}"'.format(i, i+1), page, re.DOTALL):
            ads.append(ujemanje.group(1))
    ads += zadnji_ad
    sez2 = []
    for block in ads:
        c = get_dict_from_ad_block(block)
        sez2.append(c)
    rx1 = re.compile(r'<div class="chart-number-one__weeks-at-one">(?P<weeks_at_no1>\d+)</div>'
                     r'.*<div class="chart-number-one__weeks-on-chart">(?P<weeks_on_chart>\d+)</div>'
                     r'.*<div class="chart-number-one__title">(?P<title>.*?)</div>'
                     r'.*<div class="chart-number-one__artist">\\n(?P<artist>.*?)\\n</div>',
                     re.DOTALL)
    data = re.search(rx1, str(prvi_ad))
    return sez2

def write_csv(fieldnames, rows, directory, filename):
    '''Write a CSV file to directory/filename. The fieldnames must be a list of
    strings, the rows a list of dictionaries each mapping a fieldname to a
    cell-value.'''
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return None

def write_bil_to_csv(ads, directory, filename):
    write_csv(ads[0].keys(), ads, directory, filename)

def bil_to_csv_save(ads):
    write_bil_to_csv(ads, bil_directory, csv_filename)

