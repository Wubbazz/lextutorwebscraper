from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import csv
import os

def get_id_num(e):
    return int(e[0:3])
def get_q_num(e):
    q_num = e[8:10]
    if not q_num.isdigit():
        q_num = e[8]
    return int(q_num)
def isnumber(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

text_files = os.listdir('textdata')
text_files.sort(key=get_q_num)
text_files.sort(key=get_id_num)

print(text_files)

numeric_data_fields = ['ID', 'Question number','Words in text (tokens)', 'Different words (types)', 'Type-token ratio (TTR)',
                               'Tokens per type', 'Lexical density', 'Tokens', 'Types', 'Families', 'Tokens per Family',
                               'Family/token ratio', 'Types per Family', 'Singleton Ratio']
data = [numeric_data_fields]
for text_file in text_files:
    id_num = get_id_num(text_file)
    q_num = get_q_num(text_file)
    file_addr = "textdata/" + text_file
    with open(file_addr, "r") as f:
        driver.get("https://www.lextutor.ca/vp/comp/")

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.XPATH, '//*[@value="SUBMIT_window"]'))
        )

        input_element = driver.find_element(By.ID, "text_input")
        input_element.clear()
        input_element.send_keys(f.read())

        button = driver.find_element(By.XPATH, '//*[@value="SUBMIT_window"]')

        button.click()

        WebDriverWait(driver, 5).until(
            EC.presence_of_element_located((By.NAME, 'editor'))
        )

        data_tables = driver.find_elements(By.CLASS_NAME, "datasheet")

        # The second table is the data we want for now
        ratio_data_table = data_tables[1].find_elements(By.TAG_NAME, 'td')

        numeric_data = [id_num, q_num]
        # Extract the number data
        for el in ratio_data_table:
            if isnumber(el.text):
                numeric_data.append(el.text)

        data.append(numeric_data)
driver.quit()

with open('extracted_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)


