from dotenv import load_dotenv
import requests
import os
import random

load_dotenv()

NOTION_TOKEN  = os.getenv('NOTION_TOKEN')
DATABASE_ID = os.getenv('QUOTES_DATABASE_ID')

headers = {
    "Authorization": "Bearer " + NOTION_TOKEN,
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28",
}

def get_pages(num_pages=None):
    url = f"https://api.notion.com/v1/databases/{DATABASE_ID}/query"

    get_all = num_pages is None
    page_size = 100 if get_all else num_pages

    payload = {"page_size": page_size}
    response = requests.post(url, json=payload, headers=headers)

    # Verifica el código de estado de la respuesta
    if response.status_code != 200:
        return []

    data = response.json()

    if "results" not in data:
        return []

    results = data["results"]
    while data.get("has_more") and get_all:
        payload = {"page_size": page_size, "start_cursor": data.get("next_cursor")}
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code != 200:
            break

        data = response.json()

        results.extend(data["results"])

    return results

def get_random_quote():
    pages = get_pages()
    page = pages[random.randint(0, len(pages) - 1)]
    try:
        props = page["properties"]
        quote = props["Quote"]["rich_text"][0]["text"]["content"]
        author = props["Author"]["rich_text"][0]["text"]["content"]
        return quote, author
    except IndexError:
        props = page["properties"]
        quote = props["Quote"]["rich_text"][0]["text"]["content"]
        return quote