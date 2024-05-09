# that with out collection 

import requests
from bs4 import BeautifulSoup
import csv
import pandas as pd
from openpyxl import Workbook
from urllib.parse import urljoin
def get_machine_details(urll):
    html = requests.get(urll)
    soup = BeautifulSoup(html.text, "html.parser")

    machineDictionary = {
        'reference_number': None,'watch_URL': urll,'type': None,'brand': None,'year_introduced': None,
        'parent_model': None,'specific_model': None,'nickname': None,'marketing_name': None,
        'style': None,'currency': None,'price': None,'image_URL': None,'made_in': None,
        'case_shape': None,'case_material': None,'case_finish': None,'caseback': None,
        'diameter': None,'between_lugs': None,'lug_to_lug': None,'case_thickness': None,
        'bezel_material': None,'bezel_color': None,'crystal': None,'water_resistance': None,
        'weight': None,'dial_color': None,'numerals': None,'bracelet_material': None,
        'bracelet_color': None,'clasp_type': None,'movement': None,'caliber': None,
        'power_reserve': None,'frequency': None,'jewels': None,'features': None,
        'description': None,'short_description': None
    }

    # Extracting relevant details
    brand = soup.find('a', class_='main')
    if brand:
        machineDictionary['brand'] = brand.text.strip().upper()

    parent_model = urll.split('/')[-2]
    parent_model = parent_model.replace('-', " ").capitalize()
    machineDictionary['parent_model'] = parent_model



    machine_section = soup.find('section', id='machine')
    if machine_section:
        # Check for different h3 headings and extract corresponding details
        case_heading = machine_section.find('h3', text='Case')
        if case_heading:
            case_material = case_heading.find_next('ul').text.strip()
            machineDictionary['case_material'] = case_material
            
            # Fill other columns with the same value as case_material
            machineDictionary['diameter'] = case_material
            machineDictionary['between_lugs'] = case_material
            machineDictionary['lug_to_lug'] = case_material
            machineDictionary['case_thickness'] = case_material

        movement_heading = machine_section.find('h3', text='Engine')
        if movement_heading:
            movement = movement_heading.find_next('ul').text.strip()
            machineDictionary['movement'] = movement
            
            # Fill other columns with the same value as movement
            machineDictionary['caliber'] = movement
            machineDictionary['power_reserve'] = movement
            machineDictionary['frequency'] = movement
            machineDictionary['jewels'] = movement

        features_heading = machine_section.find('h3', text='Functions / indications')
        if features_heading:
            features = features_heading.find_next('ul').text.strip()
            machineDictionary['features'] = features

    # Find the first image URL within the section with id='machine'
    image_relative_url = soup.find('section', id='machine').find('a', class_='lgitem')['href']
    base_url = 'https://www.mbandf.com'  # Base URL of the website
    image_absolute_url = urljoin(base_url, image_relative_url)  # Convert relative URL to absolute URL
    machineDictionary['image_URL'] = image_absolute_url

    description_section = soup.find('section', id='overview')
    if description_section:
        description1 = description_section.find_all('p')
        descr = ''
        for des in description1:
            descr = descr + des.text.strip()
        machineDictionary['description'] = descr

    return machineDictionary
urlls=[
    'https://www.mbandf.com/en/machines/co-creations/tom-and-t-rex',
    'https://www.mbandf.com/en/machines/performance-art/hmoser-mbandf-streamliner-pandamonium',
    'https://www.mbandf.com/en/machines/performance-art/hm10-panda-only-watch',
    'https://www.mbandf.com/en/machines/performance-art/hm8-only-watch',
    'https://www.mbandf.com/en/machines/performance-art/hm4-only-watch',
    'https://www.mbandf.com/en/machines/performance-art/hm2-2-black-box',
    'https://www.mbandf.com/en/machines/performance-art/hm2-only-watch' ]


machine_details_list = []

for urll in urlls:
    machine_details = get_machine_details(urll)
    machine_details_list.append(machine_details)

df_watch = pd.DataFrame(machine_details_list)
df_watch.to_csv('MBandF_Brands_without_collection.csv')
df_watch.to_excel('MBandF_Brands_without_collection.xlsx',index=False)
print('save file')
