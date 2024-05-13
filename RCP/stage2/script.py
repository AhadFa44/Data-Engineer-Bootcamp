import requests
from bs4 import BeautifulSoup
import pandas as pd
from openpyxl import Workbook
import subprocess
import toml
from urllib.parse import urljoin

def get_dic_machine(url):
    html = requests.get(url)
    soup = BeautifulSoup(html.text, "html.parser")
    machineDictionary = dict.fromkeys(['reference_number','watch_URL','type','brand','year_introduced',
                                       'parent_model','specific_model','nickname','marketing_name','style','currency',
                                       'price', 'image_URL','made_in','case_shape','case_material','case_finish','caseback',
                                       'diameter','between_lugs','lug_to_lug','case_thickness','bezel_material','bezel_color',
                                       'crystal','water_resistance','weight','dial_color','numerals','bracelet_material',
                                       'bracelet_color','clasp_type','movement','caliber','power_reserve','frequency',
                                       'jewels','features', 'description','short_description'])
    machineCollection = soup.find('section',id = 'collection')
    collection =  machineCollection.find_all('p',class_='xs-small')
    collection_list = []
    for i in collection:
        listtemp =[]
        listnull =['','','']
        for index,c in enumerate(i):
            listtemp.append(c.text)
            listtemp=list(filter(lambda a: a != '', listtemp))
        for index,c in enumerate(listtemp):
            check =True
            for i in c:
                if i.isnumeric():
                    if check == True:
                        check =True
                elif i == ' ':
                    if check == True:
                        check =True 
                else:
                    check =False    
            if check ==True:
                c=c.replace(" ", "")
            if (c.count('.') == 2)|(c.count('.') == 3)|((c.count('.') == 1)&(c.count('/') == 1))|((c.count('-') == 3)):
                if listnull[0] == '':
                    listnull[0]=c
                elif 'Limited edition' in c:        
                    x = c.split("Limited edition")
                    x[1] = "Limited edition" + x[1]  
                    listnull[1]=x[0]      
                    listnull[2]=x[1]     
            elif ((c.count('.') == 2)|(c.count('.') == 3)|((c.count('.') == 1)&(c.count('/') == 1))|((c.count('-') == 3))|c.isnumeric()|c.startswith("Limited")|c.endswith('Uniques')|c.endswith('unique')|c.startswith("Unique piece"))==False:
                num = c.replace('.','')
                if (c.count('.')==1)&(num.isnumeric()):
                    listnull[0]=c
                else:   
                    if 'Limited edition' in c:        
                        x = c.split("Limited edition")
                        x[1] = "Limited edition" + x[1]  
                        listnull[1]=x[0]      
                        listnull[2]=x[1] 
                    else:           
                        if listnull[1]=='':
                            listnull[1]=c
                        else: 
                            listnull[1]=listnull[1]+" "+c                     
            elif c.isnumeric()|c.startswith("Limited")|c.endswith('Uniques')|c.endswith('unique')|c.startswith("Unique piece"):
                    if c.startswith("Limited"):
                       listnull[2]=c
                    elif c.isnumeric():
                       listnull[2]=c
                    elif c.endswith('Uniques')|c.endswith('unique')|c.startswith("Unique piece"):    
                       listnull[2]=listnull[2]+' '+c                            
        collection_list.append(listnull)  
    specific_model = soup.find('h1')
    specific_model = specific_model.text.strip()
    marketing_name =[]
    machine_category = machineCollection.find_all('a',class_ ="lgitem")
    if machine_category == []:
        category = machineCollection.find_all('h3')
        for i in category:
            if i:
                    machine_edition = i.text.strip()
                    substr_to_remove = specific_model
                    machine_edition = machine_edition.replace(substr_to_remove, "")
                    marketing_name.append(machine_edition)               
    else:
        for i in machine_category:
            machine_cat = i.find('h3')
            if machine_cat:
                    machine_edition = machine_cat.text.strip()
                    substr_to_remove = specific_model
                    machine_edition = machine_edition.replace(substr_to_remove, "")
                    marketing_name.append(machine_edition)
    image_url = []
    if machine_category == []:
        machine_category = machineCollection.find_all('img')
        for img in machine_category:
                src = img.get("data-src")
                if src:
                    src = requests.compat.urljoin(url, src)
                    image_url.append(src)
    else:    
        for img in machine_category:
                    src = img.get("href")
                    if src:
                        src = requests.compat.urljoin(url, src)
                        image_url.append(src)  
    brand = soup.find('a',class_='main')
    brand =brand.text.strip()
    brand = brand.upper()   
    parent_model = url.split('/')[-2] 
    parent_model = parent_model.replace('-', " ") 
    parent_model = parent_model.capitalize()   
    machine = soup.find('section',id='machine')
    machine = machine.find_all('h3')
    checkcont=False
    checkmovement=False
    Checkfeature=False
    for sec in machine:
        word = sec.text.strip()
        word=word.lower() 
        if ('case' in word):
            case_material=sec.find_all_next()
            cont = ''
            for i in case_material:
                if i.name == 'ul':
                    continue
                elif i.name != 'h3':
                    cont =cont+'\n'+i.text  
                    checkcont =True  
                else:
                    break   
        else:
            if checkcont!=True:
                cont=''              
        if ('engine' in word):
            enginsec=sec.find_all_next()
            movement=''
            for i in enginsec:
                if i.name == 'ul':
                    continue
                elif i.name != 'h3':
                    movement =movement+'\n'+i.text
                    checkmovement=True
                else:
                    break  
        else:
            if checkmovement!=True:
                movement=''          
        if ('function' in word):
            funsec=sec.find_all_next()
            feature=''
            for i in funsec:
                if i.name == 'ul':
                    continue
                elif (i.name ==  'li'):
                    feature =feature+'\n'+i.text
                    Checkfeature=True
                else:
                    break 
        else:
            if Checkfeature!=True:
                feature=''         
    feature = feature.replace('\n', " ")             
    description = soup.find('section',id='overview')
    descr =''
    description1 = description.find_all('p')
    for des in description1:
            descr = descr+des.text.strip()  
    descr = descr.replace('\n', " ")                       
    machineDictionary["reference_number"]=[]
    machineDictionary["nickname"]=[]
    machineDictionary["short_description"]=[]
    machineDictionary["specific_model"]=[]
    machineDictionary["marketing_name"]=[]
    machineDictionary["image_URL"]=[]
    machineDictionary["specific_model"]=[]
    machineDictionary["watch_URL"]=[]
    machineDictionary["brand"]=[]
    machineDictionary["parent_model"]=[]
    machineDictionary["case_material"]=[]
    machineDictionary["diameter"]=[]
    machineDictionary["between_lugs"]=[]
    machineDictionary["lug_to_lug"]=[]
    machineDictionary["case_thickness"]=[]
    machineDictionary["movement"]=[]
    machineDictionary["caliber"]=[]
    machineDictionary["power_reserve"]=[]
    machineDictionary["frequency"]=[]
    machineDictionary["jewels"]=[]
    machineDictionary["features"]=[]
    machineDictionary["description"]=[]
    for i in collection_list:
        machineDictionary["reference_number"].append(i[0])
        machineDictionary["nickname"].append(i[1])
        machineDictionary["short_description"].append(i[2])
    machineDictionary["marketing_name"]= marketing_name    
    machineDictionary["image_URL"]=image_url
    for i in machineDictionary["nickname"]:
        machineDictionary["specific_model"].append(specific_model)
        machineDictionary["watch_URL"].append(url)
        machineDictionary["brand"].append(brand)
        machineDictionary["parent_model"].append(parent_model)
        machineDictionary["case_material"].append(cont)
        machineDictionary["diameter"].append(cont)
        machineDictionary["between_lugs"].append(cont)
        machineDictionary["lug_to_lug"].append(cont)
        machineDictionary["case_thickness"].append(cont)
        machineDictionary["movement"].append(movement)
        machineDictionary["caliber"].append(movement)
        machineDictionary["power_reserve"].append(movement)
        machineDictionary["frequency"].append(movement)
        machineDictionary["jewels"].append(movement)
        machineDictionary["features"].append(feature)
        machineDictionary["description"].append(descr)
    return machineDictionary        


# this is function that will deal with watches that doesn't have collection section 
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


# here we will save the result into S3 bucket
if __name__=="__main__": 
    app_config = toml.load('config_file.toml')
    bucket=app_config['s3']['bucket']
    folder=app_config['s3']['folder']



urls=[
'https://www.mbandf.com/en/machines/co-creations/musicmachine1-reloaded',
'https://www.mbandf.com/en/machines/co-creations/orb',
'https://www.mbandf.com/en/machines/co-creations/tripod',
'https://www.mbandf.com/en/machines/co-creations/destination-moon',
'https://www.mbandf.com/en/machines/co-creations/starfleet-explorer',
'https://www.mbandf.com/en/machines/co-creations/project-lpx',
'https://www.mbandf.com/en/machines/co-creations/t-rex',
'https://www.mbandf.com/en/machines/co-creations/medusa',
'https://www.mbandf.com/en/machines/co-creations/grant',
'https://www.mbandf.com/en/machines/co-creations/the-fifth-element',
 'https://www.mbandf.com/en/machines/co-creations/Kelys-Chirp',
'https://www.mbandf.com/en/machines/co-creations/octopod',
'https://www.mbandf.com/en/machines/co-creations/astrograph',
'https://www.mbandf.com/en/machines/co-creations/balthazar',
'https://www.mbandf.com/en/machines/co-creations/sherman',
'https://www.mbandf.com/en/machines/co-creations/arachnophobia',
'https://www.mbandf.com/en/machines/co-creations/musicmachine3',
'https://www.mbandf.com/en/machines/co-creations/musicmachine2',
'https://www.mbandf.com/en/machines/co-creations/starfleet-machine',
'https://www.mbandf.com/en/machines/co-creations/musicmachine1',
'https://www.mbandf.com/en/machines/co-creations/melchior',
'https://www.mbandf.com/en/machines/performance-art/lmflyingt-ice-blizzard-emmanuel-tarpin',
'https://www.mbandf.com/en/machines/performance-art/lmflyingtallegra-mbandf-bulgari',
'https://www.mbandf.com/en/machines/performance-art/lmse-eddy-jaquet',
'https://www.mbandf.com/en/machines/performance-art/lm101-mbandf-hmoser',
'https://www.mbandf.com/en/machines/performance-art/moonmachine2',
'https://www.mbandf.com/en/machines/performance-art/lm1-silberstein',
'https://www.mbandf.com/en/machines/performance-art/BlackBadger',
'https://www.mbandf.com/en/machines/performance-art/lm1-xiahang',
'https://www.mbandf.com/en/machines/performance-art/moonmachine',
'https://www.mbandf.com/en/machines/performance-art/experimentzr012',
'https://www.mbandf.com/en/machines/performance-art/jwlrymachine',
'https://www.mbandf.com/en/machines/legacy-machines/lm1',
'https://www.mbandf.com/en/machines/legacy-machines/lm2',
'https://www.mbandf.com/en/machines/legacy-machines/lmperpetual',
'https://www.mbandf.com/en/machines/legacy-machines/lmse',
'https://www.mbandf.com/en/machines/legacy-machines/lmse-evo',
'https://www.mbandf.com/en/machines/legacy-machines/lm101',
'https://www.mbandf.com/en/machines/legacy-machines/lmflyingt',
'https://www.mbandf.com/en/machines/legacy-machines/lmthunderdome',
'https://www.mbandf.com/en/machines/legacy-machines/lmp-evo',
'https://www.mbandf.com/en/machines/legacy-machines/lmx',
'https://www.mbandf.com/en/machines/legacy-machines/lmsequential-evo',
'https://www.mbandf.com/en/machines/horological-machines/hm1',
'https://www.mbandf.com/en/machines/horological-machines/hm2',
'https://www.mbandf.com/en/machines/horological-machines/hm3',
'https://www.mbandf.com/en/machines/horological-machines/hm3-frog',
'https://www.mbandf.com/en/machines/horological-machines/hm3-megawind',
'https://www.mbandf.com/en/machines/horological-machines/hm4',
'https://www.mbandf.com/en/machines/horological-machines/hm5',
'https://www.mbandf.com/en/machines/horological-machines/hm6',
'https://www.mbandf.com/en/machines/horological-machines/hmx',
'https://www.mbandf.com/en/machines/horological-machines/hm7',
'https://www.mbandf.com/en/machines/horological-machines/hm8',
'https://www.mbandf.com/en/machines/horological-machines/hm9',
'https://www.mbandf.com/en/machines/horological-machines/hm10',
'https://www.mbandf.com/en/machines/horological-machines/hm8-mark-2',
'https://www.mbandf.com/en/machines/horological-machines/hm11']

urlls=[
    'https://www.mbandf.com/en/machines/co-creations/tom-and-t-rex',
    'https://www.mbandf.com/en/machines/performance-art/hmoser-mbandf-streamliner-pandamonium',
    'https://www.mbandf.com/en/machines/performance-art/hm10-panda-only-watch',
    'https://www.mbandf.com/en/machines/performance-art/hm8-only-watch',
    'https://www.mbandf.com/en/machines/performance-art/hm4-only-watch',
    'https://www.mbandf.com/en/machines/performance-art/hm2-2-black-box',
    'https://www.mbandf.com/en/machines/performance-art/hm2-only-watch' ]


categories_list=[]
df_watch=pd.DataFrame()
for url in urls:
    categories_list=get_dic_machine(url)
    df=pd.DataFrame.from_dict(categories_list)
    df_watch=pd.concat([df_watch,df])
df_watch.to_csv('MBandF_Brands.csv')
#df_watch.to_excel('MBandF_Brands.xlsx',index=False)
subprocess.call(['aws','s3','cp','MBandF_Brands.csv', f's3://{bucket}/{folder}/MBandF_Brands.csv'])# from EC2 to S3

machine_details_list = []

for urll in urlls:
    machine_details = get_machine_details(urll)
    machine_details_list.append(machine_details)

df_watch = pd.DataFrame(machine_details_list)
df_watch.to_csv('MBandF_Brands_without_collection.csv')
#df_watch.to_excel('MBandF_Brands_without_collection.xlsx',index=False)
subprocess.call(['aws','s3','cp','MBandF_Brands_without_collection.csv', f's3://{bucket}/{folder}/MBandF_Brands_without_collection.csv'])

print('save file')