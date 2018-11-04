import requests
import re
import os
import csv

bil_url = "https://www.billboard.com/charts/billboard-200"

bil_directory = "podatki"

frontpage_filename = "glavna.html"

csv_filename = "bil.csv"

def download_url_to_string(url):
    '''This function takes a URL as argument and tries to download it
    using requests. Upon success, it returns the page contents as string.'''
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
    '''Write "text" to the file "filename" located in directory "directory",
    creating "directory" if necessary. If "directory" is the empty string, use
    the current directory.'''
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
    '''Return the contents of the file "directory"/"filename" as a string.'''
    path = os.path.join(directory, filename)
    with open(path, 'r') as file_in:
        return file_in.read()

def page_to_ads(page):
    '''Split "page" to a list of advertisement blocks.'''
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
    '''Build a dictionary containing the name, description and price
    of an ad block.'''
    rx = re.compile(r'data-rank="(?P<rank>\d+)"',
                    #r'data-artist="(?P<artist>\w+.*)'
                    #r'data-ttile="(?P<title>\w+.*)"',
                    #r'<div class="chart-list-item__last-week">(?P<last_week>\d+)</div>'
                    #r'<div class="chart-list-item__weeks-at-one">(?P<peek_position>\d+)</div>'
                    #r'<div class="chart-list-item__weeks-on-chart">(?P<weeks_on_chart>\d+)</div>',
                    re.DOTALL)
    data = re.search(rx, block)
    ad_dict = data.groupdict()
    return ad_dict

def ads_from_file(directory, filename, page):
    #sez = page_to_ads(read_file_to_string(directory, filename))
    ads = []
    #prvi_ad = []                               #TO ZDEJ ŠTIMA(MAL GRDO THO)
    #zadnji_ad = []
    #prvi album je malce posebno predstavljen
    prvi_ad = [ujem.group(0) for ujem in re.finditer(r'<div class="container container--no-background chart-number-one">(.*?)<div class="ad-container leaderboard leaderboard--top">', page, re.DOTALL)]
    zadnji_ad = [mec.group(0) for mec in re.finditer(r'data-rank="200"(.*?)WEEKS ON CHART', page, re.DOTALL)]
    for i in range(2, 200): 
        for ujemanje in re.finditer(r'(data-rank="{}".*?)data-rank="{}"'.format(i, i+1), page, re.DOTALL):
            ads.append(ujemanje.group(1))
    sez2 = []
    for block in ads:
        c = get_dict_from_ad_block(block)
        sez2.append(c)
    return sez2