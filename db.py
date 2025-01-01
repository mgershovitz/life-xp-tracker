import requests
import os

# Access the variables
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
DATABASE_ID = os.getenv('DATABASE_ID')

headers = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

def getActivities():
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        return [result['properties']['Activity']['title'][0]['text']['content'] 
                for result in data['results']]
    else:
        print("Failed to fetch data:", response.text)
        return []

dropdown_items = getActivities()
print(dropdown_items)  # Use this data to populate your dropdown