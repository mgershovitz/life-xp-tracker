import os
from datetime import datetime

import requests
from flask import Flask, redirect, render_template, request

# Access the variables
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
QUESTS_DATABASE_ID = os.getenv("QUESTS_DATABASE_ID")
COMPLETED_DATABASE_ID = os.getenv("COMPLETED_DATABASE_ID")


headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}


def get_today_date():
    return datetime.today().strftime("%Y-%m-%d")


def get_database_query(database_id, payload=None):
    url = f"https://api.notion.com/v1/databases/{database_id}/query"
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()
    if response.status_code == 200:
        data = response.json()
        completed_quests = data[
            "results"
        ]  # Return the filtered results (quests for today)
    else:
        print(f"Error: {response.status_code}")
        return
    return data


def fetch_quests_from_notion():
    """Fetch available quests from the source Notion database."""
    data = get_database_query(QUESTS_DATABASE_ID)
    quests = []
    if not data:
        return []
    for result in data.get("results", []):
        quest_name = result["properties"]["Activity"]["title"][0]["text"]["content"]
        xp_value = result["properties"]["XP"]["number"]
        quests.append({"name": quest_name, "xp": xp_value})
    return quests


def add_quest_to_completed(quest, xp_value):
    """Add the selected quest to the 'Completed Quests' database."""
    today = get_today_date()
    url = "https://api.notion.com/v1/pages"

    # Payload to create a new page (quest completion entry)
    payload = {
        "parent": {"database_id": COMPLETED_DATABASE_ID},
        "properties": {
            "Date": {"date": {"start": today}},  # Add today's date
            "Activity": {
                "title": [{"text": {"content": quest}}]
            },  # Quest name as the title
            "XP": {"number": xp_value},
        },
    }

    response = requests.post(url, json=payload, headers=headers)

    if response.status_code == 200:
        return True
    else:
        print(f"Error adding quest: {response.status_code} - {response.text}")
        return False


def get_daily_xp_sum():

    today = get_today_date()
    query_payload = {
        "filter": {
            "property": "Date",  # Replace with your actual date property name
            "date": {"equals": today},  # Filter by today's date
        }
    }

    data = get_database_query(COMPLETED_DATABASE_ID, query_payload)
    if not data:
        return []

    # Calculate the daily XP sum
    daily_xp = sum(
        quest["properties"]["XP"]["number"] for quest in data.get("results", [])
    )

    return daily_xp
