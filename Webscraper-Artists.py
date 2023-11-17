from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.ui import Select
import pandas as pd


# All lists
stage_name = []
full_name = []
korean_name = []
korean_stage_name = []
date_of_birth = []
group = []
country = []
birthplace = []
gender = []
kpop_artists = []

URL = "https://dbkpop.com/db/all-k-pop-idols/"

adblock = webdriver.ChromeOptions()
adblock.add_extension('ADBlocker.crx')
driver = webdriver.Chrome('/Users/mx0601/Downloads/chromedriver-mac-x64/chromedriver', options= adblock) # installing adblocker
driver.implicitly_wait(30)
driver.get(URL)

# Accessing the entry dropdown menu
div_select = driver.find_element_by_xpath('//*[@id="table_1_length"]/label/div/button')
driver.execute_script('arguments[0].click();', div_select)
selector = div_select.find_element_by_xpath("//select[@name='table_1_length']")
select = Select(selector)
select.select_by_value('-1') #display all


# Accessing the column button for the dropdown menu
xpath_column_dropdown = "dt-button buttons-collection buttons-colvis DTTT_button DTTT_button_colvis"
driver.implicitly_wait(30)
div_to_columns = driver.find_element_by_xpath('//*[@id="table_1_wrapper"]/div[1]/button')
driver.execute_script('arguments[0].click();', div_to_columns) # clicking the column button to reveal the dropdown menu


# Deselecting the following values: Profile, Short Name, Fanclub Name
values_to_deselect = [1, 13]
for i in range(1, 14):
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

for i in range(0, len(data_values), 9):
    # Extract a sublist from the input_list starting at index i and ending at index i + sublist_size
    sublist = data_values[i:i + 9]
    driver.implicitly_wait(10)
    # Append the extracted sublist to the result list
    if len(sublist) == 9:
        kpop_artists.append(sublist)


# Appending the values to our respective lists
for artist in kpop_artists:
    full_name.append(artist[0].text)
    stage_name.append(artist[1].text)
    korean_name.append(artist[2].text)
    korean_stage_name.append(artist[3].text)
    date_of_birth.append(artist[4].text)
    group.append(artist[5].text)
    country.append(artist[6].text)
    birthplace.append(artist[7].text)
    gender.append(artist[8].text)
    print(artist[0].text, artist[1].text, artist[2].text, artist[3].text, artist[4].text, artist[5].text, artist[6].text, artist[7].text, artist[8].text)
    
lists = [full_name, stage_name, korean_name, korean_stage_name, date_of_birth, group, country, birthplace, gender]

# Removing the last index of all the lists (contains foreign unwanted data)
for list in lists:
    list.pop(-1)

# Creating a dataframe using pandas and exporting as a csv.
df = pd.DataFrame({'Full Name':full_name, 'Stage Name': stage_name, 'Korean Name': korean_name, 'Korean Stage Name': korean_stage_name, 'Birthday': date_of_birth, 'Group': group, 'Country': country, 'Gender': gender})
df.to_csv('kpop_artists.csv', sep='\t', encoding='utf-8', index=False)
