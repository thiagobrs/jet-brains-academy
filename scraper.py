# imports the necessary packages
import requests
import string
import os
from bs4 import BeautifulSoup


# removes punctuations and replaces whitespaces by _ in the article's title
def adjust_title(title):
    for letter in title:
        if letter in string.punctuation:
            title = title.replace(letter, '')
    return title.replace(' ', '_') + '.txt'


# retrieves the content of one article and saves it to a txt file
def get_article_content(page_url, filename):
    resp = requests.get(page_url, headers={'Accept-Language': 'en-US,en;q=0.5'})
    if resp:
        page = BeautifulSoup(resp.content, 'html.parser')
        content = page.find('div', {'class': 'c-article-body'}).text.strip().encode()

        # saves the article content into a file
        with open(filename, 'wb') as file:
            file.write(content)
    else:
        print("Error retrieving article '" + os.path.basename(filename) + "' content. Code " + str(resp.status_code) + ".")


# variables initialization
url = "https://www.nature.com/nature/articles?sort=PubDate&year=2020&page="
articles_list = []

# asks for the inputs
print("How many pages?")
num_pages = int(input())
print("What type of articles?")
article_type = input()

# gets every article_type in the first num_pages of the url
for num in range(1, num_pages + 1):
    print(f"Processing page {num}...")

    # tries to access the url in the 'num' page
    response = requests.get(url + str(num), headers={'Accept-Language': 'en-US,en;q=0.5'})
    if response:
        # creates a directory for the page 'num'
        dir_name = 'Page_' + str(num)
        if not os.access(dir_name, os.F_OK):
            os.mkdir(dir_name)

        # parses the response HTML
        soup = BeautifulSoup(response.content, 'html.parser')

        # finds all the articles of the type "News"
        for article in soup.find_all('article'):
            if article.find('span', {'data-test': 'article.type'}).text.strip().lower() == article_type.lower():
                # gets the url and the title of the article
                article_url = article.find('a', {'data-track-action': 'view article'}).get('href').strip()
                article_title = adjust_title(article.find('a', {'data-track-action': 'view article'}).text.strip())

                # gets the article content
                get_article_content("https://www.nature.com" + article_url, os.path.join(dir_name, article_title))

                # saves the article title in an output list
                articles_list.append(article_title)
    else:
        print("Error accessing url: code " + str(response.status_code) + ".")

if len(articles_list) > 0:
    print("Saved articles: ", articles_list)
