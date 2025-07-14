# Lang Extractor
This script is for my LANG390 course at VIU. It simply extracts specific characteristics from the website https://www.lextutor.ca/vp/comp/ when inputing txt data. 

# Text file naming format
- The text file must be named in the format "XXX_JD_QX_70db.txt"
- Where the initial 3 digits corrospond to the subject and following initials (JD) to the experimenter. QX being the question number.
  - e.g. 041_JD_Q13_70db.txt

# Setup
- Create a folder called 'textdata' in the same direcotry of the main.py
- Place all the txt files in the textdata folder
- download the latest version of the chrome driver from https://googlechromelabs.github.io/chrome-for-testing/ or the version corresponding to your google chrome version and place it in the same file as main.py. 
  - Make sure the chrome driver is named "chromedriver"

- In the command line navigate to file that contains main.py
- Create a virtual environment
```bash
    python -m venv venv
```
- Activate the environment
```bash
    source venv/bin/activate
```
- Install the required packages
```bash
    pip install -r requirements.txt
```

# Runing the Script
- Simply run the script
  ```bash
  python3 main.py
  ```
- And a CSV file called extracted_data will appear in the same directory as main.py
