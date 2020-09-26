from bs4 import BeautifulSoup
import requests
import string
import io 
import json
import re

url = "https://www.cia.gov/library/publications/the-world-factbook/docs/one_page_summaries.html"
data = {}
data['data'] = []
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, features="lxml")
options = soup.select('option')
for option in options:
    if option['value'] and option['data-place-code']:
        values = option['data-place-code']
        url1 = "https://www.cia.gov/library/publications/the-world-factbook/geos/"+ values.lower() + ".html"
        if requests.get(url1).text:
            html_content1 = requests.get(url1).text
            soup1 = BeautifulSoup(html_content1, features="lxml")
            
            countryClass = soup1.find('span', {'class': 'region_name1 countryName'})
            if countryClass:
                country = countryClass.text.encode("utf-8", errors="ignore").strip()
            else:
                country = "Not Found"
            
            continentClass = soup1.find('div', {'id': 'field-map-references'})
            if continentClass:
                continent = continentClass.text.encode("utf-8", errors="ignore").strip()
            else:
                continent = "Not Found"

            flagClass = soup1.find('div', {'class': 'flagBox'})
            if flagClass:
                flagPath = flagClass.img['src'].replace('..', 'https://www.cia.gov/library/publications/the-world-factbook')
            else:
                flagPath = "Not Found"

            mapClass = soup1.find('div', {'class': 'map-holder'})
            if mapClass:
                mapPath = mapClass.img['src'].replace('..', 'https://www.cia.gov/library/publications/the-world-factbook')
            else:
                mapPath = "Not Found"
                
            populationMainClass = soup1.find('div', {'id': 'field-population'})
            if populationMainClass:
                populationClass = populationMainClass.find('span' , {'class':'subfield-number'})
                if populationClass:
                    population = populationClass.text.encode("utf-8", errors="ignore").strip()
                else:
                   population = "Not Found"
            else:
                population = "Not Found"
            
            languageMainClass = soup1.find('div', {'id': 'field-languages'})
            if languageMainClass:
                languageClass = languageMainClass.find('div' , {'class':'category_data subfield text'})
                if languageClass:
                    languageText= languageClass.text.encode("utf-8", errors="ignore")
                    languageRegex = re.sub(r'\([^)]*\)', '', languageText)
                    languageRegex1 = re.sub('[^A-Z a-z,]+', '', languageRegex)
                    languageSplit = languageRegex1.split('other', 1)[0]
                    language = languageSplit.replace('official', '').strip()
                else:
                    language = "Not Found"
            else:
                language = "Not Found"
            
            religionMainClass = soup1.find('div', {'id': 'field-religions'})
            if religionMainClass:
                religionClass = religionMainClass.find('div', {'class': 'category_data subfield text'})
                if religionClass:
                    religionText = religionClass.text.encode("utf-8", errors="ignore")
                    religionRegex = re.sub(r'\([^)]*\)', '', religionText)
                    religionRegex1 = re.sub('[^A-Z a-z,]+', '', religionRegex) 
                    religion = religionRegex1.split('other', 1)[0].strip()
                else:
                    religion = "Not Found"
            else:
                religion = "Not Found"

            governmentTypeMainClass = soup1.find('div', {'id': 'field-government-type'})
            if governmentTypeMainClass:
                governmentTypeClass = governmentTypeMainClass.find('div' , {'class':'category_data subfield text'})
                if governmentTypeClass:
                    governmentType = governmentTypeClass.text.encode("utf-8", errors="ignore").strip() 
                else:
                    governmentType = "Not Found"
            else:
                governmentType = "Not Found"

            capitalMainClass = soup1.find('div', {'id': 'field-capital'})
            if capitalMainClass:
                capitalClass = capitalMainClass.find('div' , {'class':'category_data subfield text'})
                if capitalClass:
                    capitalText = capitalClass.text.encode("utf-8", errors="ignore")
                    capital = capitalText.replace('name:','').strip()
                else:
                    capital = "Not Found"
            else:
                capital = "Not Found"

            climateMainClass = soup1.find('div', {'id': 'field-climate'})
            if climateMainClass:
                climateClass = climateMainClass.find('div' , {'class':'category_data subfield text'})
                if climateClass:
                    climate= climateClass.text.encode("utf-8", errors="ignore").strip() 
                else:
                    climate = "Not Found"
            else:
                climate = "Not Found"

            gdpMainClass = soup1.find('div', {'id': 'field-gdp-per-capita-ppp'})
            if gdpMainClass:
                gdpClass = gdpMainClass.find('span' , {'class':'subfield-number'})
                if gdpClass:
                    gdp = gdpClass.text.encode("utf-8", errors="ignore").strip()
                else:
                    gdp = "Not Found"
            else:
                gdp = "Not Found"

            agricultureMainClass = soup1.find('div', {'id': 'field-agriculture-products'})
            if agricultureMainClass:
                agricultureClass = agricultureMainClass.find('div' , {'class':'category_data subfield text'})
                if agricultureClass:
                    agriculture= agricultureClass.text.encode("utf-8", errors="ignore").strip()
                else:
                    agriculture = "Not Found"
            else:
                agriculture = "Not Found"

            industriesMainClass = soup1.find('div', {'id': 'field-industries'})
            if industriesMainClass:
                industriesClass = industriesMainClass.find('div' , {'class':'category_data subfield text'})
                if industriesClass:
                    industries= industriesClass.text.encode("utf-8", errors="ignore").strip()
                else:
                    industries = "Not Found"
            else:
                industries = "Not Found"

            exportsMainClass = soup1.find('div', {'id': 'field-exports-commodities'})
            if exportsMainClass:
                exportsClass = exportsMainClass.find('div' , {'class':'category_data subfield text'})
                if exportsClass:
                    exports = exportsClass.text.encode("utf-8", errors="ignore").strip() 
                else:
                    exports = "Not Found"
            else:
                exports = "Not Found"

            data['data'].append({
                "country": country,
                "continent": continent,
                "capital": capital,
                "governmentType": governmentType,
                "population": population, 
                "language": language,
                "religion": religion, 
                "background": "",
                "currency": "",
                "flagColor": "",
                "climate": climate, 
                "gdp": gdp,
                "agriculture": agriculture,
                "industries": industries,
                "exports": exports,
                "mapPath": mapPath,
                "flagPath": flagPath
            })
            with open('data2.json', 'w') as outfile:
                json.dump(data, outfile)
                outfile.write('\n')
    else:
        pass
