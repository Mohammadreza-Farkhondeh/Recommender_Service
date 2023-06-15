import csv
import re
import requests
from bs4 import BeautifulSoup

# Send a GET request to the web page
url = 'https://coinmarketcap.com/'
response = requests.get(url)

# Parse the HTML content using BeautifulSoup
soup = BeautifulSoup(response.text, 'html.parser')

# Find the table in the HTML content
table = soup.find('table', {'class': "sc-beb003d5-3 ieTeVa cmc-table"})

# Get the table headers
headers = [header.text.strip() for header in table.find_all('th')]

# Get the table rows
rows = []
for row in table.find_all('tr'):
    rows.append([cell.text.strip() for cell in row.find_all('td')])


index_to_delete = []

for i in range(len(rows)):
    try:
        rows[i][3] = rows[i][3].replace(',', '')
        rows[i][3] = rows[i][3].replace('$', '')
        rows[i][4] = rows[i][4].replace('%', '')

        for n in range(len(rows[i][8])):
            if rows[i][8][n] == ',':
                if rows[i][8][n+4] != ',':
                    rows[i][8] = rows[i][8][:n+4]
                    break
        rows[i][7] = re.sub(r'\$\w*\.*\w*\$', '', rows[i][7])
        rows[i][8] = rows[i][8].split(' ')[0]
        rows[i][7] = rows[i][7].replace(',', '')
        rows[i][8] = rows[i][8].replace('$', '')
        rows[i][8] = rows[i][8].replace(',', '')
        if rows[i][3][3:5] == '..':
            index_to_delete.append(i)
        rows[i][2] = rows[i][2].split(str(i))[0]
    #     re.findall(r'(\d*)', rows[i][2]))[0])
    except Exception as err:
        print (err, i)

# Write the table to a CSV file
with open('crypto_data.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(headers)
    for row in rows:
        if rows.index(row) not in index_to_delete:
            writer.writerow(row)
