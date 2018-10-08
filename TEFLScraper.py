from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import re
import pandas as pd


# CF to regular email address decoder
def decodeEmail(e):
    de = ""
    k = int(e[:2], 16)
    for i in range(2, len(e) - 1, 2):
        de += chr(int(e[i:i + 2], 16) ^ k)
    return de

employer_page_links = []
for i in range(0, 11):
    req = Request("https://teflsearch.com/employer-directory?page=" + str(i), headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")

    # file = open("content.txt", "w+", encoding="utf-8")
    # file.write(str(soup.prettify()))
    # file.close()

    all_links = soup.find_all("a", href=True)

    regexp = re.compile(r'^https://teflsearch.com/employer/*')
    for link in all_links:
        if regexp.search(str(link["href"])):
            # print(str(link["href"]))
            employer_page_links.append(str(link["href"]))

print(employer_page_links)

names_list = []
email_list = []



for link in employer_page_links:
    req = Request(link, headers={'User-Agent': 'Mozilla/5.0'})
    webpage = urlopen(req).read()
    soup = BeautifulSoup(webpage, "html.parser")

    name = soup.findAll("h1", {"class": "font-extra-large"})[0].text
    email = soup.findAll("a", {"class": "__cf_email__"})

    decodedEmail = ''
    if (len(email) > 0):
        decodedEmail = decodeEmail(str(email[0]['data-cfemail']))
    print(name + "\t"+ decodedEmail)
    names_list.append(name)
    email_list.append(decodedEmail)

print(names_list)
print(email_list)
dataframe = pd.DataFrame()
dataframe['Name'] = names_list
dataframe['Email'] = email_list
dataframe.to_csv("data.csv", index=False)
# dataframe.to_excel('test.xlsx', sheet_name='sheet1', index=False)