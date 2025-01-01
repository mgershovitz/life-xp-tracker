import os
from flask import Flask, render_template, request, redirect
import requests
from datetime import datetime

# Access the variables
NOTION_API_KEY = os.getenv('NOTION_API_KEY')
QUESTS_DATABASE_ID = os.getenv('QUESTS_DATABASE_ID')
COMPLETED_DATABASE_ID = os.getenv('COMPLETED_DATABASE_ID')

headers = {
    'Authorization': f'Bearer {NOTION_API_KEY}',
    'Content-Type': 'application/json',
    'Notion-Version': '2022-06-28'
}

def fetch_quests_from_notion():
    """Fetch available quests from the source Notion database."""
    url = f"https://api.notion.com/v1/databases/{QUESTS_DATABASE_ID}/query"
    response = requests.post(url, headers=headers)
    data = response.json()
    
    quests = []
    for result in data.get("results", []):
        quest_name = result["properties"]["Activity"]["title"][0]["text"]["content"]
        xp_value = result["properties"]["XP"]['number']
        quests.append({"name": quest_name, "xp": xp_value})
    return quests

def add_quest_to_completed(quest, xp_value):
    """Add the selected quest to the 'Completed Quests' database."""
    today = datetime.now().strftime("%Y-%m-%d")  # Today's date
    url = "https://api.notion.com/v1/pages"
    
    # Payload to create a new page (quest completion entry)
    payload = {
        "parent": {"database_id": COMPLETED_DATABASE_ID},
        "properties": {
            "Date": {"date": {"start": today}},  # Add today's date
            "Activity": {"title": [{"text": {"content": quest}}]},  # Quest name as the title
            "XP": {"number": xp_value}
        }
    }

    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code == 200:
        return True
    else:
        print(f"Error adding quest: {response.status_code} - {response.text}")
        return False