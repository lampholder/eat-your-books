import json
import requests
from bs4 import BeautifulSoup

data = {
    "Userkey": "bob@example.com",
    "Password": "S3CR3T",
    "Remember": "false"
}

session = requests.Session() 
login = session.post("https://www.eatyourbooks.com/signin", data=data)

def add_book(book_id):
    url = "https://www.eatyourbooks.com/libraryservice/addtobookshelf"
    session.post(url, json={
        "entityId": book_id,
        "entityType" 1
    })


def remove_book(book_id):
    url = "https://www.eatyourbooks.com/libraryservice/removefrombookshelf"
    session.post(url, json={
        "entityId": book_id,
        "entityType" 1
    })

def search(query):
    search_url = "https://www.eatyourbooks.com/bookshelf?q=%s" % query

    while True:
        search = session.get(search_url)
        soup = BeautifulSoup(search.text, features="html.parser")
        recipes = [html_to_json(recipe) for recipe in soup.find_all("div", "book-data")]
        for recipe in recipes:
            yield recipe
        next_page_link = soup.find("a", "page-next")
        if next_page_link:
            search_url = next_page_link["href"]
        else:
            break

def html_to_json(recipe):
    recipe_title = recipe.find("h2", "title").find("a", "RecipeTitleExp").text.strip()
    book_full_title = recipe.find("h3").find("a", "full-title").text
    book_main = recipe.find("h3").find("a", "main-title")
    book_main_title = book_main.text
    book_link = "https://www.eatyourbooks.com" + book_main["href"]
    author = recipe.find("a", "author")
    author_name = author.text
    author_link = "https://www.eatyourbooks.com" + author["href"]
    categories = [x.strip() for x in recipe.find("ul", "meta").find_all('li')[0].text.strip().split(";")[1:]]
    ingredients = [x.strip() for x in recipe.find("ul", "meta").find_all('li')[1].text.strip().split(";")[1:]]

    return {
        "title": recipe_title,
        "source": {
            "title": {
                "main": book_main_title,
                "full": book_full_title
            },
            "uri": book_link
        },
        "author": {
            "name": author_name,
            "uri": author_link
        },
        "categories": categories,
        "ingredients": ingredients
    }

x = [r for r in search("egg")]
print(json.dumps(x, indent=2))
