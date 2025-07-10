from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from tqdm import tqdm
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
def generate_repeated_k_list(num_repetitions=25):
  repeated_list = []
  for i in range(1, num_repetitions + 1):
    repeated_list.append(f'K-{i} Families')
    repeated_list.append(f'K-{i} Types')
    repeated_list.append(f'K-{i} Tokens')
    repeated_list.append(f'K-{i} Cumul. token')
  return repeated_list

service = Service(executable_path="chromedriver.exe")
driver = webdriver.Chrome(service=service)

text_files = os.listdir('textdata')
text_files.sort(key=get_q_num)
text_files.sort(key=get_id_num)

numeric_data_fields = ['Subject', 'Item','Words in text (tokens)', 'Different words (types)', 'Type-token ratio (TTR)',
                               'Tokens per type', 'Lexical density', 'Tokens', 'Types', 'Families', 'Tokens per Family',
                               'Family/token ratio', 'Types per Family', 'Singleton Ratio']
numeric_data_fields = numeric_data_fields + generate_repeated_k_list()
data = [numeric_data_fields]

for i in tqdm(range((len(text_files)))):
    id_num = text_files[i][0:5] + str(get_id_num(text_files[i]))
    q_num = 'P' + str(get_q_num(text_files[i]))
    file_addr = "textdata/" + text_files[i]
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

        k_data_table = data_tables[0].find_elements(By.TAG_NAME, 'tr')
        k_data_list = []
        # This index starts at 1 because the first item is not needed and we also don't need the last 2 items
        for i in range(1,len(k_data_table) - 2):
            valid_k_data = [num for num in k_data_table[i].text.split() if isnumber(num)]
            if len(valid_k_data) != 4:
                valid_k_data = [0,0,0,0.0]
            k_data_list = k_data_list + valid_k_data

        # The second table is the data we want for now
        ratio_data_table = data_tables[1].find_elements(By.TAG_NAME, 'td')

        numeric_data = [id_num, q_num]
        # Extract the number data
        for el in ratio_data_table:
            if isnumber(el.text):
                numeric_data.append(el.text)
        numeric_data = numeric_data + k_data_list
        data.append(numeric_data)
driver.quit()

with open('extracted_data.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(data)


