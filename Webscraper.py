from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd


# All lists
name = []
korean_name = []
debut_date = []
company_name = []
num_members = []
num_og_members = []
isActive = []
kpop_groups = []

URL = "https://dbkpop.com/db/k-pop-girlgroups/"

adblock = webdriver.ChromeOptions()
adblock.add_extension('ADBlocker.crx')
driver = webdriver.Chrome('/Users/mx0601/Downloads/chromedriver-mac-x64/chromedriver', options= adblock) # installing adblocker
driver.implicitly_wait(30)
driver.get(URL)

# Accessing the column button for the dropdown menu
xpath_column_dropdown = "dt-button buttons-collection buttons-colvis DTTT_button DTTT_button_colvis"
driver.implicitly_wait(30)
div_to_columns = driver.find_element_by_xpath('//*[@id="table_1_wrapper"]/div[1]/button')
driver.execute_script('arguments[0].click();', div_to_columns) # clicking the column button to reveal the dropdown menu


# Deselecting the following values: Profile, Short Name, Fanclub Name
values_to_deselect = [1, 3, 9]
for i in range(1, 10):
    button = driver.find_element_by_xpath(f'//*[@id="table_1_wrapper"]/div[1]/div[2]/div/button[{i}]')
    if i in values_to_deselect:
        driver.execute_script('arguments[0].click();', button) # deselecting the values


driver.implicitly_wait(30)

# arguments[0].style.zIndex-'9999' brings out the element to the front; not needed here; bug fixed
# https://stackoverflow.com/questions/49871432/what-does-arguments0-and-arguments1-mean-when-using-executescript-method-fro

# Accessing the table 
table = driver.find_element_by_xpath("//div[@class='wdtscroll']//table[@id='table_1']//tbody")
rows = table.find_elements_by_xpath("//tr")
data_values = rows[0].find_elements_by_xpath("//td") 

for i in range(0, len(data_values), 7):
    # Extract a sublist from the input_list starting at index i and ending at index i + sublist_size
    sublist = data_values[i:i + 7]
    driver.implicitly_wait(10)
    # Append the extracted sublist to the result list
    if len(sublist) != 7:
        continue
    else:
        kpop_groups.append(sublist)

# Appending the values to our respective lists
for group in kpop_groups:
    name.append(group[0].text)
    korean_name.append(group[1].text)
    debut_date.append(group[2].text)
    company_name.append(group[3].text)
    num_members.append(group[4].text)
    num_og_members.append(group[5].text)
    isActive.append(group[6].text)
    print(group[0].text, group[1].text, group[2].text, group[3].text,group[4].text,group[5].text,group[6].text)

lists = [name, korean_name, debut_date, company_name, num_members, num_og_members, isActive]

# Removing the last index of all the lists (contains foreign unwanted data)
for list in lists:
    list.pop(-1)

# Creating a dataframe using pandas and exporting as a csv.
df = pd.DataFrame({'Name':name, 'Korean Name': korean_name, 'Debut Date': debut_date, 'Company': company_name, 'Current Member Count': num_members, 'Original Member Count': num_og_members, 'Active': isActive})
df.to_csv('kpop_girl_groups.csv', sep='\t', encoding='utf-8', index=False)
