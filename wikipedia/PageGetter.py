import warnings

import wikipedia.exceptions
import wikipediaapi
import wikipedia as wp
import requests

from bs4 import GuessedAtParserWarning
warnings.filterwarnings('ignore', category=GuessedAtParserWarning)
def search():
    search_term = input('Enter the search term: ')
    page_py = wiki_wiki.page(search_term)
    wp_page = wp.page(search_term)
    return wp_page, page_py


wiki_wiki = wikipediaapi.Wikipedia('PageGetter (christopher.a.castillo.b@gmail.com', 'en',
                                   extract_format=wikipediaapi.ExtractFormat.WIKI)

# page_py =wiki_wiki.page(search_term)
try:
    wp_page, page_py = search()
except wikipedia.exceptions.PageError as p:
    print("Error: ", p)
    wp_page, page_py = search()
except wikipedia.exceptions.DisambiguationError as d:
    print("Error: ", d)
    wp_page, page_py = search()
# except wikipedia.BeautifulSoup.parserClass. as parse:
#     print("Error: ")
#     wp_page, page_py = search()


print(page_py.text)
list_img_urls = wp_page.images
for filename in wp_page.images[:]:  # Creating a copy of the list to avoid modification during iteration
    if filename.endswith(".svg") or filename.endswith(".gif"):
        wp_page.images.remove(filename)
print(list_img_urls)
