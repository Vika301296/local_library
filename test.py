import requests

from bs4 import BeautifulSoup

url = "https://tululu.org/b9/"


def parse_book_page(url):
    try:
        response = requests.get(url, verify=False, allow_redirects=False)
        soup = BeautifulSoup(response.text, "lxml")
        comments = soup.find_all("div", class_="texts")
        comment_texts = []
        for comment in comments:
            full_comment = comment.get_text()
            full_comment.split(')')
            comment_text = (full_comment.split(')'))[1].strip()
            comment_texts.append(comment_text)
        return comment_texts
    except requests.HTTPError:
        print(f"HTTPError for book {url}")
        # Return None if there's an error


print(parse_book_page(url))
