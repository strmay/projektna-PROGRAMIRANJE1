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