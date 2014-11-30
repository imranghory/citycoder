import csv 
import pycountry

countrymap = {}
regionmap = {}
citymap = {}
allcities = {}


with open('cities15000.txt', 'rb') as csvfile:
    csvreader = csv.reader(csvfile, delimiter='\t', quotechar=None)
    count = 0 
    for row in csvreader:
        if int(row[14])>100000:  
            country = row[8]

            if not citymap.has_key(country):
                citymap[country] = []
                
            citymap[country].append((row[1],row[10],row[14]))

            if not allcities.has_key(row[1]):
                allcities[row[1]] = []
            allcities[row[1]].append((country,row[14]))
            
            if row[1] != row[2]:
                citymap[country].append((row[2],row[10],row[14]))

                if not allcities.has_key(row[2]):
                    allcities[row[2]] = []
                allcities[row[2]].append((country,row[14])) 

for countrycode in [(c.name.split(',')[0].split("(")[0].strip(),c.alpha2) for c in pycountry.countries]:
    countrymap[countrycode[0]] = countrycode[1]

# add some country names that aren't official but commonly used
countrymap.update({'Russia' : 'RU', 'South Korea' : 'KR', 'Syria' : 'SY', 'UK' : 'GB', 'Brasil' : 'BR', 'Holland' : 'NL'})
from collections import Counter

uniqregions =  [x for x,y in Counter([x.name for x in pycountry.subdivisions]).items() if y == 1]

for c in [(x.name, x.country.alpha2) for x in pycountry.subdivisions if x.name in uniqregions]:
    regionmap[c[0]] = c[1]



def parserUS(x, location=None):
    states = {'AL': 'Alabama', 'AK':'Alaska','AZ':'Arizona','AR':'Arkansas','CA':'California','CO':'Colorado','CT':'Connecticut','DE':'Delaware','FL':'Florida','GA':'Georgia','HI':'Hawaii','ID':'Idaho','IL':'Illinois','IN':'Indiana','IA':'Iowa','KS':'Kansas','KY':'Kentucky','LA':'Louisiana','ME':'Maine','MD':'Maryland','MA':'Massachusetts','MI':'Michigan','MN':'Minnesota','MS':'Mississippi','MO':'Missouri', 'MT':'Montana', 'NE':'Nebraska', 'NV':'Nevada', 'NH':'New Hampshire', 'NJ':'New Jersey', 'NM':'New Mexico', 'NY':'New York', 'NC':'North Carolina', 'ND':'North Dakota', 'OH':'Ohio', 'OK':'Oklahoma', 'OR':'Oregon', 'PA':'Pennsylvania', 'RI':'Rhode Island', 'SC':'South Carolina', 'SD':'South Dakota', 'TN':'Tennessee', 'TX':'Texas', 'UT':'Utah', 'VT':'Vermont', 'VA':'Virginia', 'WA':'Washington', 'WV':'West Virginia', 'WI':'Wisconsin', 'WY':'Wyoming'}
    if x in states.keys():
        return {'Country' : 'US', 'Region' : states[x], 'City' : None }
    if x in states.values():
        return {'Country' : 'US', 'Region' : x, 'City' : None }
      
    lastsegment = x.split(',')[-1].strip()
    if lastsegment in ['US', 'USA', ' United States of America', 'United States']:
        return parserUS(x[0:x.rfind(',')], {'Country' : 'US', 'Region' : None, 'City' : None })

    if lastsegment in states.keys():
        return parserUS(x[0:x.rfind(',')], {'Country' : 'US', 'Region' : states[lastsegment], 'City' : None })     
 
    if lastsegment in states.values():
        return parserUS(x[0:x.rfind(',')], {'Country' : 'US', 'Region' : lastsegment, 'City' : None })

    
    if location and location['Region']:
        region = location['Region']
    else:
        region = None
    
    firstsegment = x.split(',')[0].strip()
    uscities = [c[0] for c in citymap['US']]

    if firstsegment in uscities:
        return {'Country' : 'US', 'Region' : region, 'City': firstsegment }
    if lastsegment in uscities:
        return {'Country' : 'US', 'Region' : region, 'City': lastsegment }
        
    if location:
        return location
    else:
        return None


def parserGeneral(text, location=None):
    lastsegment = text.split(',')[-1].strip()
    if lastsegment in countrymap.keys():
        return parserGeneral(text[0:text.rfind(',')], {'Country' : countrymap[lastsegment], 'Region' : None, 'City' : None })
      
    if location and location['Country']:
        try:      
            localregions = pycountry.subdivisions.get(country_code=location['Country'])
            if lastsegment in localregions:
                return parserGeneral(text[0:text.rfind(',')], {'Country' : location['Country'], 'Region' : lastsegment, 'City' : None })
        except: #we don't have subdivisions for some countries 
            pass
    if location and location['Region']:
        region = location['Region']
    else:
        region = None
    
    firstsegment = text.split(',')[0].strip()
    if location and location['Country']:
        try:    
            localcities = [c[0] for c in citymap[location['Country']]]

            if firstsegment in localcities:
                return {'Country' : location['Country'], 'Region' : region, 'City': firstsegment }
            if lastsegment in localcities:
                return {'Country' : location['Country'], 'Region' : region, 'City': lastsegment }
        except:
            pass

    if regionmap.has_key(lastsegment):
        return parserGeneral(text[0:text.rfind(',')],{'Country' : regionmap[lastsegment], 'Region' : lastsegment, 'City' : None})    
        
    if location:
        return location
    else:
        if regionmap.has_key(text):
            return {'Country' : regionmap[text], 'Region' : text, 'City' : None}        
        if allcities.has_key(text):
            return {'Country' : sorted(allcities[text], key = lambda c: c[1], reverse=True)[0][0], 'Region' : None, 'City': text}

        if regionmap.has_key(firstsegment):
            return {'Country' : regionmap[firstsegment], 'Region' : lastsegment, 'City' : None}    

        if allcities.has_key(firstsegment):
            return {'Country' : sorted(allcities[firstsegment], key = lambda c: c[1], reverse=True)[0][0], 'Region' : None, 'City': firstsegment}

        return None

def parselocation(text):
    text = text.strip()
    location = parserGeneral(text)
    if not location or location['Country'] == 'US':
        location = parserUS(text)
    if not location:
	location = parserGeneral(','.join(text.split(',')[::-1]))

    if location and location['Country']:
        location['iso3'] = pycountry.countries.get(alpha2=location['Country']).alpha3
	location['Country'] = pycountry.countries.get(alpha2=location['Country']).name
    return location
