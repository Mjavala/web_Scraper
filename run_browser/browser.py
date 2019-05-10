from selenium import webdriver
import pandas as pd
import numpy as np
from bs4 import BeautifulSoup as bs

browser = webdriver.Firefox(executable_path="C:\\ProgramData\\Anaconda3\\Lib\\site-packages\\geckodriver-v0.24.0-win64\geckodriver.exe")
browser.get('https://nacehouston.net/directory.php')
 #gives an implicit wait for 20 seconds

#navigate the page to desired table output
el = browser.find_elements_by_name('maxItems')
for option in browser.find_elements_by_tag_name('option'):
        if option.text == "200":
                option.click()
                break
            
el = browser.find_element_by_xpath('//ul[@class="page-nav alpha"]/li[4]/a')
el.click()

lever = True

while lever:
    datalist = []
    comp_list = []
    # get the soup
    soup_level1 = bs(browser.page_source, 'lxml')

    table = soup_level1.find("table", {"class": "data-table mem-directory"})
    table_sel = browser.find_element_by_xpath('//table[@class="data-table mem-directory"]')

    #emails_sub_table = soup_level1.select("tbody", {"attr" : "alt"})[0]
    #able_rows = table.find_all("tr", {"class" : "alt"})[0]
    #panda read the soup
    df = pd.read_html(str(table),header=0)

    datalist.append(df[0])

    data_set = datalist[0]

    df1 = pd.DataFrame(data_set)

    df2 = df1[~df1.Company.str.startswith('(', na=False)]

    df3 = df2[~df2["Address"].str.contains("nan", na=True)]
    
    for comp_link_cells in table_sel.find_elements_by_xpath('//table[@class="data-table mem-directory"]/tbody/tr/td[1]/p'):
        try:
            comp = comp_link_cells.find_element_by_css_selector('a')
            link = comp.get_attribute('href')
            #link = link[7:]
            comp_list.append(link)
        except:
            word = "NaN"
            comp_list.append(word)
    
    df_comp_links = pd.DataFrame(comp_list)
    
    df_comp_links.to_csv('tampa_company_links.csv')
            
    break
