from bs4 import BeautifulSoup
import requests
import csv
import string
import PyPDF2
import io
from pyPdf import PdfFileReader
import json
import re

parsedData = csv.writer(open("parsedHtml.csv", "w"))
parsedData.writerow(["Id", "Role", "Company", "Description"])
url = "https://www.cia.gov/library/publications/the-world-factbook/docs/one_page_summaries.html"
print(url)
data = {}
data['data'] = []
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, features="lxml")
options = soup.select('option')
for option in options:
    if option['value'] and option['data-place-code']:
        values = option['data-place-code']
        url1 = "https://www.cia.gov/library/publications/the-world-factbook/attachments/summaries/"+ values.upper() + "-summary.pdf"
        try:
            print(url1)
            if requests.get(url1).text:
                html_content1 = requests.get(url1).text
                soup1 = BeautifulSoup(html_content1, features="lxml")
                if(soup1.find_all('div', {'class': 'row'})):
                    pass
                else:
                    r = requests.get(url1)
                    f = io.BytesIO(r.content)
                    reader = PdfFileReader(f)
                    contents = reader.getPage(0).extractText().lower().replace(':', ' ')
                    f.close()
                    name = contents.split('geography', 1)[0]
                    #Geography 
                    try:
                        total = re.search(r'geographyareatotal(.*?)land', contents).group(1).strip()
                    except AttributeError:
                        total = "null"
                    try:
                        land = re.search(r'land(.*?)water', contents).group(1).strip()
                    except AttributeError:
                        land = "null"
                    try:
                        water = re.search(r'water(.*?)climate', contents).group(1).strip()
                    except AttributeError:
                        water = "null"
                    try:
                        climate = re.search(r'climate(.*?)natural resources', contents).group(1).strip()
                    except AttributeError:
                         climate = "null"
                    try:
                        naturalResources=re.search(r'natural resources(.*?)government', contents).group(1).strip()
                    except AttributeError:
                        naturalResources = "null"
                        
                    #Government
                    try:
                        chiefOfState = re.search(r'chief of state(.*?)head of government', contents).group(1).strip()
                    except AttributeError:
                       chiefOfState = "null"
                    try:
                        headOfGovernment = re.search(r'head of government(.*?)government type', contents).group(1).strip()
                    except AttributeError:
                        headOfGovernment = "null"
                    try:
                        governmentType = re.search(r'government type(.*?)capital', contents).group(1).strip()
                    except AttributeError:
                        governmentType = "null"
                    try:
                        capital = re.search(r'capital(.*?)legislature', contents).group(1).strip()
                    except AttributeError:
                        capital = "null"
                    try:
                        legislature = re.search(r'legislature(.*?)judiciary', contents).group(1).strip()
                    except AttributeError:
                        legislature = "null"
                    try:
                        judiciary = re.search(r'judiciary(.*?)ambassador to us', contents).group(1).strip()
                    except AttributeError:
                        judiciary = "null"
                    try:
                        ambassadorToUs = re.search(r'ambassador to us(.*?)us ambassador', contents).group(1).strip()
                    except AttributeError:
                        ambassadorToUs = "null"
                    try:
                        uSAmbassador = re.search(r'us ambassador(.*?)people & society', contents).group(1).strip()
                    except AttributeError:
                        uSAmbassador = "null"

                    #People
                    try:
                       population = re.search(r'people & societypopulation(.*?)population growth', contents).group(1).strip() 
                    except AttributeError:
                        population = "null"
                    try:
                       populationGrowth = re.search(r'population growth(.*?)ethnicity', contents).group(1).strip() 
                    except AttributeError:
                        populationGrowth = "null"
                    try:
                        ethnicity = re.search(r'ethnicity(.*?)language', contents).group(1).strip()
                    except AttributeError:
                        ethnicity = "null"
                    try:
                       language = re.search(r'language(.*?)religion', contents).group(1).strip() 
                    except AttributeError:
                        language = "null"
                    try:
                       religion = re.search(r'religion(.*?)urbanization', contents).group(1).strip() 
                    except AttributeError:
                        religion = "null"
                    try:
                        urbanization = re.search(r'urbanizationurban population(.*?)rate of urbanization', contents).group(1).strip()
                    except AttributeError:
                        urbanization = "null"
                    try:
                        literacy = re.search(r'literacy(.*?)economyeconomic', contents).group(1).strip()
                    except AttributeError:
                        literacy = "null"
                    try:
                        economicOverview = re.search(r'economyeconomic overview(.*?)gdp', contents).group(1).strip()
                    except AttributeError:
                        economicOverview = "null"
                    try:
                        gDP= re.search(r'gdp(.*?)gdp per capita', contents).group(1).strip()
                    except AttributeError:
                        gDP = "null"
                    try:
                        gDPPerCapita = re.search(r'gdp per capita(.*?)exports', contents).group(1).strip()
                    except AttributeError:
                        gDPPerCapita = "null"
                    try:
                        exportsTotal = re.search(r'exports(.*?)partners', contents).group(1).strip()
                    except AttributeError:
                        exportsTotal = "null"
                    try:
                        exportpatners = re.search(r'partners(.*?)imports', contents).group(1).strip()
                    except AttributeError:
                        exportpatners = "null"
                    try:
                        importsTotal = re.search( r'imports(.*?)partners', contents).group(1).strip()
                    except AttributeError:
                        importsTotal = "null"
                    try:
                        importpatners = re.search(r'partners(.*?)', contents).group(1).strip()
                    except AttributeError:
                        importpatners = "null"
                  

                    data['data'].append({
                        "country": name,
                        "governemnet": {
                            "chiefOfState": chiefOfState,
                            "headOfGovernment": headOfGovernment,
                            "governmentType": governmentType,
                            "capital": capital,
                            "legislature": legislature,
                            "judiciary": judiciary,
                            "ambassadortoUS": ambassadorToUs,
                            "uSAmbassador": uSAmbassador
                        },
                        "economy" : {
                            "economicOverview" : economicOverview,
                            "gdp" : gDP,
                            "gdpPerCapita" : gDPPerCapita,
                            "imports" : {
                                "total": importsTotal,
                                "patners": importpatners
                            },
                            "exports" : {
                                "total": exportsTotal,
                                "patners": exportpatners
                            }
                        },
                        "people" : {
                            "population" : population,
                            "populationGrowth" : populationGrowth,
                            "ethnicity" : ethnicity,
                            "language" : language,
                            "religion" : religion,
                            "urbanization" : urbanization,
                            "literacy" : literacy
                        },
                        "geography" : {
                            "area" : {
                                "total" : total,
                                "land" : land,
                                "water" : water
                            },
                            "climate" : climate,
                            "naturalResources" : naturalResources
                        }
                    })
                    with open('data.json', 'w') as outfile:
                        json.dump(data, outfile)
                        outfile.write('\n')
        except PyPDF2.utils.PdfReadError:
            print("invalid PDF file")
            pass
        else:
            pass
        
