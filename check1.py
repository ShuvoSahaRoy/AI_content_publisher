from main_script import publish
import pandas as pd

openai_api_key = ''
site_url = ''
username = ''
password = ''
max_tokens = ''

# Read credentials from config.txt file
try:
    with open('config.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith('openai_api_key'):
                openai_api_key = line.split('=')[1].strip()
            elif line.startswith('site_url'):
                site_url = line.split('=')[1].strip()
            elif line.startswith('username'):
                username = line.split('=')[1].strip()
            elif line.startswith('password'):
                password = line.split('=')[1].strip()
            elif line.startswith('max_tokens'):
                max_tokens =int( line.split('=')[1].strip() )
except FileNotFoundError:
    print("Config file not found. Please make sure 'config.txt' exists in the same directory as your script.")
    exit(1)
except Exception as e:
    print(f"An error occurred while reading the config file: {str(e)}")
    exit(1)

# Provide the path of the XLSX file
xlsx_path = "content.xlsx"

try:
    # Read the XLSX file into a pandas DataFrame
    df = pd.read_excel(xlsx_path)

    i = 1
    # Iterate through each row in the DataFrame
    for index, row in df.iterrows():
        
        topic = row['topic'].upper()
        tags = row['tags'].split(',')
        points = row['points']
        slug = row['slug']
        catagory = row['catagory'].split(',')
        status = row['status']

        publish(openai_api_key, site_url, username, password, topic, tags, points, slug, catagory, status, max_tokens)
        i+=1
    print(f"Processing completed for {i}.")
except Exception as e:
    print(f"An error occurred while processing the file: {str(e)}")
