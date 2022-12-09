#Baixe as dependências e execute o código :)
#1 - Acesse o site https://pt.wikipedia.org/wiki/Lista_de_capitais_do_Brasil_por_%C3%A1rea
# e extraía a sede do governo, a unidade federativa e a área. Depois coloque esses dados em um Pandas Dataframe.




import requests
import pandas as pd
from bs4 import BeautifulSoup

def df_from_url():
    url = "https://pt.wikipedia.org/wiki/Lista_de_capitais_do_Brasil_por_%C3%A1rea"
    data = requests.get(url).text
    soup = BeautifulSoup(data, 'html.parser')
    table = soup.find('table', class_='wikitable sortable')
    df = pd.DataFrame(columns=['sede_do_governo', 'uf', 'area'])
    
    for row in table.tbody.find_all('tr'):
        cols = row.find_all('td')
        if(cols !=  []):
            sede = cols[1].a.text.strip()
            uf = cols[3].a.text.strip()
            area = cols[4].text.strip('&0.\n')
            df = df.append({'sede_do_governo': sede, 'uf': uf, 'area': area}, ignore_index=True)
            
    return df

print(df_from_url())

