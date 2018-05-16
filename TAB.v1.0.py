import csv
import time
from selenium import webdriver
from bs4 import BeautifulSoup

#Set website base url
base_url = "https://www.tab.co.nz/sport"
sports_url = base_url+"/sports-betting"

#Set output location
base_file = "Results\\TAB\\"

#load browser driver
driver = webdriver.Chrome()
driver.get(base_url)

#parse page
new_soup = BeautifulSoup(driver.page_source, 'lxml')

#search for soccer link and load page
data_soccer = new_soup.find('dt', id="spSOCC").find_next_siblings('dd')[0]
urls_soccer = data_soccer.find_all('a', class_="game-page")

# #load each soccer game
for url_soccer in urls_soccer:
    #load url
    file_name_socc = (base_file +" " +url_soccer.text.strip() + ".csv").replace("/","-")
    with open(file_name_socc, 'w') as f:
        f.write("Section,Selection,Odds\n")
    url_soccer_href = base_url+url_soccer.get('href')
    print(url_soccer_href)
    driver.get(url_soccer_href)
    driver.refresh()
    soup2 = BeautifulSoup(driver.page_source, 'lxml')
    body_soup = soup2.find('body',class_="sport")
    soup=body_soup.find('div',class_="main-outer").find('div',class_="main").find('div',id="game-page")   
    #Parse betting page and extract all bets
    # # Get Game Name
    match_soccer = soup.find('h3', class_="name").text
    #Find all Sections
    sec_soccer = soup.find_all('div', class_="option option_fpw")
    for i in sec_soccer:
        # Get Section Name
        sec_soccer_name = i.find('a', class_="js-state description").text
        # #selection - 'td', class=c2 cnorder-selection
        lines_socc = i.find_all('td', class_="c2 cnorder-selection")
        odds_socc = i.find_all('td', class_="odds-fpw c3 cnorder-odds")
        for x in range(len(lines_socc) -1):
            with open(file_name_socc, 'a') as f:
                f.write(sec_soccer_name+","+lines_socc[x].text.strip()+","+odds_socc[x].span.text+"\n")

driver.close()
