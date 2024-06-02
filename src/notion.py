from dotenv import load_dotenv
import requests
import os
from qgenerator import get_random_quote

load_dotenv()

NOTION_TOKEN  = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('QUOTES_DATABASE_ID')
BLOCK_ID = os.getenv('BLOCK_ID')

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def update_page(page_id: str, data: dict):
    url = f"https://api.notion.com/v1/pages/{page_id}"

    payload = {"properties": data}

    res = requests.patch(url, json=payload, headers=headers)
    return res

def get_page_blocks(page_id):
    url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    return data.get("results", [])

def update_block(block_id, update):
    url = f"https://api.notion.com/v1/blocks/{block_id}"
    payload = {
        "callout": {
            "rich_text": [
                {
                    "text": {
                        "content": f'{update[0]}',
                    },
                    "annotations": {
                        "italic": True,
                    }
                },
                {
                    "text": {
                        "content": '\n> ',
                    },
                    "annotations": {
                        "bold": True,
                    }
                },
                {
                    "text": {
                        "content": f'{update[1]}',
                    },
                    "annotations": {
                        "bold": True,
                        "color": "yellow"
                    }
                }
            ]
        }
    }

    response = requests.patch(url, headers=headers, json=payload)

def create_page_in_database(database_id, properties):
    url = "https://api.notion.com/v1/pages"

    payload = {
        "parent": {"database_id": database_id},
        "properties": properties
    }

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code != 200:
        print(f"Error: Received status code {response.status_code}")
        print(response.text)
    else:
        print(f"Page created successfully")

'''
new_page_properties = {
        "Quote": {
            "rich_text": [
                {
                    "text": {
                        "content": "Knowing is not enough; we must apply. Willing is not enough; we must do."
                    },
                    "annotations": {
                        "bold": False,
                        "italic": True
                    }
                },
            ]
        },
        "Author": {
            "rich_text": [
                {
                    "text": {
                        "content": "Johann Wolfgang von Goethe"
                    },
                    "annotations": {
                        "bold": True,
                        "italic": False
                    }
                },
            ]
        }
    }

create_page_in_database(DATABASE_ID, new_page_properties)
'''

blocks = get_page_blocks(BLOCK_ID)
update_block(blocks[1]['id'], get_random_quote())